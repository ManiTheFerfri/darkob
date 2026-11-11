from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class EditSlowMode:
    async def edit_slow_mode(
        self: "darkob.Messenger",
        group: str,
        slow_mode: Union[str, int]
    ):
        """
        Parameters:
            group (str): The GUID or link of the group.
            slow_mode (Union[str, int]): The new slow mode setting for the group.

        Returns:
            The result of the API call.
        """
        return await self.edit_group_info(group=group, slow_mode=slow_mode)