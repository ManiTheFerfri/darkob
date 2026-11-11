from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetContactsStories:
    async def get_contacts_stories(self: "darkob.Messenger"):
        """
        Get stories from contacts in the chat page.

        Returns:
            The result of the API call containing contacts stories.
        """
        return await self.request(method='getStories')