from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetCallConfig:
    async def get_call_config(self: "darkob.Messenger"):
        """
        Get the voice call configuration (WebRTC technical settings).

        Returns:
            The result of the API call, containing the `call_config` object.
        """
        return await self.request(method='getCallConfig')