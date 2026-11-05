import inspect
import darkob
from ..core import handlers
from ..filters import Filter

class OnCallUpdate:
    def on_call_update(self: "darkob.Client", *filters: Filter):
        """Decorator for call updates."""
        def MetaHandler(func):
            async def wrapper(event):
                for f in filters:
                    if hasattr(f, 'evaluate'):
                        if not await f.evaluate(event):
                            return

                result = func(event)
                if inspect.isawaitable(result):
                    result = await result
                return result

            self.add_handler(wrapper, handlers.CallUpdates())
            return func
        return MetaHandler