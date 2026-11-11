from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetMyGuid:
    async def get_my_guid(self: "darkob.Messenger") -> str:
        """
        Get the GUID of the currently authenticated user.

        Returns:
            str: The user's GUID.
        """
        return self.guid