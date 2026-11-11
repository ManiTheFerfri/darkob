from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class RequestForgetPassword:
    async def request_forget_password(self: "darkob.Messenger"):
        """
        Request to reset the account password.

        Returns:
            The result of the API call.
        """
        return await self.request(method='requestForgetPassword')