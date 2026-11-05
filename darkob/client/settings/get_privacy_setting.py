import darkob

class GetPrivacySetting:
    async def get_privacy_setting(self: "darkob.Client"):
        """
        Get the current user's privacy setting.

        Returns:
            The current user's privacy setting.
        """
        return await self.request(method = 'getPrivacySetting')