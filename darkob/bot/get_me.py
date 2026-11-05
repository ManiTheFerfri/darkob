import darkob

class GetMe:
    async def get_me(self: "darkob.Bot", refresh: bool = False):
        """
        Get information about the authenticated bot.

        The result is cached for the lifetime of the bot, because a bot's
        identity does not change. Pass ``refresh=True`` to force a new
        request.

        Parameters:
            refresh (bool): Ignore the cache and re-fetch. Defaults to False.

        Returns:
            Information about the authenticated bot.
        """
        if not refresh and getattr(self, '_me_cache', None) is not None:
            return self._me_cache

        result = await self.request('POST', 'getMe', json={})
        self._me_cache = result
        return result
