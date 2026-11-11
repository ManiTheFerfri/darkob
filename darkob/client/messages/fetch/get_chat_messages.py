from typing import Optional, Literal, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

FILTER_TYPE_MAP = {
    'voice': 'Voice',
    'file': 'File',
    'music': 'Music',
    'gif': 'Gif',
    'media': 'Media',
    'link': 'Link'
}

VALID_FILTER_TYPES = {
    'Voice', 'File', 'Music', 'Gif', 'Media', 'Link'
}

class GetChatMessages:
    async def get_chat_messages(
        self: "darkob.Messenger",
        chat: str,
        max_id: Optional[Union[str, int]] = None,
        sort: Literal['FromMax', 'FromMin'] = 'FromMin',
        filter_type: Optional[Literal[
            'Voice', 'File', 'Music', 'Gif', 'Media', 'Link'
        ]] = None,
        limit: Optional[int] = None,
        all_pages: bool = False,
        min_id: Optional[Union[str, int]] = None,
        middle_message_id: Optional[Union[str, int]] = None,
    ):
        """
        Get messages from a chat with filtering and pagination.

        Parameters:
            chat (str): The GUID, link, or username of the chat.
            max_id (Union[str, int], optional): Maximum message ID. Retained
                as the second positional parameter for pre-1.18 callers.
            sort (Literal['FromMax', 'FromMin']): Sort direction. Default is 'FromMin'.
            filter_type (Literal, optional): Filter messages by type:
                'Voice', 'File', 'Music', 'Gif', 'Media', 'Link'.
            limit (int, optional): Maximum number of messages to retrieve.
            all_pages (bool): If True, fetch all pages (ignores `limit`). Default is False.
            min_id (Union[str, int], optional): Minimum message ID (new in 1.18).
            middle_message_id (Union[str, int], optional): Start from this message ID (new in 1.18).

        Returns:
            The result containing messages, count, and pagination info.
        """
        from ....data import Data
        from ...exceptions import InvalidInput

        if max_id in ('FromMax', 'FromMin'):
            # Also tolerate upstream's new positional form. The second value
            # is a direction rather than a numeric message ID, so the two
            # conventions are distinguishable without guessing GUIDs.
            upstream_sort = max_id
            if isinstance(filter_type, bool):
                max_id, sort, filter_type, limit, all_pages, min_id, middle_message_id = (
                    all_pages, upstream_sort, sort, limit, filter_type,
                    middle_message_id, limit,
                )
            else:
                max_id, sort = None, upstream_sort

        chat_guid = await self.get_guid(chat)

        sort_map = {'frommax': 'FromMax', 'frommin': 'FromMin'}
        sort = sort_map.get(sort.lower())

        if not sort:
            raise InvalidInput("'sort' must be 'FromMax' or 'FromMin'.")

        if filter_type is not None:
            filter_type = FILTER_TYPE_MAP.get(filter_type.lower())
            if not filter_type:
                message = f"Invalid filter_type. Must be one of: {', '.join(sorted(VALID_FILTER_TYPES))}"
                raise InvalidInput(message)

        current_id = None
        if middle_message_id is not None:
            current_id = str(middle_message_id)
        elif sort == 'FromMax' and max_id is not None:
            current_id = str(max_id)
        elif sort == 'FromMin' and min_id is not None:
            current_id = str(min_id)

        effective_limit = None if all_pages else limit

        all_messages = []
        message_ids = set()

        while True:
            input_data = {
                'object_guid': chat_guid,
                'sort': sort,
                'limit': 25
            }

            if current_id is not None:
                if sort == 'FromMax':
                    input_data['max_id'] = current_id
                else:
                    input_data['min_id'] = current_id

            if filter_type is not None:
                input_data['filter_type'] = filter_type

            result = await self.request(method='getMessages', input=input_data)

            if isinstance(result, dict):
                result = Data(result)

            messages = result.find_keys('messages')

            if not messages:
                break

            for msg in messages:
                if isinstance(msg, dict):
                    msg = Data(msg)

                msg_id = msg.find_keys('message_id')
                if msg_id and int(msg_id) not in message_ids:
                    message_ids.add(int(msg_id))
                    all_messages.append(msg.to_dict())

                    if effective_limit is not None and len(all_messages) >= effective_limit:
                        break

            if effective_limit is not None and len(all_messages) >= effective_limit:
                break

            has_continue = result.find_keys('has_continue')
            if has_continue is False:
                break

            if sort == 'FromMax':
                next_id = result.find_keys('new_max_id')
            else:
                next_id = result.find_keys('new_min_id')

            if not next_id or str(next_id) == current_id:
                break

            current_id = str(next_id)

            if not all_pages:
                break

        result_dict = {
            "messages": all_messages[:effective_limit] if effective_limit else all_messages,
            "count": len(all_messages[:effective_limit]) if effective_limit else len(all_messages),
            "chat_guid": chat_guid
        }

        if all_messages:
            if sort == 'FromMax':
                result_dict["first_message_id"] = str(all_messages[-1].get('message_id', ''))
                result_dict["last_message_id"] = str(all_messages[0].get('message_id', ''))
            else:
                result_dict["first_message_id"] = str(all_messages[0].get('message_id', ''))
                result_dict["last_message_id"] = str(all_messages[-1].get('message_id', ''))

        if filter_type is not None:
            result_dict["filter_type"] = filter_type

        if getattr(self, 'as_dict', False):
            return result_dict

        return Data(result_dict)