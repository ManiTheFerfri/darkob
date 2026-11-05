from time import time
from typing import Optional, Union
import darkob

class GetContactsUpdates:
    async def get_contacts_updates(
        self: "darkob.Client",
        state: Optional[Union[str, int]] = round(time()) - 150
    ):
        """
        Get updates related to contacts.

        Parameters:
            state (Optional[Union[str, int]], optional):
                The state parameter to filter updates. Defaults to `round(time()) - 150`.

        Returns:
            The update related to contacts.
        """
        return await self.request(method = 'getContactsUpdates', input = {'state': int(state)})