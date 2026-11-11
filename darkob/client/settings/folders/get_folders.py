from typing import Union, TYPE_CHECKING
from time import time

if TYPE_CHECKING:
    import darkob

class GetFolders:
    async def get_folders(
        self: "darkob.Messenger",
        last_state: Union[int, str] = None
    ):
        """
        Get a list of folders.

        Parameters:
            last_state (Union[int, str]): The last state to retrieve folders.

        Returns:
            List of folders.
        """
        if last_state is None:
            last_state = round(time()) - 150
        return await self.request(method='getFolders', input={'last_state': int(last_state)})