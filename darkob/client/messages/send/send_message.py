from typing import Optional, Union, TYPE_CHECKING
import random
import time as time_module
from datetime import timedelta, datetime

from ....data import Data

if TYPE_CHECKING:
    import darkob


class SendMessage:
    async def send_message(
        self: "darkob.Messenger",
        chat: str,
        text: Optional[str] = None,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        file_inline=None,
        base64_data: Optional[str] = None,
        sticker=None,
        type: str = 'File',
        is_spoil: bool = False,
        thumb=None,
        audio_info: bool = True,
        metadata: Optional[dict] = None,
        performer: Optional[str] = None,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[str] = None,
        is_mute: bool = False,
        **kwargs,
    ):
        """Send text, an uploaded file or a sticker.

        The long parameter list is intentional compatibility: 1.18 moved file
        arguments into ``send_file`` and removed them from this method. Keep
        the original positional layout instead of silently misrouting callers.
        Keyword-only use of upstream's ``metadata`` and ``is_mute`` is
        supported as before.
        """
        if sticker is not None:
            return await self._send_raw_sticker(
                chat, sticker, reply_to_message_id, via_bot,
                schedule_time, schedule_type, is_mute,
            )

        if text is not None and (
            file_inline is None and base64_data is None
        ) or (
            metadata is not None
            and file_inline is None
            and base64_data is None
        ):
            return await self._send_text_message(
                chat=chat,
                text=text,
                reply_to_message_id=reply_to_message_id,
                via_bot=via_bot,
                metadata=metadata,
                is_mute=is_mute,
                schedule_time=schedule_time,
                schedule_type=schedule_type,
            )

        if file_inline is not None or base64_data is not None:
            return await self.send_file(
                chat=chat,
                file_inline=(
                    file_inline
                    if isinstance(file_inline, (dict, Data))
                    else None
                ),
                file=(
                    None if isinstance(file_inline, (dict, Data))
                    else file_inline
                ),
                base64=base64_data,
                text=text,
                type=type,
                is_spoil=is_spoil,
                thumb=thumb,
                audio_info=audio_info,
                performer=performer,
                reply_to_message_id=reply_to_message_id,
                via_bot=via_bot,
                is_mute=is_mute,
                metadata=metadata,
                schedule_time=schedule_time,
                schedule_type=schedule_type,
                **kwargs,
            )

        # No text and no file: let the text path produce its normal validation
        # error rather than an opaque missing-argument TypeError.
        return await self._send_text_message(
            chat=chat,
            text=text,
            reply_to_message_id=reply_to_message_id,
            via_bot=via_bot,
            metadata=metadata,
            is_mute=is_mute,
            schedule_time=schedule_time,
            schedule_type=schedule_type,
        )

    async def _send_raw_sticker(
        self, chat, sticker, reply_to_message_id, via_bot,
        schedule_time, schedule_type, is_mute,
    ):
        """Send the pre-1.18 raw sticker payload without losing fields."""
        from ...exceptions import InvalidInput

        if isinstance(sticker, Data):
            sticker = sticker.original_data
        if not isinstance(sticker, dict):
            raise InvalidInput("'sticker' must be a dict or Data object.")

        chat_guid = (
            self.guid
            if chat.lower() in ('me', 'cloud', 'self', 'myself')
            else await self.get_guid(chat)
        )
        input_data = {
            'object_guid': chat_guid,
            'reply_to_message_id': reply_to_message_id,
            'rnd': random.randint(100000, 999999),
            'sticker': sticker,
        }
        if is_mute:
            input_data['is_mute'] = True

        if schedule_time is not None:
            if isinstance(schedule_time, timedelta):
                schedule_time = int(time_module.time() + schedule_time.total_seconds())
            elif isinstance(schedule_time, datetime):
                schedule_time = int(schedule_time.timestamp())
            elif isinstance(schedule_time, (int, float)):
                if schedule_time < 1000000000:
                    schedule_time = int(time_module.time() + schedule_time)
                else:
                    schedule_time = int(schedule_time)
            else:
                raise InvalidInput("Invalid schedule_time type.")
            if schedule_time <= time_module.time():
                raise InvalidInput("'schedule_time' must be in the future.")
            input_data.update(
                is_scheduled=True,
                schedule_type='Default',
                scheduled_time=schedule_time,
            )
        elif schedule_type == 'WhenOnline':
            if not chat_guid.startswith('u0'):
                raise InvalidInput(
                    "'schedule_type=WhenOnline' is only available for user chats."
                )
            input_data.update(is_scheduled=True, schedule_type='WhenOnline')
        elif schedule_type == 'Default':
            raise InvalidInput("'schedule_type=Default' requires 'schedule_time'.")

        if via_bot is not None:
            bot_guid = await self.get_guid(via_bot)
            if not bot_guid.startswith('b0'):
                raise InvalidInput("'via_bot' must be a bot GUID or username.")
            input_data['via_bot_guid'] = bot_guid

        return await self.request(method='sendMessage', input=input_data)

    async def _send_text_message(
        self: "darkob.Messenger",
        chat: str,
        text: str,
        reply_to_message_id: Optional[Union[str, int]] = None,
        via_bot: Optional[str] = None,
        metadata: Optional[dict] = None,
        is_mute: bool = False,
        schedule_time: Optional[Union[int, float, timedelta, datetime]] = None,
        schedule_type: Optional[str] = None
    ):
        """
        Send a text message to a chat.

        Parameters:
            chat (str): The GUID, link, or username of the chat, or 'me'/'cloud'/'self'/'myself'.
            text (str): The text content of the message (Max: 4096 chars, 128 lines).
            reply_to_message_id (Union[str, int], optional): The ID of the message to reply to.
            via_bot (str, optional): Bot GUID or username to send the message via.
            metadata (dict, optional): Additional metadata for text formatting.
            is_mute (bool): If True, the message will be sent silently without notification. Defaults to False.
            schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
            schedule_type (str, optional): 'Default' or 'WhenOnline'.

        Returns:
            The result of the API call.
        """
        from ...core import to_metadata
        from ...exceptions import InvalidInput, MessageTooLong

        if not isinstance(text, str) or not text.strip():
            raise InvalidInput("'text' must be a non-empty string.")

        if len(text) > 4096:
            message = f"Text is too long ({len(text)} characters). Maximum allowed is 4096."
            raise MessageTooLong(message)

        if text.count('\n') > 128:
            message = f"Text has too many lines ({text.count(chr(10))}). Maximum allowed is 128."
            raise MessageTooLong(message)

        if chat.lower() in ('me', 'cloud', 'self', 'myself'):
            chat_guid = self.guid
        else:
            chat_guid = await self.get_guid(chat)

        input_data = {
            'object_guid': chat_guid,
            'reply_to_message_id': reply_to_message_id,
            'rnd': random.randint(100000, 999999)
        }
        if is_mute:
            input_data['is_mute'] = True

        if schedule_time is not None:
            if isinstance(schedule_time, timedelta):
                schedule_time = int(time_module.time() + schedule_time.total_seconds())
            elif isinstance(schedule_time, datetime):
                schedule_time = int(schedule_time.timestamp())
            elif isinstance(schedule_time, (int, float)):
                if schedule_time < 1000000000:
                    schedule_time = int(time_module.time() + schedule_time)
                else:
                    schedule_time = int(schedule_time)
            else:
                message = f"Invalid schedule_time type: {type(schedule_time).__name__}"
                raise InvalidInput(message)

            if schedule_time <= time_module.time():
                raise InvalidInput("'schedule_time' must be in the future.")

            input_data['is_scheduled'] = True
            input_data['schedule_type'] = 'Default'
            input_data['scheduled_time'] = schedule_time

        elif schedule_type is not None:
            if schedule_type == 'WhenOnline':
                if not chat_guid.startswith('u0'):
                    raise InvalidInput("'schedule_type=WhenOnline' is only available for user chats.")
                input_data['is_scheduled'] = True
                input_data['schedule_type'] = 'WhenOnline'
            elif schedule_type == 'Default':
                raise InvalidInput("'schedule_type=Default' requires 'schedule_time'.")

        if via_bot is not None:
            bot_guid = await self.get_guid(via_bot)
            if not bot_guid.startswith('b0'):
                message = f"'{via_bot}' does not point to a valid bot. Expected a bot GUID or bot username."
                raise InvalidInput(message)
            input_data['via_bot_guid'] = bot_guid

        processed_text = text
        if not metadata:
            try:
                processed = to_metadata(text)
                processed_text = processed['text']
                metadata = processed.get('metadata')
            except Exception:
                processed_text = text
                metadata = None

        input_data['text'] = processed_text.strip()

        if metadata:
            if 'metadata' in metadata:
                input_data.update(metadata)
            else:
                input_data['metadata'] = metadata

        return await self.request(method='sendMessage', input=input_data)