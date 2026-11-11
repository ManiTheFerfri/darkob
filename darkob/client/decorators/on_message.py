from typing import TYPE_CHECKING

from ..core import handlers
from ..filters import Filter

if TYPE_CHECKING:
    import darkob

class OnMessage:
    def on_message(self: "darkob.Messenger", *filters: Filter):
        """Decorator for message updates with optional filters."""
        def MetaHandler(func):
            handler = handlers.MessageUpdates(*filters)
            self.add_handler(func, handler)
            return func
        return MetaHandler