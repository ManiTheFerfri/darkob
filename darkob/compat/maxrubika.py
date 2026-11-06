"""Compatibility surface for projects migrating from `maxrubika`.

Changing one import is the whole migration::

    # before
    from maxrubika import Messenger

    # after
    from darkob.compat.maxrubika import Messenger

Everything maxrubika exported is re-exported here, unchanged. Names that
only exist in darkob are available too, so a half-migrated file still
works.
"""

from __future__ import annotations

import warnings
from typing import Any

import darkob as _darkob
from darkob import *  # noqa: F401,F403
from darkob import __all__ as _darkob_exports

__all__ = list(_darkob_exports)

#: maxrubika's own last version, kept so version checks keep working.
__maxrubika_version__ = "1.17.0"

warnings.warn(
    "darkob.compat.maxrubika is a migration shim. Import from 'darkob' "
    "directly; this module is for running existing maxrubika code as-is.",
    DeprecationWarning,
    stacklevel=2,
)


def __getattr__(name: str) -> Any:
    """Proxy anything else to darkob, so partial migrations keep working."""
    try:
        return getattr(_darkob, name)
    except AttributeError:
        raise AttributeError(
            f"Neither maxrubika nor darkob exposes {name!r}."
        ) from None

#: The version actually in use (darkob's, not maxrubika's).
__version__ = _darkob.__version__
