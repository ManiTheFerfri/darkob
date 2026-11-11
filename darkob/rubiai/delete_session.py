from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class DeleteSession:
    async def delete_session(
        self: "darkob.RubiAI",
        session_id: str
    ):
        """
        Delete an AI chat session.

        Parameters:
            session_id (str): Identifier of the session to delete.

        Returns:
            The API response.
        """
        return await self.request(
            method="deleteSession",
            input={"session_id": session_id}
        )