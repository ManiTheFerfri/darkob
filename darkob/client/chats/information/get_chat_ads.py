from time import time as time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetChatAds:
    async def get_chat_ads(
        self: "darkob.Messenger",
        state: int = None
    ):
        """
        Retrieves advertising information for chats.

        Parameters:
            state (int, optional): The timestamp state to filter chat ads. Defaults to the current time minus 150 seconds.

        Returns:
            The result of the API call.
        """
        if state is None:
            state = round(time()) - 150
        return await self.request(method='getChatAds', input={'state': int(state)})