from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetAvailableReactions:
    async def get_available_reactions(self: "darkob.Messenger"):
        """
        Retrieve the list of available message reactions that can be used in chats.

        Returns:
            Shows available reactions data from the server.
        """
        return await self.request(method='getAvailableReactions')