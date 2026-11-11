from .actions import Actions
from .fetch import Fetch
from .iter_messages import IterMessages
from .send import Send
from .utilities import Utilities


class Messages(
    Actions,
    Fetch,
    Send,
    Utilities,
    IterMessages,
):
    """Message API, grouped upstream with darkob's streaming iterator kept."""
