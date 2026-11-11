from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetSuggestedFolders:
    async def get_suggested_folders(self: "darkob.Messenger"):
        """
        Get the suggested folders for the user.

        Returns:
            The suggested folders for the user.
        """
        return await self.request(method='getSuggestedFolders')