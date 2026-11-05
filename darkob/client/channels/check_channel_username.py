import darkob

class CheckChannelUsername:
    async def check_channel_username(self: "darkob.Client", username: str):
        """
        Check the availability of a username for a channel.

        Parameters:
            username (str): The username to check.

        Returns:
            The result of the API call.
        """
        return await self.request(
            method = 'checkChannelUsername',
            input = {'username': username.replace('@', '')}
        )