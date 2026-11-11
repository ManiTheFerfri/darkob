from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class TerminateOtherSessions:
    async def terminate_other_sessions(self: "darkob.Messenger"):
        """
        Terminate other account sessions.

        Returns:
            The result of the API call.
        """
        return await self.request(method='terminateOtherSessions')