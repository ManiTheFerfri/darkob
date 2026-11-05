import time

import darkob
from ...data import Data

class GetMe:
    async def get_me(self: "darkob.Client", refresh: bool = False,
                     ttl: float = 300.0):
        """
        Get information about the authenticated user.

        The result is cached for ``ttl`` seconds (default 5 minutes),
        because profile reads are frequent and rarely change. Pass
        ``refresh=True`` to force a new request.

        Parameters:
            refresh (bool): Ignore the cache. Defaults to False.
            ttl (float): Cache lifetime in seconds. Defaults to 300.

        Returns:
            Information about the authenticated user.
        """
        cached = getattr(self, '_me_cache', None)
        cached_at = getattr(self, '_me_cached_at', 0.0)
        if (
            not refresh
            and cached is not None
            and (time.time() - cached_at) < ttl
        ):
            return cached

        result = await self.get_user_info()

        data = result.to_dict() if hasattr(result, 'to_dict') else result

        if hasattr(self, 'auth') and self.auth:
            data['auth'] = self.auth

        if hasattr(self, 'private_key') and self.private_key:
            data['private_key'] = self.private_key

        payload = Data(data)
        self._me_cache = payload
        self._me_cached_at = time.time()
        return payload
