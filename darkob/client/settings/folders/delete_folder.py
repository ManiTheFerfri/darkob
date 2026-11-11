from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class DeleteFolder:
    async def delete_folder(
        self: "darkob.Messenger",
        folder_id: str
    ):
        """
        Delete a folder.

        Parameters:
            folder_id (str): The ID of the folder to be deleted.

        Returns:
            Result of the delete folder operation.
        """
        return await self.request(method='deleteFolder', input={'folder_id': folder_id})