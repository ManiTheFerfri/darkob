import darkob

class GetSuggestedFolders:
    async def get_suggested_folders(self: "darkob.Client"):
        """
        Get the suggested folders for the user.

        Returns:
            The suggested folders for the user.
        """
        return await self.request(method = 'getSuggestedFolders')