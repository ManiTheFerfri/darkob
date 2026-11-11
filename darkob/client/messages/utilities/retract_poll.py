from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class RetractPoll:
    async def retract_poll(
        self: "darkob.Messenger",
        poll_id: str
    ):
        """
        Retract a poll.

        Parameters:
            poll_id (str): The ID of the poll to retract.

        Returns:
            The result of the API call.
        """
        input_data = {
            'poll_id': poll_id,
            'action': 'Retract'
        }

        return await self.request(
            method='setPollAction',
            input=input_data
        )