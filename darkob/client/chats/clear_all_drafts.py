import darkob

class ClearAllDrafts:
    async def clear_all_drafts(self: "darkob.Client"):
        """
        Clear all drafts.

        Returns:
            The result of the API call.
        """
        return await self.request(method = 'clearDrafts', input = {'action': 'All'})