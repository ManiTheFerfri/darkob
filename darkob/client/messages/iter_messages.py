"""Stream messages from a chat instead of buffering the whole history.

``get_chat_messages`` already paginates internally, but it collects every
message into a list before returning. For a large chat that is megabytes
of objects in memory. ``iter_messages`` walks the same pages and yields
one message at a time.
"""

from __future__ import annotations

from typing import AsyncIterator, Optional

import darkob
from ...data import Data
from ..exceptions import InvalidInput

FILTER_TYPES = {'Voice', 'File', 'Music', 'Gif', 'Media', 'Link'}


class IterMessages:
    async def iter_messages(
        self: "darkob.Client",
        chat: str,
        *,
        sort: str = 'FromMin',
        filter_type: Optional[str] = None,
        page_size: int = 25,
        max_items: Optional[int] = None,
    ) -> AsyncIterator[Data]:
        """Yield messages from *chat*, one page at a time.

        Parameters:
            chat (str): Chat GUID, link or username.
            sort (str): 'FromMin' (oldest first) or 'FromMax' (newest first).
            filter_type (str, optional): 'Voice', 'File', 'Music', 'Gif',
                'Media' or 'Link'.
            page_size (int): Messages requested per round-trip.
            max_items (int, optional): Stop after this many messages.

        Yields:
            Each message as a :class:`~darkob.data.Data` object.
        """
        sort_lower = sort.lower()
        if sort_lower == 'frommax':
            sort = 'FromMax'
        elif sort_lower == 'frommin':
            sort = 'FromMin'
        else:
            raise InvalidInput(
                f"Invalid sort: '{sort}'. Must be 'FromMax' or 'FromMin'."
            )

        if filter_type is not None:
            match = next(
                (ft for ft in FILTER_TYPES if ft.lower() == filter_type.lower()),
                None,
            )
            if match is None:
                raise InvalidInput(
                    f"Invalid filter_type: '{filter_type}'. Must be one of: "
                    f"{', '.join(sorted(FILTER_TYPES))}"
                )
            filter_type = match

        if page_size <= 0:
            raise InvalidInput("'page_size' must be greater than 0.")

        chat_guid = await self.get_guid(chat)

        current_id: Optional[str] = None
        seen: set = set()
        yielded = 0

        while True:
            payload: dict = {
                'object_guid': chat_guid,
                'sort': sort,
                'limit': page_size,
            }
            if current_id is not None:
                payload['max_id' if sort == 'FromMax' else 'min_id'] = current_id
            if filter_type is not None:
                payload['filter_type'] = filter_type

            result = await self.request(method='getMessages', input=payload)
            data = result.to_dict() if hasattr(result, 'to_dict') else result

            messages = data.get('messages') or []
            if not messages:
                return

            for message in messages:
                payload_message = (
                    message.to_dict() if hasattr(message, 'to_dict') else message
                )
                message_id = payload_message.get('message_id')

                if message_id in seen:
                    continue
                seen.add(message_id)

                yield Data(payload_message)
                yielded += 1

                if max_items is not None and yielded >= max_items:
                    return

            if not data.get('has_continue', True):
                return

            next_id = data.get('new_max_id' if sort == 'FromMax' else 'new_min_id')
            if not next_id or str(next_id) == current_id:
                return
            current_id = str(next_id)
