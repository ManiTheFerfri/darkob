# Bot API reference

The official Rubika Bot API. Token based, plain HTTP JSON.

> Generated from the installed package by `scripts/generate_docs_assets.py`. Every signature below is real; do not hand-edit this file.

**51 public methods.**

## Method index

- **core** (1): [`include_router`](#include-router)
- **bot** (50): [`ask`](#ask), [`auto_delete_message`](#auto-delete-message), [`ban_member`](#ban-member), [`check_join`](#check-join), [`close`](#close), [`delete`](#delete), [`delete_message`](#delete-message), [`delete_messages`](#delete-messages), [`disconnect`](#disconnect), [`download_file`](#download-file), [`edit`](#edit), [`edit_chat_keypad`](#edit-chat-keypad), [`edit_inline_keypad`](#edit-inline-keypad), [`edit_message`](#edit-message), [`forward_message`](#forward-message), [`forward_messages`](#forward-messages), [`get_chat_info`](#get-chat-info), [`get_chat_member`](#get-chat-member), [`get_file`](#get-file), [`get_me`](#get-me), [`get_token_string`](#get-token-string), [`get_updates`](#get-updates), [`iter_updates`](#iter-updates), [`member_is_admin`](#member-is-admin), [`member_is_joined`](#member-is-joined), [`member_is_owner`](#member-is-owner), [`register_all_endpoints`](#register-all-endpoints), [`remove_chat_keypad`](#remove-chat-keypad), [`remove_commands`](#remove-commands), [`remove_member`](#remove-member), [`reply`](#reply), [`request`](#request), [`request_send_file`](#request-send-file), [`run`](#run), [`send_contact`](#send-contact), [`send_file`](#send-file), [`send_gif`](#send-gif), [`send_image`](#send-image), [`send_location`](#send-location), [`send_message`](#send-message), [`send_music`](#send-music), [`send_poll`](#send-poll), [`send_quiz`](#send-quiz), [`send_video`](#send-video), [`send_voice`](#send-voice), [`set_commands`](#set-commands), [`start`](#start), [`unban_member`](#unban-member), [`update_bot_endpoints`](#update-bot-endpoints), [`upload_file`](#upload-file)

## core

### include_router

```python
include_router(self, router)
```

Register every handler declared on *router*, recursively.

Lets a bot be split into feature modules::

    bot.include_router(admin_router)

Returns the router so calls can be chained.

## bot

### ask

```python
ask(localself, chat_id: str, text: Optional[str]=None, *, filters: Optional[list]=None, timeout: float=60.0, inline_keypad: Any=None, chat_keypad: Any=None)
```

Send a prompt and await the next matching reply in that chat.

While the prompt is pending, the first message in the chat that
passes *filters* is returned to you instead of being dispatched to
handlers, so a two-step flow needs no state flag::

    name = await bot.ask(chat_id, "Your name?", timeout=30)

Raises:
    darkob.NoReply: when nothing arrives within ``timeout``.

### auto_delete_message

```python
auto_delete_message(self: 'darkob.Bot', chat_id: str, message_id: Union[str, int], time: Union[float, int])
```

Automatically delete a message after a specified time.

Parameters:
    chat_id (str): chat_id of the object associated with the message (e.g., user, group, channel).
    message_id (str): The ID of the message to be deleted.
    time (Union[float, int]): The time delay (in seconds) before deleting the message.

Returns:
    The updated information after deleting the message.

### ban_member

```python
ban_member(self: 'darkob.Bot', chat_id: str, sender_id: str)
```

Ban a member from a group or channel.

Parameters:
    chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0').
    sender_id (str): sender_id of member to ban (starts with 'u0').

Returns:
    The API response.

### check_join

```python
check_join(self: 'darkob.Bot', chat_id: str, user_id: str)
```

Check whether a user is a member of the given chat.

Parameters:
    chat_id (str): chat_id of group (g0...) or channel (c0...).
    user_id (str): user_id of the user (u0...).

Returns:
    bool: True if the user is a member, else False.

### close

```python
close(self: 'darkob.Bot')
```

Async close — must be awaited inside the session's loop.

### delete

```python
delete(localself, event: Any)
```

Delete the message that produced *event*.

### delete_message

```python
delete_message(self: 'darkob.Bot', chat_id: str, message_id: Union[int, str])
```

Delete a single message.

Parameters:
    chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0') or user (starts with 'b0').
    message_id (Union[str, int]): message_id of the message to be deleted.

Returns:
    The API response with delete message information.

### delete_messages

```python
delete_messages(self: 'darkob.Bot', chat_id: str, message_ids: Union[int, str, List[Union[int, str]]])
```

Delete one or more messages.

Parameters:
    chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0') or user (starts with 'b0').
    message_ids (Union[int, str, List[Union[int, str]]]): A single message ID or a list of message IDs to delete.

Returns:
    A list of API responses, one for each message.

### disconnect

```python
disconnect(self: 'darkob.Bot')
```

Close the session synchronously, from any context:
  - if a loop is running, schedule the close on it;
  - if the owning loop is running in another thread, schedule there;
  - otherwise, run a new/owner loop to completion.

### download_file

```python
download_file(self: 'darkob.Bot', file_id: str, name: Optional[str]=None, path: Optional[str]=None, save_as: bool=False, as_base64: bool=False, callback: Optional[Callable[[int, int, float], None]]=None, resume: bool=True)
```

Download a file by ID, preserving darkob's original return types.

``save_as=True`` returns a status dictionary with ``file_path`` and
``size``. Otherwise the raw bytes are returned, or a base64 string
when ``as_base64=True``. Upstream 1.18 changed these returns to a
``Data`` wrapper, which would break existing darkob callers, so its
validation improvements are kept without its return-type change.

### edit

```python
edit(localself, event: Any, text: str, **kwargs: Any)
```

Edit the message that produced *event* to say *text*.

### edit_chat_keypad

```python
edit_chat_keypad(self: 'darkob.Bot', chat_id: str, chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]], resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Edits or adds a new chat keypad (custom keyboard) to the chat.

Parameters:
    chat_id (str): chat_id of the group (starts with 'g0') or user (starts with 'b0').
    chat_keypad (Dict[str, Any] or List): The keyboard layout to set. Supports three formats:

        1. Simple list of strings:
            [
                ["Button 1", "Button 2"],
                ["Button 3"]
            ]
            Each inner list is a row. Buttons are strings. The type is set to "Simple" and IDs are assigned automatically starting from 100.

        2. List of tuples: (button_text, button_id, button_type)
            [
                [("راهنما", "help")],
                [("تلاش مجدد", "retry"), ("بستن", "close")],
                [("پنل مدیریت", "panel", "Simple"), ("تنظیمات", "settings", "Simple")],
                [("درباره", None), ("پشتیبانی", None)],
                [("✅ تایید", "confirm"), ("❌ لغو", "cancel"), ("🔄 بازگشت", "back")],
            ]
            Tuple structure: (text, id, type) - text: button text, id: button ID (if None, auto-assigned starting from 100), type: button type (if omitted, defaults to "Simple").

        3. Full dictionary (raw API format):
            {
                "rows": [
                    {"buttons": [{"id": "1", "button_text": "Button 1", "type": "Simple"}]},
                    {"buttons": [{"id": "2", "button_text": "Button 2", "type": "Simple"}]}
                ]
            }

    resize_keyboard (bool, optional): Requests clients to resize the keyboard vertically. Defaults to True.
    one_time_keyboard (bool, optional): Requests clients to hide the keyboard as soon as it's been used. Defaults to False.

Returns:
    The API response after editing the chat keypad.

### edit_inline_keypad

```python
edit_inline_keypad(self: 'darkob.Bot', chat_id: str, message_id: Union[str, int], inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]])
```

Edits the inline keyboard of a specific message in a chat.

Parameters:
    chat_id (str): chat_id of the chat containing the message. Must be a valid GUID (c0..., g0..., b0...) or a username (@username).
    message_id (str or int): Identifier of the message whose inline keypad should be updated. If passed as a string, it must contain only digits.
    inline_keypad (Dict[str, Any] or List): The new inline keyboard layout. Supports three formats:

        1. Simple list of strings:
            [
                ["Button 1", "Button 2"],
                ["Button 3"]
            ]
            Each inner list is a row. Buttons are strings. The type is set to "Simple" and IDs are assigned automatically starting from 100.

        2. List of tuples: (button_text, button_id, button_type)
            [
                [("راهنما", "help")],
                [("تلاش مجدد", "retry"), ("بستن", "close")],
                [("پنل مدیریت", "panel", "Simple"), ("تنظیمات", "settings", "Simple")],
                [("درباره", None), ("پشتیبانی", None)],
                [("✅ تایید", "confirm"), ("❌ لغو", "cancel"), ("🔄 بازگشت", "back")],
            ]
            Tuple structure: (text, id, type) - text: button text, id: button ID (if None, auto-assigned starting from 100), type: button type (if omitted, defaults to "Simple").

        3. Full dictionary (raw API format):
            {
                "rows": [
                    {"buttons": [{"id": "1", "button_text": "Button 1", "type": "Simple"}]},
                    {"buttons": [{"id": "2", "button_text": "Button 2", "type": "Simple"}]}
                ]
            }

        Note: Passing an empty list ([]) or None removes the inline keypad from the message.

Uses the ``editMessageKeypad`` endpoint. The reference page's
cURL sample shows ``editInlineKeypad``, but that name returns
``INVALID_INPUT: Invalid Method`` against the live API, while
``editMessageKeypad`` answers ``OK``. The prose heading is right
and the sample is stale.

Returns:
    API response with message information.

### edit_message

```python
edit_message(self: 'darkob.Bot', chat_id: str, message_id: Union[str, int], text: str, metadata: Optional[Dict[str, Any]]=None, inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None)
```

Edits an existing message in a chat.

Parameters:
    chat_id (str): chat_id of the chat.
    message_id (Union[str, int]): The unique identifier of the message to edit.
    text (str): The new text of the message.
    metadata (dict, optional): Pre-formatted metadata (Bold, Italic, etc.).
    inline_keypad (dict or list, optional): Replacement inline
        keyboard. Accepts a Keyboard builder, a list of rows, or a
        raw keypad dict. Pass an empty list to remove it.

Returns:
    API response with message information.

### forward_message

```python
forward_message(self: 'darkob.Bot', from_chat_id: str, message_id: Union[str, int], to_chat_id: str, disable_notification: bool=False)
```

Forward a message from one chat to another.

Parameters:
    from_chat_id (str): chat_id of the source object from which messages are forwarded.
    message_id (Union[str, int]): message_id of the message to be forwarded.
    to_chat_id (str): chat_id of the destination object to which messages are forwarded.
    disable_notification (bool): If set to True, the message will be sent silently without triggering a notification for users. Defaults to False.

Returns:
    API response with message information.

### forward_messages

```python
forward_messages(self: 'darkob.Bot', from_chat_id: str, message_ids: Union[int, str, List[Union[int, str]]], to_chat_id: str, disable_notification: bool=False)
```

Forward one or more messages from one chat to another.

Parameters:
    from_chat_id (str): chat_id of the source object from which messages are forwarded.
    message_ids (Union[int, str, List[Union[int, str]]]): A single message ID or a list of message IDs to forward.
    to_chat_id (str): chat_id of the destination object to which messages are forwarded.
    disable_notification (bool): If set to True, the messages will be sent silently without triggering a notification for users. Defaults to False.

Returns:
    API responses, one for each forwarded message.

### get_chat_info

```python
get_chat_info(self: 'darkob.Bot', chat_id: str)
```

Get information about a user, group, or channel.

Parameters:
    chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0') or user (starts with 'b0').

Returns:
    The API response with chat information.

### get_chat_member

```python
get_chat_member(self: 'darkob.Bot', chat_id: str, user_id: str)
```

Get information about a single member of a chat.

Parameters:
    chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0').
    user_id (str): user_id of member to look up (starts with 'u0').

Returns:
    The API response.

### get_file

```python
get_file(self: 'darkob.Bot', file_id: str)
```

Requests the file associated with the specified file ID.

Parameters:
    file_id (str): The identifier of the file to retrieve. This should be a valid file ID within the system.

### get_me

```python
get_me(self: 'darkob.Bot', refresh: bool=False)
```

Get information about the authenticated bot.

The result is cached for the lifetime of the bot, because a bot's
identity does not change. Pass ``refresh=True`` to force a new
request.

Parameters:
    refresh (bool): Ignore the cache and re-fetch. Defaults to False.

Returns:
    Information about the authenticated bot.

### get_token_string

```python
get_token_string(self: 'darkob.Bot', password: Optional[str]=None)
```

Export current bot token as an encrypted TokenString.

Parameters:
    password (str, optional): Optional password for encryption. If provided, TokenString can only be opened with this password.

Returns:
    str: Encrypted TokenString that can be used later with `Bot(token_string=..., password=...)`.

### get_updates

```python
get_updates(self: 'darkob.Bot', offset_id: Optional[str]=None, limit: int=100)
```

Fetches new updates (like messages) from the API.

Parameters:
    offset_id (str, optional): Identifier to fetch subsequent updates. Defaults to None.
    limit (int, optional): Maximum number of updates to retrieve. Defaults to 100.

Returns:
    The API response including updates and the next_offset_id.

### iter_updates

```python
iter_updates(localself, limit: int=100, max_pages: Optional[int]=None)
```

Yield updates one at a time, handling the offset cursor.

Args:
    limit: Updates requested per round-trip.
    max_pages: Stop after this many round-trips (``None`` = forever).

Yields:
    Individual update payloads, in server order.

### member_is_admin

```python
member_is_admin(self: 'darkob.Bot', chat_id: str, user_id: str)
```

Check whether a member is an admin or owner of the given chat.

Parameters:
    chat_id (str): chat_id of group (g0...) or channel (c0...).
    user_id (str): user_id of the member (u0...).

Returns:
    bool: True if status is 'Admin' or 'Creator', else False.

### member_is_joined

```python
member_is_joined(self: 'darkob.Bot', chat_id: str, user_id: str)
```

Check whether a user is a member of the given chat.

Parameters:
    chat_id (str): chat_id of group (g0...) or channel (c0...).
    user_id (str): user_id of the user (u0...).

Returns:
    bool: True if the user is a member, else False.

### member_is_owner

```python
member_is_owner(self: 'darkob.Bot', chat_id: str, user_id: str)
```

Check whether a member is the owner of the given chat.

Parameters:
    chat_id (str): chat_id of group (g0...) or channel (c0...).
    user_id (str): user_id of the member (u0...).

Returns:
    bool: True if status is 'Creator', else False.

### register_all_endpoints

```python
register_all_endpoints(self: 'darkob.Bot', base_url: str, endpoints: Optional[List[str]]=None)
```

Register all webhook endpoints at once.

Parameters:
    base_url (str): Base URL of your server (e.g. `"https://myserver.com"`). The path `/wk` will be appended automatically.
    endpoints (list of str, optional): Which endpoints to register. If None, registers all five. Defaults to None.

Returns:
    list: Responses for each registration call.

### remove_chat_keypad

```python
remove_chat_keypad(self: 'darkob.Bot', chat_id: str)
```

Removes the custom reply keyboard from the specified chat.

Parameters:
    chat_id (str): chat_id of the chat where the keypad should be removed.

Returns:
    The API response after removing the chat keypad.

### remove_commands

```python
remove_commands(self: 'darkob.Bot')
```

Remove every custom command previously registered for this bot.

The Bot API exposes this as ``setCommands`` with an empty
``bot_commands`` list, which is what this calls.

Returns:
    The API response.

### remove_member

```python
remove_member(self: 'darkob.Bot', chat_id: str, sender_id: str)
```

Remove (Ban) a member from a group or channel.

Parameters:
    chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0').
    sender_id (str): sender_id of member to ban.

Returns:
    The API response.

### reply

```python
reply(localself, event: Any, text: str, **kwargs: Any)
```

Reply to the message that produced *event*.

Equivalent to ``send_message`` with ``chat_id`` and
``reply_to_message_id`` filled in from the event.

### request

```python
request(self: 'darkob.Bot', method: str, endpoint: str=None, input: dict=None, **kwargs)
```

Call the Bot API using either supported public signature.

Darkob's original form is ``request("POST", "getMe", json={})``.
Upstream 1.18 added ``request(method="getMe", input={})`` and the
positional shorthand ``request("getMe", {})``. Both are accepted so
new upstream endpoints and existing darkob applications share this
instrumented retry path.

Args:
    method: HTTP method in the original form, or API method name in
        the upstream form.
    endpoint: API method name in the original form. A dict here is
        treated as the upstream positional ``input`` payload.
    input: JSON body for the upstream call form.
    **kwargs: Extra ``aiohttp`` request arguments, including ``json``.

Returns:
    Response or dict: ``dict`` when ``Bot(as_dict=True)`` is set,
    otherwise a :class:`Response`.

### request_send_file

```python
request_send_file(self: 'darkob.Bot', file_type: Literal['File', 'Image', 'Voice', 'Video', 'Music', 'Gif']='File')
```

Request an upload URL for sending a file to the server.

Parameters:
    file_type (str): Type of file to upload.
        Options: 'File', 'Image', 'Voice', 'Video', 'Music', 'Gif'.
        Defaults to 'File'.

Returns:
    str: Upload URL for the file.

Examples:
    # Get upload URL for an image
    upload_url = await bot.request_send_file(file_type="Image")

    # Then upload file using that URL
    file_id = await bot.upload_file(upload_url, "photo.jpg")

### run

```python
run(self: 'darkob.Bot', poll_interval: float=0.05, webhook_url: Optional[str]=None, webhook_path: str='/wk', host: str='0.0.0.0', port: int=8080)
```

Start the bot.

Parameters:
    poll_interval (float): Seconds between polls in polling mode. Defaults to 0.05 seconds.
    webhook_url (str, optional): Public URL for webhook mode. Defaults to None.
    webhook_path (str): Path for the webhook receiver. Defaults to "/wk".
    host (str): Bind address for the webhook server. Defaults to "0.0.0.0".
    port (int): Bind port for the webhook server. Defaults to 8080.

### send_contact

```python
send_contact(self: 'darkob.Bot', chat_id: str, phone_number: str, first_name: str, last_name: str='', chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Sends a contact message to a chat.

Parameters:
    chat_id (str): chat_id for the target chat.
    phone_number (str): Contact's phone number.
    first_name (str): Contact's first name.
    last_name (str, optional): Contact's last name. Defaults to ''.
    chat_keypad (Dict[str, Any], optional): Custom keyboard attached to the message. Defaults to None.
    inline_keypad (Dict[str, Any], optional): Custom inline keyboard attached to the message. Defaults to None.
    reply_to_message_id (Union[int, str], optional): If the message is a reply, the original message's ID. Defaults to None.
    disable_notification (bool, optional): Sends the message silently. Users will not receive a notification. Defaults to False.
    resize_keyboard (bool, optional): Requests clients to resize the keyboard vertically. Defaults to True.
    one_time_keyboard (bool, optional): Requests clients to hide the keyboard as soon as it's been used. Defaults to False.

Returns:
    API response with message information.

### send_file

```python
send_file(self: 'darkob.Bot', chat_id: str, file: Optional[Union[str, bytes]]=None, file_type: Literal['File', 'Image', 'Voice', 'Video', 'Music', 'Gif']='File', text: Optional[str]=None, file_id: Optional[str]=None, base64: Optional[str]=None, file_name: Optional[str]=None, metadata: Optional[Dict[str, Any]]=None, chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Sends a file to a chat.

Parameters:
    chat_id (str): Target chat ID.
    file (str | bytes, optional): Path to file, URL, or raw bytes.
    file_type (Literal['File', 'Image', 'Voice', 'Video', 'Music', 'Gif']): Type of file. Default is 'File'.
    text (str, optional): Caption text.
    file_id (str, optional): Already uploaded file_id (skips upload).
    base64 (str, optional): Base64 encoded file data.
    file_name (str, optional): Custom file name. If not provided, auto-generated.
    metadata (dict, optional): Pre-formatted metadata (Bold, Italic, etc.).
    chat_keypad (Dict, optional): Custom keyboard attached to the message.
    inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
    reply_to_message_id (Union[int, str], optional): Message ID to reply to.
    disable_notification (bool): Disable notification.
    resize_keyboard (bool): Resize keyboard vertically.
    one_time_keyboard (bool): Hide keyboard after use.

Returns:
    API response with message information.

### send_gif

```python
send_gif(self: 'darkob.Bot', chat_id: str, gif: Optional[Union[str, bytes]]=None, text: Optional[str]=None, file_id: Optional[str]=None, base64: Optional[str]=None, file_name: Optional[str]=None, chat_keypad: Optional[Dict[str, Any]]=None, inline_keypad: Optional[Dict[str, Any]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Sends a gif to a chat.

Parameters:
    chat_id (str): Target chat ID.
    gif (str | bytes, optional): Path to the gif file OR raw bytes.
    text (str, optional): Caption text.
    file_id (str, optional): Already uploaded file_id.
    base64 (str, optional): Base64 encoded gif data.
    file_name (str, optional): Custom file name. If not provided, auto-generated.
    chat_keypad (Dict, optional): Custom keyboard attached to the message.
    inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
    reply_to_message_id (Union[int, str], optional): Message ID to reply to.
    disable_notification (bool): Disable notification.
    resize_keyboard (bool): Resize keyboard vertically.
    one_time_keyboard (bool): Hide keyboard after use.

Returns:
    API response with message information.

### send_image

```python
send_image(self: 'darkob.Bot', chat_id: str, image: Optional[Union[str, bytes]]=None, text: Optional[str]=None, file_id: Optional[str]=None, base64: Optional[str]=None, file_name: Optional[str]=None, chat_keypad: Optional[Dict[str, Any]]=None, inline_keypad: Optional[Dict[str, Any]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Sends an image to a chat.

Parameters:
    chat_id (str): Target chat ID.
    image (str | bytes, optional): Path to the image file OR raw bytes.
    text (str, optional): Caption text.
    file_id (str, optional): Already uploaded file_id.
    base64 (str, optional): Base64 encoded image data.
    file_name (str, optional): Custom file name. If not provided, auto-generated.
    chat_keypad (Dict, optional): Custom keyboard attached to the message.
    inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
    reply_to_message_id (Union[int, str], optional): Message ID to reply to.
    disable_notification (bool): Disable notification.
    resize_keyboard (bool): Resize keyboard vertically.
    one_time_keyboard (bool): Hide keyboard after use.

Returns:
    API response with message information.

### send_location

```python
send_location(self: 'darkob.Bot', chat_id: str, latitude: float, longitude: float, chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Sends a location message to a chat.

Parameters:
    chat_id (str): chat_id for the target chat.
    latitude (float): Latitude of the location.
    longitude (float): Longitude of the location.
    chat_keypad (Dict[str, Any], optional): Custom keyboard attached to the message. Defaults to None.
    inline_keypad (Dict[str, Any], optional): Custom inline keyboard attached to the message. Defaults to None.
    reply_to_message_id (Union[int, str], optional): If the message is a reply, the original message's ID. Defaults to None.
    disable_notification (bool, optional): Sends the message silently. Users will not receive a notification. Defaults to False.
    resize_keyboard (bool, optional): Requests clients to resize the keyboard vertically. Defaults to True.
    one_time_keyboard (bool, optional): Requests clients to hide the keyboard as soon as it's been used. Defaults to False.

Returns:
    API response with message information.

### send_message

```python
send_message(self: 'darkob.Bot', chat_id: str, text: str, metadata: Optional[Dict[str, Any]]=None, chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Sends a text message to a chat.

Parameters:
    chat_id (str): chat_id for the target chat.
    text (str): The text of the message to be sent.
    metadata (dict, optional): Pre-formatted metadata (Bold, Italic, etc.).
    chat_keypad (Dict[str, Any], optional): Custom keyboard attached to the message.
    inline_keypad (Dict[str, Any], optional): Custom inline keyboard attached to the message.
    reply_to_message_id (Union[int, str], optional): If the message is a reply, the original message's ID.
    disable_notification (bool, optional): Sends the message silently.
    resize_keyboard (bool, optional): Requests clients to resize the keyboard vertically.
    one_time_keyboard (bool, optional): Requests clients to hide the keyboard as soon as it's been used.

Returns:
    API response with message information and action methods.

### send_music

```python
send_music(self: 'darkob.Bot', chat_id: str, music: Optional[Union[str, bytes]]=None, text: Optional[str]=None, file_id: Optional[str]=None, base64: Optional[str]=None, file_name: Optional[str]=None, chat_keypad: Optional[Dict[str, Any]]=None, inline_keypad: Optional[Dict[str, Any]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Sends a music to a chat.

Parameters:
    chat_id (str): Target chat ID.
    music (str | bytes, optional): Path to the music file OR raw bytes.
    text (str, optional): Caption text.
    file_id (str, optional): Already uploaded file_id.
    base64 (str, optional): Base64 encoded music data.
    file_name (str, optional): Custom file name. If not provided, auto-generated.
    chat_keypad (Dict, optional): Custom keyboard attached to the message.
    inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
    reply_to_message_id (Union[int, str], optional): Message ID to reply to.
    disable_notification (bool): Disable notification.
    resize_keyboard (bool): Resize keyboard vertically.
    one_time_keyboard (bool): Hide keyboard after use.

Returns:
    API response with message information.

### send_poll

```python
send_poll(self: 'darkob.Bot', chat_id: str, question: str, options: List[str], is_anonymous: bool=True, multi_select: bool=False, chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Send a poll message with the specified parameters.

Parameters:
    chat_id (str): chat_id of the object associated with the poll (e.g., group or channel).
    question (str): The question for the poll.
    options (list): A list of string values representing the poll options.
    is_anonymous (bool): Whether the poll is anonymous or not. Defaults to True.
    multi_select (bool): Whether the poll allows multiple answers or not. Defaults to False.
    chat_keypad (Dict, optional): Custom keyboard attached to the message.
    inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
    reply_to_message_id (Union[str, int]): The ID of the message to reply to.
    disable_notification (bool): If set to True, the poll will be sent silently without triggering a notification for users. Defaults to False.
    resize_keyboard (bool): Resize keyboard vertically.
    one_time_keyboard (bool): Hide keyboard after use.

Returns:
    API response with message information.

### send_quiz

```python
send_quiz(self: 'darkob.Bot', chat_id: str, question: str, options: List[str], correct_option: Union[int, str], hint: Optional[str]=None, is_anonymous: bool=True, chat_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, inline_keypad: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Send a quiz-type poll message with the specified parameters.

Parameters:
    chat_id (str): chat_id of the object associated with the quiz (e.g., group or channel).
    question (str): The question for the quiz.
    options (list): A list of string values representing the quiz options.
    correct_option (Union[int, str]): The index or text of the correct option for quiz-type polls.
    hint (str, optional): A hint for the correct answer in quiz-type polls. Defaults to None.
    is_anonymous (bool): Whether the poll is anonymous or not. Defaults to True.
    chat_keypad (Dict, optional): Custom keyboard attached to the message.
    inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
    reply_to_message_id (Union[int, str]): The ID of the message to reply to.
    disable_notification (bool): If set to True, the poll will be sent silently without triggering a notification for users. Defaults to False.
    resize_keyboard (bool): Resize keyboard vertically.
    one_time_keyboard (bool): Hide keyboard after use.

Returns:
    API response with message information.

### send_video

```python
send_video(self: 'darkob.Bot', chat_id: str, video: Optional[Union[str, bytes]]=None, text: Optional[str]=None, file_id: Optional[str]=None, base64: Optional[str]=None, file_name: Optional[str]=None, chat_keypad: Optional[Dict[str, Any]]=None, inline_keypad: Optional[Dict[str, Any]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Sends a video to a chat.

Parameters:
    chat_id (str): Target chat ID.
    video (str | bytes, optional): Path to the video file OR raw bytes.
    text (str, optional): Caption text.
    file_id (str, optional): Already uploaded file_id.
    base64 (str, optional): Base64 encoded video data.
    file_name (str, optional): Custom file name. If not provided, auto-generated.
    chat_keypad (Dict, optional): Custom keyboard attached to the message.
    inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
    reply_to_message_id (Union[int, str], optional): Message ID to reply to.
    disable_notification (bool): Disable notification.
    resize_keyboard (bool): Resize keyboard vertically.
    one_time_keyboard (bool): Hide keyboard after use.

Returns:
    API response with message information.

### send_voice

```python
send_voice(self: 'darkob.Bot', chat_id: str, voice: Optional[Union[str, bytes]]=None, text: Optional[str]=None, file_id: Optional[str]=None, base64: Optional[str]=None, file_name: Optional[str]=None, chat_keypad: Optional[Dict[str, Any]]=None, inline_keypad: Optional[Dict[str, Any]]=None, reply_to_message_id: Optional[Union[int, str]]=None, disable_notification: bool=False, resize_keyboard: bool=True, one_time_keyboard: bool=False)
```

Sends a voice to a chat.

Parameters:
    chat_id (str): Target chat ID.
    voice (str | bytes, optional): Path to the voice file OR raw bytes.
    text (str, optional): Caption text.
    file_id (str, optional): Already uploaded file_id.
    base64 (str, optional): Base64 encoded voice data.
    file_name (str, optional): Custom file name. If not provided, auto-generated.
    chat_keypad (Dict, optional): Custom keyboard attached to the message.
    inline_keypad (Dict, optional): Custom inline keyboard attached to the message.
    reply_to_message_id (Union[int, str], optional): Message ID to reply to.
    disable_notification (bool): Disable notification.
    resize_keyboard (bool): Resize keyboard vertically.
    one_time_keyboard (bool): Hide keyboard after use.

Returns:
    API response with message information.

### set_commands

```python
set_commands(self: 'darkob.Bot', commands: Optional[Union[List[Dict[str, str]], Dict[str, str]]]=None)
```

Sets custom commands for the bot. Pass empty list/dict to remove all commands.

Parameters:
    commands (List[Dict[str, str]] or Dict[str, str], optional): Either a list of dictionaries with 'command' and 'description', or a simple dictionary like {"start": "Start the bot", "help": "Help"}. Example: [{"command": "start", "description": "Start the bot"}, ...] or: {"start": "Start the bot", "help": "Show help"}. If None or empty, all commands will be removed.

Returns:
    API response.

### start

```python
start(self: 'darkob.Bot', poll_interval: float=0.005, webhook_url: Optional[str]=None, webhook_path: str='/wk', host: str='0.0.0.0', port: int=8080)
```

Starts the bot, either by polling for updates or by running a webhook server.

If a `webhook_url` is provided, sets up an aiohttp web server to receive real-time updates from the Rubika API. Otherwise, falls back to a long-polling mechanism to fetch updates continuously.

Parameters:
    poll_interval (float): The interval (in seconds) between each polling operation when running in polling mode. Defaults to 0.005 seconds.
    webhook_url (str, optional): The base URL where the webhook server is accessible. If provided, the bot operates in webhook mode. Defaults to None.
    webhook_path (str): The URL path on the server to handle incoming webhook requests. Defaults to "/wk".
    host (str): The hostname or IP address to bind the webhook server. Use "0.0.0.0" to listen on all available interfaces. Defaults to "0.0.0.0".
    port (int): The port number on which the webhook server will listen. Defaults to 8080.

Returns:
    None

### unban_member

```python
unban_member(self: 'darkob.Bot', chat_id: str, sender_id: str)
```

Unban a member from a group or channel.

Parameters:
    chat_id (str): chat_id of group (starts with 'g0') or channel (starts with 'c0').
    sender_id (str): sender_id of member to unban.

Returns:
    The API response.

### update_bot_endpoints

```python
update_bot_endpoints(self: 'darkob.Bot', url: str, endpoint_type: Literal['ReceiveUpdate', 'ReceiveInlineMessage', 'ReceiveQuery', 'GetSelectionItem', 'SearchSelectionItems']='ReceiveUpdate')
```

Register a single webhook endpoint on the Rubika server.

Parameters:
    url (str): Full URL that Rubika should call when an event occurs. Must be publicly reachable (HTTPS recommended).
    endpoint_type (Literal['ReceiveUpdate', 'ReceiveInlineMessage', 'ReceiveQuery', 'GetSelectionItem', 'SearchSelectionItems']): Which kind of event this URL handles. Default is 'ReceiveUpdate'.

Returns:
    The raw response from the server confirming the registration.

### upload_file

```python
upload_file(self: 'darkob.Bot', url: str, file: Optional[Union[str, bytes]]=None, base64: Optional[str]=None, file_name: Optional[str]=None)
```

Upload a file to the server and return file_id.

Supports local path, URL, raw bytes, and base64. The entire file is uploaded in a single request.

Parameters:
    url (str): Upload URL from `request_send_file`.
    file (str | bytes, optional): Path, URL, or raw bytes.
    base64 (str, optional): Base64-encoded file data.
    file_name (str, optional): Name of the file. Auto-detected when possible.

Returns:
    Optional[str]: file_id or None if failed.
