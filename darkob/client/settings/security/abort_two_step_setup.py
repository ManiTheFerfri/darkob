from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class AbortTwoStepSetup:
    async def abort_two_step_setup(self: "darkob.Messenger"):
        """
        Abort the two-step verification setup process.

        Returns:
            The result of the operation.
        """
        return await self.request(method='abortTwoStepSetup')