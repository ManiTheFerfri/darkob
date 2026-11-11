from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class ClearAllDrafts:
    async def clear_all_drafts(self: "darkob.Messenger"):
        """
        Clear all drafts.

        Returns:
            The result of the API call.
        """
        return await self.request(method='clearDrafts', input={'action': 'All'})