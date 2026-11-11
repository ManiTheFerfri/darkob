from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class GetNextEpisode:
    async def get_next_episode(
        self: "darkob.RubikaTV",
        episode_id: str
    ):
        """
        Retrieve the next episode after the given episode.

        Parameters:
            episode_id (str): Identifier of the current episode.

        Returns:
            The API output.
        """
        return await self.request(
            method="getNextEpisode",
            input={"episode_id": episode_id}
        )