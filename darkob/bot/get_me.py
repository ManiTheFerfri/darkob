import darkob

class GetMe:
    async def get_me(self: "darkob.Bot"):
        """
        Get information about the authenticated bot.

        Returns:
            dict: Information about the authenticated bot.
        """
        return await self.request('POST', 'getMe', json = {})