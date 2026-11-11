from time import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetMessagesUpdates:
    async def get_messages_updates(
        self: "darkob.Messenger",
        chat: str,
        state: int = None
    ):
        """
        Get message updates for a specific chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat for which updates are requested.
            state (int): The state at which updates are requested. Defaults to a timestamp approximately 150 seconds ago.

        Returns:
            The message updates for the specified chat.
        """
        if state is None:
            state = round(time()) - 150
        chat_guid = await self.get_guid(chat)

        input_data = {
            'object_guid': chat_guid,
            'state': state
        }

        return await self.request(method='getMessagesUpdates', input=input_data)