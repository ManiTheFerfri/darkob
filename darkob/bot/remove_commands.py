import darkob


class RemoveCommands:
    async def remove_commands(self: "darkob.Bot"):
        """
        Remove every custom command previously registered for this bot.

        The Bot API exposes this as ``setCommands`` with an empty
        ``bot_commands`` list, which is what this calls.

        Returns:
            The API response.
        """
        return await self.request('POST', 'setCommands', json={'bot_commands': []})
