from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class Connect:
    async def connect(self: "darkob.Messenger") -> "darkob.Messenger":
        """
        Establish a connection to the Rubika API.

        Creates an Api instance and loads stored session information
        (auth, guid, private_key, user_agent) if available.

        Returns:
            Messenger instance with active connection.
        """
        from ..core.api import Api

        self.connection = Api(client=self)

        information = self.session.information()
        # Do not log this tuple: it contains auth and private_key as well as
        # identifying user data. Recording whether any credentials were used
        # is enough for operators to diagnose session problems.
        if information:
            self.logger.debug('Credentials restored from the stored session.')
        else:
            self.logger.debug('No stored credentials were found for this session.')

        if information:
            self.auth = information[1]
            self.guid = information[2]
            self.private_key = information[4]

            if isinstance(information[3], str):
                self.user_agent = information[3] or self.user_agent

        return self