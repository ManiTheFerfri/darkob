import darkob

class GetNotificationSetting:
    async def get_notification_setting(self: "darkob.Client"):
        """
        Retrieves the current notification settings for the account.

        Returns:
            The result of the API call.
        """
        return await self.request(method = 'getNotificationSetting')