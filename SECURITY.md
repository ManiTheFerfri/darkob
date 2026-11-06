# Security Policy

darkob handles bot tokens, `Messenger` session strings and the crypto that carries
them, so security reports are taken seriously and handled privately.

## Supported versions

darkob is pre-1.0, so **only the latest minor release receives security fixes** —
currently `0.17.x` and later.

| Version | Supported |
| --- | --- |
| `0.17.x` and later | :white_check_mark: receives security fixes |
| `< 0.17.0` | :x: unsupported |

If you are on an older minor, upgrade before reporting: the issue may already be
fixed. Fixes ship as a new patch release and are noted in the release notes.

## Reporting a vulnerability

**Do not open a public issue for a vulnerability.** It would be visible to everyone,
including whoever would abuse it, before a fix exists.

Report privately through **GitHub Security Advisories**:

<https://github.com/ManiTheFerfri/darkob/security/advisories/new>

The channel is private between you and the maintainer, Mani Keikhosravi, until an
advisory is published.

Please include:

- **Affected version** — from `python -c "import darkob; print(darkob.__version__)"`,
  plus the Python version and platform if relevant.
- **A minimal reproduction** — the shortest script that shows the problem, with real
  tokens and session strings replaced by obviously fake values.
- **Impact assessment** — what an attacker gains. Token disclosure, code execution,
  SSRF and denial of service are different severities, and this drives the response.
- **Any suggested fix** — the module at fault, or a patch or failing test. All optional.

## Response timeline

- **Acknowledgement** within **3 business days**.
- **Initial assessment** (severity, affected versions, plan) within **7 days**.
- **Coordinated disclosure** aim of **90 days** from the report; if a fix needs longer
  you will be told why. Credit is given in the advisory unless you ask otherwise.

## Scope

In scope — issues in darkob itself:

- **Token or session leakage**: a bot token or `Messenger` session string in logs,
  exception messages, `repr()` output, or error payloads that reach the server.
- **Unsafe deserialisation of server payloads**: anything that lets a crafted API
  response execute code or corrupt state instead of being validated.
- **Path traversal in file download filenames**: a server-supplied filename that
  escapes the download directory or overwrites an arbitrary path.
- **Credential handling in `Messenger` / `Shad` DC auth**: mishandling the passphrase,
  key derivation, session import/export, or the auth handshake.
- **Dependency vulnerabilities** in `aiohttp`, `pycryptodome`, or any dependency pulled
  in by an optional extra.

Out of scope: the Rubika and Shad servers themselves. darkob is a client library, so
server behaviour, account bans and platform API weaknesses belong to the platform —
report them there. Also out of scope: anything that needs the attacker to already
control the user's machine or dependency tree, and docs-site header nits.

## Protecting your own tokens

- **Never commit a token or a session string** — not in a script, not in a test, not in
  a notebook you push. Read them from the environment at runtime:

  ```python
  import os

  from darkob import Bot

  bot = Bot(token=os.environ["DARKOB_BOT_TOKEN"])
  ```

- **A `Messenger` session string is equivalent to a password**: anyone who has it can
  act as that account until it is revoked. Never paste one into issues or screenshots.
- If a token does leak, revoke it through the platform immediately and rotate.

## Security practices

- **`pip-audit` in CI** on every push and PR, surfacing dependency advisories in the
  build log (reported, not blocking, so an upstream advisory cannot freeze the repo).
- **Static analysis** with ruff in CI plus bandit-style checks (`eval`/`exec`, shell
  use, unsafe deserialisation, hard-coded secrets) on code that parses remote data.
- **No `eval` or `exec` of remote data.** Server payloads are parsed as data, never run
  as code, and no `pickle`/`yaml.load` path accepts untrusted input.
- **Pinned minimum dependency versions** (`aiohttp>=3.9`, `pycryptodome>=3.20`) so an
  install cannot resolve to a release known to be vulnerable.
- **TLS verification is on by default**; opting out is an explicit argument.
