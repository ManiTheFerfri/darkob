import os
import json
import zlib
import base64
import sqlite3
import secrets
import logging
import time
from hashlib import sha256, sha512, pbkdf2_hmac

logger = logging.getLogger(__name__)

#: Where sessions live when the caller passes a bare name. Overridable so
#: tests and containers can redirect it.
SESSION_DIR_ENV = "DARKOB_SESSION_DIR"


def default_session_dir() -> str:
    """Directory used for sessions that are given as a bare name."""
    override = os.environ.get(SESSION_DIR_ENV)
    if override:
        return os.path.expanduser(override)
    return os.path.join(os.path.expanduser("~"), ".darkob", "sessions")


def _has_directory_part(name: str) -> bool:
    return os.path.isabs(name) or bool(os.path.dirname(name))


def resolve_session_path(name: str) -> str:
    """Resolve a session name to a stable absolute path.

    A name containing a directory component is used verbatim. A bare name
    is placed in :func:`default_session_dir`, except that an existing file
    with that name in the current directory wins, so sessions created by
    older versions keep working instead of forcing a re-login.
    """
    if _has_directory_part(name):
        return name

    if os.path.exists(name):
        return name

    directory = default_session_dir()
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError:
        logger.warning("Could not create session directory %s", directory,
                       exc_info=True)
        return name

    return os.path.join(directory, name)


# Keep the on-disk format stable. Changing either value would make every
# existing darkob session unreadable and force users through login again.
suffix = '.max'
_DB_KEY = sha256(b'darkob_session_full_encrypt_v2').digest()
_LEGACY_DB_KEYS = (
    sha256(b'maxrubika_session_full_encrypt_v2').digest(),
)

def _encrypt(data: dict) -> bytes:
    from Crypto.Cipher import AES
    plaintext = json.dumps(data).encode('utf-8')
    nonce = os.urandom(12)
    cipher = AES.new(_DB_KEY, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return nonce + tag + ciphertext

def _decrypt(data: bytes) -> dict:
    from Crypto.Cipher import AES

    nonce = data[:12]
    tag = data[12:28]
    ciphertext = data[28:]
    last_error = None
    for key in (_DB_KEY, *_LEGACY_DB_KEYS):
        try:
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return json.loads(plaintext.decode('utf-8'))
        except Exception as exc:
            last_error = exc
    raise last_error

def _read_rp_session(filename: str):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute('SELECT phone, auth, guid, agent, private_key FROM session')
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'phone': result[0],
            'auth': result[1],
            'guid': result[2],
            'agent': result[3],
            'private_key': result[4]
        }
    return None

def _read_json_session(filename: str):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        user = data.get('user', {})
        return {
            'phone': user.get('phone', ''),
            'auth': data.get('auth', '') or data.get('Auth', ''),
            'guid': user.get('user_guid', '') or data.get('guid', ''),
            'agent': user.get('user_agent', 'Mozilla/5.0') or data.get('agent', 'Mozilla/5.0'),
            'private_key': data.get('private_key', '') or data.get('Key', '')
        }
    except Exception:
        # A malformed or partially written session file is not fatal here:
        # the caller falls back to another session format. Log it so the
        # resulting "no session found" error is diagnosable.
        logger.debug("Could not read JSON session %r", filename, exc_info=True)
        return None

