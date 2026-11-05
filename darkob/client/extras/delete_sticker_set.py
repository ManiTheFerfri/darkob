import darkob

class DeleteStickerSet:
    async def delete_sticker_set(
        self: "darkob.Client",
        sticker_set_id: str
    ):
        """
        Delete a sticker set.

        Parameters:
            sticker_set_id (str): The ID of the sticker set.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'actionOnStickerSet',
            input = {'sticker_set_id': sticker_set_id, 'action': 'Remove'})