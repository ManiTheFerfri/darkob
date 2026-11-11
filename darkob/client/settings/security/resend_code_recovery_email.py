from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class ResendCodeRecoveryEmail:
    async def resend_code_recovery_email(
        self: "darkob.Messenger",
        password: str
    ):
        """
        Resend the recovery email verification code.

        Parameters:
            password (str): The two-step verification password.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method='resendCodeRecoveryEmail',
            input={'password': password}
        )