def _find_session(filename_without_ext: str):
    for ext in ['.darkob', '.max', '.rp', '.pyrubi', '.rubka', '.json']:
        full_path = filename_without_ext + ext
        if os.path.exists(full_path):
            if ext in ('.darkob', '.max'):
                try:
                    conn = sqlite3.connect(full_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT data FROM session')
                    row = cursor.fetchone()
                    conn.close()
                    if row and row[0]:
                        return _decrypt(row[0]), ext
                except Exception:
                    logger.warning(
                        "Could not read native session file %r", full_path,
                        exc_info=True,
                    )
            elif ext == '.rp':
                try:
                    data = _read_rp_session(full_path)
                    if data:
                        return data, ext
                except Exception:
                    pass
            elif ext in ('.pyrubi', '.rubka', '.json'):
                data = _read_json_session(full_path)
                if data and data.get('auth'):
                    return data, ext
    return None, None

class StringSession:
    _SECRET_PASSWORD = b"Darkob_Ultra_Secret_2026"
    _LEGACY_SECRET_PASSWORDS = (b"MAXRubika_Ultra_Secret_2026",)
    _ROUNDS = 3

    def __init__(self, string: str = ""):
        self._string = string

    @classmethod
    def _derive_master_key(
        cls, salt: bytes, password: str = None, secret: bytes = None
    ) -> bytes:
        if password:
            return pbkdf2_hmac('sha256', password.encode(), salt, 300000, dklen=32)
        return pbkdf2_hmac(
            'sha256', secret or cls._SECRET_PASSWORD, salt, 300000, dklen=32
        )

    @classmethod
    def _xor(cls, data: bytes, key: bytes) -> bytes:
        return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

    @classmethod
    def _encrypt_layer(cls, data: bytes, key: bytes) -> bytes:
        from Crypto.Cipher import AES
        nonce = secrets.token_bytes(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        ciphertext = cls._xor(ciphertext, sha512(key + nonce).digest())
        return nonce + tag + ciphertext

    @classmethod
    def _decrypt_layer(cls, data: bytes, key: bytes) -> bytes:
        from Crypto.Cipher import AES
        nonce = data[:12]
        tag = data[12:28]
        ciphertext = cls._xor(data[28:], sha512(key + nonce).digest())
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)

    @classmethod
    def from_data(cls, data: dict, password: str = None) -> "StringSession":
        json_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        compressed = zlib.compress(json_str.encode(), level=9)
        combined = sha512(compressed).digest() + compressed

        for _ in range(cls._ROUNDS):
            salt = secrets.token_bytes(16)
            key = cls._derive_master_key(salt, password)
            combined = salt + cls._encrypt_layer(combined, key)

        return cls(base64.b64encode(combined).decode())

    def to_data(self, password: str = None) -> dict:
        if not self._string:
            return {}

        secrets_to_try = (
            [None]
            if password
            else [self._SECRET_PASSWORD, *self._LEGACY_SECRET_PASSWORDS]
        )
        for secret in secrets_to_try:
            try:
                combined = base64.b64decode(self._string.encode())

                for _ in range(self._ROUNDS):
                    key = self._derive_master_key(
                        combined[:16], password, secret=secret
                    )
                    combined = self._decrypt_layer(combined[16:], key)

                data_hash, compressed = combined[:64], combined[64:]
                if sha512(compressed).digest() != data_hash:
                    raise ValueError("Hash mismatch.")

                return json.loads(zlib.decompress(compressed).decode())
            except Exception:
                continue
        return {}

    def __str__(self):
        return self._string

    def __bool__(self):
        return bool(self._string)

class Session:
    def __init__(self, session: str = None, create_file: bool = False,
                 string_session: str = None, password: str = None) -> None:

        self._connection = None
        self._cursor = None
        self._data = None
        self.is_logged_in = False
        self._imported_from = None

        if string_session:
            data = StringSession(string_session).to_data(password)
            if not data:
                raise ValueError("Invalid StringSession or wrong password.")
            if not isinstance(data, dict) or not data.get("auth"):
                raise ValueError(
                    "StringSession has no 'auth' credential; its payload is incomplete."
                )
            self.filename = None
            self.create_file = False
            self._imported_from = "string_session"
            self._data = data
            self.is_logged_in = True
            return

        base_name = (
            session if session and session.endswith(suffix) else f"{session}{suffix}"
        )
        self.filename = resolve_session_path(base_name)
        self.create_file = create_file

        if os.path.exists(self.filename) and not create_file:
            self._initialize_connection()
            info = self.information()
            if info and info[0]:
                self.is_logged_in = True
            else:
                # Never delete a session we could not read: quarantine it
                # so the login can be recovered and the failure is visible.
                self.close()
                self._connection = None
                self._cursor = None
                self._quarantine_unreadable_file()

        elif not create_file:
            base_name = (
                self.filename[:-len(suffix)]
                if self.filename.endswith(suffix)
                else self.filename
            )
            imported_data, ext = _find_session(base_name)
            if imported_data:
                self._imported_from = base_name + ext
                self._initialize_database()
                self.insert(
                    imported_data.get('phone'),
                    imported_data.get('auth'),
                    imported_data.get('guid'),
                    imported_data.get('agent'),
                    imported_data.get('private_key')
                )
                self.is_logged_in = True

                from ...utils.console import Console, Text

                console = Console()
                text = Text()
                text.append("Session migrated from ", style="cyan")
                text.append(base_name + ext, style="bold yellow")
                text.append(" to ", style="cyan")
                text.append(self.filename, style="bold green")
                # Never delete the source credential file during migration.
                # A failed or partial migration must not cause data loss.
                text.append("\nOld file kept.\n", style="dim")
                console.print(text)

        elif create_file:
            self._initialize_database()

    def _quarantine_unreadable_file(self) -> None:
        """Move an unreadable session aside instead of deleting it."""
        if not self.filename or not os.path.exists(self.filename):
            return

        quarantined = f"{self.filename}.corrupt-{int(time.time())}"
        try:
            os.replace(self.filename, quarantined)
            logger.warning(
                "Session %s could not be read (wrong key or corruption); "
                "moved it to %s. Log in again; the old file is kept.",
                self.filename,
                quarantined,
            )
        except OSError:
            logger.warning(
                "Session %s could not be read and could not be moved",
                self.filename,
                exc_info=True,
            )

    def _initialize_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self.filename, check_same_thread=False)
            self._cursor = self._connection.cursor()

    def _initialize_database(self):
        self._initialize_connection()
        self._cursor.execute('DROP TABLE IF EXISTS session')
        self._cursor.execute('CREATE TABLE session (data BLOB)')
        self._connection.commit()

    def information(self):
        if self._data is not None:
            return (
                self._data.get('phone'),
                self._data.get('auth'),
                self._data.get('guid'),
                self._data.get('agent', 'Mozilla/5.0'),
                self._data.get('private_key')
            )

        if not self._connection:
            return None

        try:
            cursor = self._connection.cursor()
            cursor.execute('SELECT data FROM session')
            result = cursor.fetchone()
            cursor.close()
            if result and result[0] is not None:
                data = _decrypt(result[0])
                return (
                    data.get('phone'), data.get('auth'), data.get('guid'),
                    data.get('agent'), data.get('private_key')
                )
        except Exception:
            logger.warning("Could not read session %s", self.filename,
                           exc_info=True)
        return None

    def insert(self, phone_number, auth, guid, user_agent, private_key,
               *args, **kwargs):
        if self._data is not None:
            self._data = {
                'phone': phone_number, 'auth': auth, 'guid': guid,
                'agent': user_agent, 'private_key': private_key
            }
            self.is_logged_in = True
            return

        if self._connection is None:
            self._initialize_database()

        encrypted = _encrypt({
            'phone': phone_number, 'auth': auth, 'guid': guid,
            'agent': user_agent, 'private_key': private_key
        })

        cursor = self._connection.cursor()
        cursor.execute('DELETE FROM session')
        cursor.execute('INSERT INTO session VALUES (?)', (encrypted,))
        self._connection.commit()
        cursor.close()
        self.is_logged_in = True

    @classmethod
    def from_string(cls, session_obj, file_name=None):
        info = session_obj.information()
        if file_name is None:
            if info is None or not info[0]:
                raise ValueError('file_name arg is not set.')
            file_name = info[0]
        session_instance = cls(file_name, create_file=(info is None))
        if info is not None:
            session_instance.insert(*info)
        return session_instance

    def close(self):
        if self._connection:
            self._connection.commit()
            self._connection.close()
            self._connection = None
            self._cursor = None
            self.is_logged_in = False

    def __del__(self):
        try:
            self.close()
        except Exception:
            # Interpreter shutdown: module globals (including the
            # logger) may already be gone, so logging here would raise
            # a second error. Swallowing is the only safe option.
            pass