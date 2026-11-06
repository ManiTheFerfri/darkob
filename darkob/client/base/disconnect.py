from .. import exceptions
import darkob
import asyncio
import logging

logger = logging.getLogger(__name__)

class Disconnect:
    async def close(self: "darkob.Client") -> None:
        """
        Close the connection to the Darkob server (async version).
        """
        try:
            if self.connection is not None:
                await self.connection.close()
                self.logger.info('The client was disconnected.')
        except AttributeError:
            raise exceptions.NoConnection(
                'You must first connect the Client'
                ' with the *.connect() method'
            )
        except Exception as e:
            try:
                self.logger.debug(f'Error during disconnect: {e}')
            except Exception:
                logger.debug("Suppressed exception", exc_info=True)

    def disconnect(self: "darkob.Client") -> None:
        """
        Disconnect from the Darkob server (sync version).
        """
        if self.connection is None:
            return

        result = self.close()

        if asyncio.iscoroutine(result):
            try:
                asyncio.get_running_loop().create_task(result)
            except RuntimeError:
                result.close()