import darkob

class GetMyGuid:
    async def get_my_guid(self: "darkob.Client"):
        """
        Get the GUID of the currently authenticated user.

        Returns:
            str: The user's GUID.
        """
        return self.guid