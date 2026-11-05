import darkob

class GetMyStickerSets:
    async def get_my_sticker_sets(self: "darkob.Client"):
        """
        Get the sticker sets owned by the user.

        Returns:
            The sticker sets owned by the user.
        """
        return await self.request(method = 'getMyStickerSets')