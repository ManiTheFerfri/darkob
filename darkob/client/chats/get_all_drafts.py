import darkob

class GetAllDrafts:
    async def get_all_drafts(self: "darkob.Client"):
        """
        Get all saved message drafts.

        Returns:
            The result of the API call containing all drafts.
        """
        return await self.request(method = 'getAllDrafts')