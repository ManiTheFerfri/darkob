from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetCustomMenuItems:
    async def get_custom_menu_items(
        self: "darkob.RubikaTV"
    ):
        """
        Retrieve custom menu items.

        Returns:
            The API output.
        """
        return await self.request(method="getCustomMenuItems")