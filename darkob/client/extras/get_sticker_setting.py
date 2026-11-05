import darkob

class GetStickerSetting:
    async def get_sticker_setting(self: "darkob.Client"):
        """
        Get the sticker settings of the current user.

        Returns:
            The result of the API call containing sticker settings.
        """
        return await self.request(method = 'getStickerSetting')