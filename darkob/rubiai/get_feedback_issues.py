from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetFeedbackIssues:
    async def get_feedback_issues(
        self: "darkob.RubiAI"
    ):
        """
        Retrieve available feedback issue types.

        Returns:
            Parsed feedback-issues response.
        """
        return await self.request(method="getFeedbackIssues")