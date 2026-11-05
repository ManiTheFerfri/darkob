import darkob

class AbortTwoStepSetup:
    async def abort_two_step_setup(self: "darkob.Client"):
        """
        Abort the two-step verification setup process.

        Returns:
            The result of the operation.
        """
        return await self.request(method = 'abortTwoStepSetup')