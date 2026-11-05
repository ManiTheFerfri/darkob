import darkob

class UnarchiveChat:
    async def unarchive_chat(self: "darkob.Client", chat: str):
        """
        Unarchive a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat to unarchive.

        Returns:
            Result of the operation.
        """
        chat_guid = await self.get_guid(chat)

        return await self.request(
            method = 'setActionChat',
            input = {'object_guid': chat_guid, 'action': 'UnArchive'}
        )