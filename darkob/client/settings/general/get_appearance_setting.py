from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetAppearanceSetting:
    async def get_appearance_setting(self: "darkob.Messenger"):
        """
        Get the user's appearance settings (chat background, font size, emoji, night mode, themes, etc.).

        Returns:
            The result of the API call, containing the `appearance_setting` object.
        """
        return await self.request(method='getAppearanceSetting')