from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetDataSetting:
    async def get_data_setting(self: "darkob.Messenger"):
        """
        Get the user's data and media auto-download settings.

        Returns:
            The result of the API call, containing the `data_setting` object.
        """
        return await self.request(method='getDataSetting')