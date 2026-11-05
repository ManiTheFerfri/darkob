# Messenger API reference

A real user account (userbot): channels, groups, voice chats, settings.

> Generated from the installed package by `scripts/generate_docs_assets.py`. Every signature below is real; do not hand-edit this file.

**324 public methods.**

## Method index

- **messages** (61): [`add_reaction`](#add-reaction), [`auto_delete_message`](#auto-delete-message), [`click_inline_button`](#click-inline-button), [`click_message_url`](#click-message-url), [`delete_all_messages`](#delete-all-messages), [`delete_messages`](#delete-messages), [`delete_my_messages`](#delete-my-messages), [`edit_message`](#edit-message), [`forward_messages`](#forward-messages), [`get_all_messages`](#get-all-messages), [`get_chat_messages`](#get-chat-messages), [`get_first_message`](#get-first-message), [`get_first_messages`](#get-first-messages), [`get_last_message`](#get-last-message), [`get_last_messages`](#get-last-messages), [`get_message_info`](#get-message-info), [`get_message_url`](#get-message-url), [`get_messages`](#get-messages), [`get_messages_by_id`](#get-messages-by-id), [`get_messages_interval`](#get-messages-interval), [`get_messages_reactions`](#get-messages-reactions), [`get_messages_updates`](#get-messages-updates), [`get_pinned_messages`](#get-pinned-messages), [`get_poll_option_voters`](#get-poll-option-voters), [`get_poll_status`](#get-poll-status), [`get_scheduled_messages`](#get-scheduled-messages), [`iter_messages`](#iter-messages), [`mark_as_read`](#mark-as-read), [`mark_as_seen`](#mark-as-seen), [`pin_message`](#pin-message), [`remove_reaction`](#remove-reaction), [`report_message`](#report-message), [`request_send_file`](#request-send-file), [`retract_poll`](#retract-poll), [`search_chat_messages`](#search-chat-messages), [`search_global_messages`](#search-global-messages), [`search_messages`](#search-messages), [`send_contact`](#send-contact), [`send_file`](#send-file), [`send_gif`](#send-gif), [`send_image`](#send-image), [`send_live`](#send-live), [`send_location`](#send-location), [`send_message`](#send-message), [`send_message_api_call`](#send-message-api-call), [`send_music`](#send-music), [`send_now_scheduled_message`](#send-now-scheduled-message), [`send_poll`](#send-poll), [`send_quiz`](#send-quiz), [`send_rubino_post`](#send-rubino-post), [`send_rubino_product`](#send-rubino-product), [`send_rubino_story`](#send-rubino-story), [`send_sticker`](#send-sticker), [`send_video`](#send-video), [`send_video_message`](#send-video-message), [`send_voice`](#send-voice), [`stop_poll`](#stop-poll), [`transcribe_voice`](#transcribe-voice), [`unpin_all_messages`](#unpin-all-messages), [`unpin_message`](#unpin-message), [`vote_poll`](#vote-poll)
- **chats** (81): [`accept_all_join_requests`](#accept-all-join-requests), [`accept_join_request`](#accept-join-request), [`accept_ownership_request`](#accept-ownership-request), [`add_members`](#add-members), [`archive_chat`](#archive-chat), [`ban_member`](#ban-member), [`ban_members`](#ban-members), [`cancel_change_owner`](#cancel-change-owner), [`change_owner`](#change-owner), [`check_join`](#check-join), [`clear_all_drafts`](#clear-all-drafts), [`clear_black_list`](#clear-black-list), [`clear_chat_draft`](#clear-chat-draft), [`click_chat_ads`](#click-chat-ads), [`click_keypad_button`](#click-keypad-button), [`create_join_link`](#create-join-link), [`delete_all_avatars`](#delete-all-avatars), [`delete_avatar`](#delete-avatar), [`delete_chat_history`](#delete-chat-history), [`discard_voice_chat`](#discard-voice-chat), [`dont_show_chat_ads`](#dont-show-chat-ads), [`download_profile_picture`](#download-profile-picture), [`edit_join_link`](#edit-join-link), [`get_all_drafts`](#get-all-drafts), [`get_avatars`](#get-avatars), [`get_banned_members`](#get-banned-members), [`get_chat_ads`](#get-chat-ads), [`get_chat_info`](#get-chat-info), [`get_chat_voice_chat`](#get-chat-voice-chat), [`get_chats`](#get-chats), [`get_chats_info`](#get-chats-info), [`get_chats_updates`](#get-chats-updates), [`get_guid`](#get-guid), [`get_info_by_link`](#get-info-by-link), [`get_info_by_username`](#get-info-by-username), [`get_join_links`](#get-join-links), [`get_join_requests`](#get-join-requests), [`get_my_guid`](#get-my-guid), [`get_pending_owner`](#get-pending-owner), [`get_profile_link_items`](#get-profile-link-items), [`get_related_chats`](#get-related-chats), [`get_voice_chat_participants`](#get-voice-chat-participants), [`get_voice_chat_updates`](#get-voice-chat-updates), [`heartbeat`](#heartbeat), [`join_chat`](#join-chat), [`join_voice_chat`](#join-voice-chat), [`leave_chat`](#leave-chat), [`leave_voice_chat`](#leave-voice-chat), [`member_is_admin`](#member-is-admin), [`mute_chat`](#mute-chat), [`pin_chat`](#pin-chat), [`pin_chat_in_folder`](#pin-chat-in-folder), [`play_voice_chat`](#play-voice-chat), [`reject_join_request`](#reject-join-request), [`reject_ownership_request`](#reject-ownership-request), [`report_chat`](#report-chat), [`report_chat_ads`](#report-chat-ads), [`revoke_join_link`](#revoke-join-link), [`search_global_chats`](#search-global-chats), [`seen_chats`](#seen-chats), [`send_chat_activity`](#send-chat-activity), [`send_voice_chat_activity`](#send-voice-chat-activity), [`set_admin`](#set-admin), [`set_ask_spam`](#set-ask-spam), [`set_chat_auto_delete`](#set-chat-auto-delete), [`set_chat_protected_content`](#set-chat-protected-content), [`set_chat_use_time`](#set-chat-use-time), [`set_voice_chat_setting`](#set-voice-chat-setting), [`set_voice_chat_state`](#set-voice-chat-state), [`speaking`](#speaking), [`start_voice_chat`](#start-voice-chat), [`unarchive_chat`](#unarchive-chat), [`unban_all_members`](#unban-all-members), [`unban_member`](#unban-member), [`unban_members`](#unban-members), [`unmute_chat`](#unmute-chat), [`unpin_chat`](#unpin-chat), [`unpin_chat_in_folder`](#unpin-chat-in-folder), [`unset_admin`](#unset-admin), [`upload_avatar`](#upload-avatar), [`view_chat_ads`](#view-chat-ads)
- **groups** (22): [`create_group`](#create-group), [`delete_group`](#delete-group), [`edit_group_info`](#edit-group-info), [`edit_group_timer`](#edit-group-timer), [`edit_group_title`](#edit-group-title), [`edit_slow_mode`](#edit-slow-mode), [`get_group_admin_access`](#get-group-admin-access), [`get_group_admins`](#get-group-admins), [`get_group_default_access`](#get-group-default-access), [`get_group_info`](#get-group-info), [`get_group_link`](#get-group-link), [`get_group_members`](#get-group-members), [`get_group_mention_list`](#get-group-mention-list), [`get_group_message_read_participants`](#get-group-message-read-participants), [`get_group_online_count`](#get-group-online-count), [`get_unread_mentions`](#get-unread-mentions), [`join_group`](#join-group), [`leave_group`](#leave-group), [`lock_group`](#lock-group), [`set_group_default_access`](#set-group-default-access), [`set_group_link`](#set-group-link), [`unlock_group`](#unlock-group)
- **channels** (20): [`check_channel_username`](#check-channel-username), [`create_channel`](#create-channel), [`delete_channel`](#delete-channel), [`edit_channel_info`](#edit-channel-info), [`edit_channel_title`](#edit-channel-title), [`get_channel_admin_access`](#get-channel-admin-access), [`get_channel_admins`](#get-channel-admins), [`get_channel_info`](#get-channel-info), [`get_channel_link`](#get-channel-link), [`get_channel_members`](#get-channel-members), [`get_channel_post_by_link`](#get-channel-post-by-link), [`get_channel_seen_count`](#get-channel-seen-count), [`get_channel_statistics`](#get-channel-statistics), [`get_post_by_ask_link`](#get-post-by-ask-link), [`join_channel`](#join-channel), [`leave_channel`](#leave-channel), [`seen_channel_messages`](#seen-channel-messages), [`set_channel_link`](#set-channel-link), [`set_channel_type`](#set-channel-type), [`update_channel_username`](#update-channel-username)
- **users** (23): [`add_contact`](#add-contact), [`block_user`](#block-user), [`check_user_username`](#check-user-username), [`delete_contact`](#delete-contact), [`delete_user_chat`](#delete-user-chat), [`discard_call`](#discard-call), [`get_blocked_users`](#get-blocked-users), [`get_common_groups`](#get-common-groups), [`get_contacts`](#get-contacts), [`get_contacts_last_online`](#get-contacts-last-online), [`get_contacts_stories`](#get-contacts-stories), [`get_contacts_updates`](#get-contacts-updates), [`get_last_online`](#get-last-online), [`get_me`](#get-me), [`get_saved_music_playlist`](#get-saved-music-playlist), [`get_top_users`](#get-top-users), [`get_user_info`](#get-user-info), [`remove_from_top_users`](#remove-from-top-users), [`request_video_call`](#request-video-call), [`request_voice_call`](#request-voice-call), [`reset_contacts`](#reset-contacts), [`unblock_all_users`](#unblock-all-users), [`unblock_user`](#unblock-user)
- **settings** (48): [`abort_two_step_setup`](#abort-two-step-setup), [`add_folder`](#add-folder), [`add_saved_music_playlist`](#add-saved-music-playlist), [`add_saved_music_track`](#add-saved-music-track), [`auto_delete_account`](#auto-delete-account), [`change_password`](#change-password), [`check_two_step_passcode`](#check-two-step-passcode), [`confirm_unconfirmed_session`](#confirm-unconfirmed-session), [`delete_account`](#delete-account), [`delete_folder`](#delete-folder), [`delete_saved_music_playlist`](#delete-saved-music-playlist), [`deny_unconfirmed_session`](#deny-unconfirmed-session), [`edit_can_called_by`](#edit-can-called-by), [`edit_can_join_chat_by`](#edit-can-join-chat-by), [`edit_show_birthday`](#edit-show-birthday), [`edit_show_last_online`](#edit-show-last-online), [`edit_show_phone_number`](#edit-show-phone-number), [`edit_show_profile_photo`](#edit-show-profile-photo), [`get_folders`](#get-folders), [`get_my_sessions`](#get-my-sessions), [`get_notification_setting`](#get-notification-setting), [`get_privacy_setting`](#get-privacy-setting), [`get_suggested_folders`](#get-suggested-folders), [`get_two_passcode_status`](#get-two-passcode-status), [`get_unconfirmed_sessions`](#get-unconfirmed-sessions), [`login_disable_two_step`](#login-disable-two-step), [`login_two_step_forget_password`](#login-two-step-forget-password), [`logout`](#logout), [`register_device`](#register-device), [`reorder_folder`](#reorder-folder), [`request_change_phone_number`](#request-change-phone-number), [`request_forget_password`](#request-forget-password), [`request_recovery_email`](#request-recovery-email), [`set_notification`](#set-notification), [`set_saved_music_playlist`](#set-saved-music-playlist), [`set_setting`](#set-setting), [`set_two_step_verification`](#set-two-step-verification), [`terminate_other_sessions`](#terminate-other-sessions), [`terminate_session`](#terminate-session), [`turn_off_two_step`](#turn-off-two-step), [`update_my_bio`](#update-my-bio), [`update_my_birthday`](#update-my-birthday), [`update_my_name`](#update-my-name), [`update_my_profile`](#update-my-profile), [`update_my_username`](#update-my-username), [`upgrade_to_api6`](#upgrade-to-api6), [`verify_change_phone_number`](#verify-change-phone-number), [`verify_recovery_email`](#verify-recovery-email)
- **extras** (30): [`add_live_comment`](#add-live-comment), [`add_sticker_set`](#add-sticker-set), [`add_to_my_gif_set`](#add-to-my-gif-set), [`archive_sticker_set`](#archive-sticker-set), [`delete_all_my_gif_set`](#delete-all-my-gif-set), [`delete_my_gif_set`](#delete-my-gif-set), [`delete_sticker_set`](#delete-sticker-set), [`feedback_voice_transcription`](#feedback-voice-transcription), [`get_available_reactions`](#get-available-reactions), [`get_link_from_app_url`](#get-link-from-app-url), [`get_live_comments`](#get-live-comments), [`get_live_play_url`](#get-live-play-url), [`get_live_status`](#get-live-status), [`get_location_view`](#get-location-view), [`get_my_archived_sticker_sets`](#get-my-archived-sticker-sets), [`get_my_gif_set`](#get-my-gif-set), [`get_my_sticker_sets`](#get-my-sticker-sets), [`get_sticker_set_by_id`](#get-sticker-set-by-id), [`get_sticker_setting`](#get-sticker-setting), [`get_stickers_by_emoji`](#get-stickers-by-emoji), [`get_stickers_by_set_ids`](#get-stickers-by-set-ids), [`get_time`](#get-time), [`get_trend_sticker_sets`](#get-trend-sticker-sets), [`get_wallet_transaction_message`](#get-wallet-transaction-message), [`get_wallpapers`](#get-wallpapers), [`reorder_sticker_sets`](#reorder-sticker-sets), [`report_live`](#report-live), [`reset_wallpapers`](#reset-wallpapers), [`search_stickers`](#search-stickers), [`set_current_live_location`](#set-current-live-location)
- **bots** (7): [`delete_bot_chat`](#delete-bot-chat), [`delete_service_chat`](#delete-service-chat), [`get_bot_info`](#get-bot-info), [`get_inline_bots`](#get-inline-bots), [`get_service_info`](#get-service-info), [`start_bot`](#start-bot), [`stop_bot`](#stop-bot)
- **base** (12): [`close`](#close), [`connect`](#connect), [`disconnect`](#disconnect), [`download_file`](#download-file), [`get_string_session`](#get-string-session), [`get_updates`](#get-updates), [`request`](#request), [`run`](#run), [`send_code`](#send-code), [`sign_in`](#sign-in), [`start`](#start), [`upload_file`](#upload-file)
- **core** (3): [`add_handler`](#add-handler), [`remove_handler`](#remove-handler), [`stop`](#stop)
- **decorators** (17): [`on_add_reaction`](#on-add-reaction), [`on_call_signal`](#on-call-signal), [`on_call_update`](#on-call-update), [`on_chat_updates`](#on-chat-updates), [`on_delete_message`](#on-delete-message), [`on_draft_message`](#on-draft-message), [`on_edit_message`](#on-edit-message), [`on_message`](#on-message), [`on_new_message`](#on-new-message), [`on_remove_notifications`](#on-remove-notifications), [`on_remove_reaction`](#on-remove-reaction), [`on_scheduled_message`](#on-scheduled-message), [`on_show_activities`](#on-show-activities), [`on_show_notifications`](#on-show-notifications), [`on_unconfirmed_session`](#on-unconfirmed-session), [`on_voice_chat_participant`](#on-voice-chat-participant), [`on_voice_chat_update`](#on-voice-chat-update)

## messages

### add_reaction

```python
add_reaction(self: 'darkob.Client', chat: str, message_id: Union[str, int], reaction_id: Union[int, str])
```

Add a reaction to a specific message.

Parameters:
    chat (str): The GUID, link, or username of the chat associated with the message.
    message_id (Union[str, int]): The ID of the message to which the reaction will be added.
    reaction_id (Union[str, int]): The ID of the reaction to be added.

Returns:
    The result of the API call.

### auto_delete_message

```python
auto_delete_message(self: 'darkob.Client', chat: str, message_id: Union[str, int], time: Union[float, int])
```

Automatically delete a message after a specified time.

Parameters:
    chat (str): The GUID, link, or username of the chat associated with the message
        (e.g., user, group, channel).
    message_id (Union[str, int]): The ID of the message to be deleted.
    time (Union[float, int]): The time delay (in seconds) before deleting the message.

Returns:
    The updated information after deleting the message.

### click_inline_button

```python
click_inline_button(self: 'darkob.Client', chat: str, message_id: Union[str, int], button_id: str)
```

Send API call response to a chat's inline keypad button.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the message containing inline keyboard.
    button_id (str): The ID of the button.

Returns:
    The result of the API call.

### click_message_url

```python
click_message_url(self: 'darkob.Client', chat: str, message_id: typing.Union[str, int], link_url: str)
```

Simulate clicking a URL contained within a specific message.

Parameters:
    chat (str): The GUID, link or username of the chat.
    message_id (Union[str, int]): The unique ID of the message that includes the URL.
    link_url(str): The URL string embedded in the message to be clicked.

Returns:
    The result of the API call.

### delete_all_messages

```python
delete_all_messages(self: 'darkob.Client', chat: str, exclude_message_ids: Optional[Union[str, int, List[Union[str, int]]]]=None)
```

Delete all messages in a chat except the first creation event message
and optionally specified message IDs.

This method retrieves all messages from the chat and deletes them,
while preserving:
- Any message IDs specified in `exclude_message_ids`.

Parameters:
    chat (str): The GUID, link, or username of the chat
    exclude_message_ids (Union[str, int, List[Union[str, int]]], optional): 
        Message ID(s) to preserve (not delete). Can be string, integer, or list.
        Default is None.

Returns:
    Result of the deletion operation.

### delete_messages

```python
delete_messages(self: 'darkob.Client', chat: str, message_ids: Union[str, int, list], type: Literal['Local', 'Global', 'Scheduled']='Global')
```

Delete specified messages associated with the given chat.

Parameters:
    chat (str): The GUID, link, or username of the chat associated with the messages
        (e.g., user, group, channel).
    message_ids (Union[str, int, list]): The ID or list of IDs of the messages to be deleted.
    type (str): The type of deletion, can be 'Global', 'Local', or 'Scheduled'. Default is 'Global'.

Returns:
    The updated information after deleting the messages.

### delete_my_messages

```python
delete_my_messages(self: 'darkob.Client', chat: str, exclude_message_ids: Optional[Union[str, int, List[Union[str, int]]]]=None)
```

Delete all messages sent by the authenticated user in a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    exclude_message_ids (Optional[Union[str, int, List[Union[str, int]]]]): 
        Message ID(s) to exclude from deletion (preserve them). Default is None.

Returns:
    Result of the deletion operation.

### edit_message

```python
edit_message(self: 'darkob.Client', chat: str, message_id: Union[int, str], text: str, metadata: Optional[dict]=None)
```

Edit the specified message associated with the given chat.

Parameters:
    chat (str): The GUID, link, or username of the chat associated with the message
        (e.g., user, group, channel).
    message_id (Union[int, str]): The ID of the message to be edited.
    text (str): The new text content for the message.
    metadata (dict, optional): Pre-formatted metadata (Bold, Italic, etc.).

Returns:
    The updated information after editing the message.

### forward_messages

```python
forward_messages(self: 'darkob.Client', from_chat: str, message_ids: Union[str, int, list], to_chat: str, hide_author: bool=False, is_mute: bool=False, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None)
```

Forward specified messages from one chat to another.

Parameters:
    from_chat (str): The GUID, link, or username of the source chat.
    message_ids (Union[str, int, list]): The IDs of the messages to forward.
    to_chat (str): The GUID, link, or username of the destination chat.
    hide_author (bool): Hide the original sender's identity. Default is False.
    is_mute (bool): Forward silently without notification. Default is False.
    schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
        When to send the forwarded message.
        - Unix timestamp (int/float): Absolute time
        - timedelta: Relative time from now
        - datetime: Absolute date and time
    schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online.

Returns:
    The updated information after forwarding the messages.

### get_all_messages

```python
get_all_messages(self: 'darkob.Client', chat: str, show_message_ids: bool=False)
```

Retrieve all messages from a chat.

Parameters:
    chat (str): Chat identifier or link (username, GUID, or invite link)
    show_message_ids (bool, optional): Include message IDs in output. Default is False.

Returns:
    Result containing all messages with total count, first/last IDs, and chat GUID.

### get_chat_messages

```python
get_chat_messages(self: 'darkob.Client', chat: str, max_id: Union[str, int]=None, sort: Literal['FromMax', 'FromMin']='FromMin', filter_type: Optional[Literal['Voice', 'File', 'Music', 'Gif', 'Media', 'Link']]=None, limit: int=None)
```

Get messages from a chat with filtering and pagination.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    max_id (Union[str, int], optional): Maximum message ID to start from.
    sort (Literal['FromMax', 'FromMin']): Sort direction. Default is 'FromMin'.
    filter_type (Literal, optional): Filter messages by type:
        'Voice', 'File', 'Music', 'Gif', 'Media', 'Link'
    limit (int, optional): Maximum number of messages to retrieve. If None, fetches all messages.

Returns:
    The result containing messages, count, and pagination info.

### get_first_message

```python
get_first_message(self: 'darkob.Client', chat: str)
```

Get the first message of a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The first message details.

### get_first_messages

```python
get_first_messages(self: 'darkob.Client', chat: str, limit: int=100)
```

Get the first messages of a chat up to a limit.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    limit (int): Maximum number of messages to retrieve (max 100, min 1).

Returns:
    List of first messages and count.

### get_last_message

```python
get_last_message(self: 'darkob.Client', chat: str)
```

Get the last message from a chat and retrieve its details.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The last message details.

### get_last_messages

```python
get_last_messages(self: 'darkob.Client', chat: str, limit: int=100)
```

Get the last messages of a chat up to a limit.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    limit (int): Maximum number of messages to retrieve (max 1000).

Returns:
    List of last messages and count.

### get_message_info

```python
get_message_info(self: 'darkob.Client', chat: str, message_id: Union[str, int])
```

Get detailed information about a message.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the message to retrieve.

Returns:
    Message information.

### get_message_url

```python
get_message_url(self: 'darkob.Client', chat: str, message_id: Union[str, int])
```

Get the shareable URL of a specific message.

Parameters:
    chat (str): The GUID, link, or username of the chat to which the message belongs.
    message_id (Union[str, int]): The ID of the message for which to retrieve the shareable URL.

Returns:
    The shareable URL of the specified message.

### get_messages

```python
get_messages(self: 'darkob.Client', chat: str, types: Optional[Union[str, List[str]]]=None)
```

Get messages from a chat with optional type filtering.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    types (Optional[Union[str, List[str]]]): Type(s) of messages to filter by.
        Each item is independent.
        Available types:
            - "text": Text messages
            - "image": Image messages
            - "video": Video messages (non-round)
            - "video_message": Round video messages
            - "voice": Voice messages
            - "music": Music messages
            - "file": File messages
            - "gif": GIF messages
            - "live": Live messages
            - "location": Location messages
            - "poll": Poll messages
            - "contact": Contact messages (only private chats)
            - "event": Event messages
            - "edited": Edited messages
            - "forwarded": Forwarded messages
            - "sticker": Sticker messages
            - "me": Messages sent by the client itself
            - "bots": Messages sent by bots
            - "users": Messages sent by users
        You can also pass a member GUID or username for member filtering.
        If None, returns all messages.

Returns:
    - messages: list of filtered messages.
    - count: number of filtered messages.
    - chat_guid: The GUID of the chat.
    - total_all: total messages before filtering.
    - filter_types: list of applied type filters.
    - member_guids: list of applied member GUID filters.

### get_messages_by_id

```python
get_messages_by_id(self: 'darkob.Client', chat: str, message_ids: Union[str, int, list])
```

Retrieve messages by their IDs.

Parameters:
    chat (str): The GUID, link, or username of the chat to which the messages belong.
    message_ids (Union[str, int, list]): The ID or list of IDs of the messages to retrieve.

Returns:
    The retrieved messages identified by their IDs.

### get_messages_interval

```python
get_messages_interval(self: 'darkob.Client', chat: str, middle_message_id: Union[int, str])
```

Retrieve messages in an interval around a middle message ID.

Parameters:
    chat (str): The GUID, link, or username of the chat to which the messages belong.
    middle_message_id (Union[int, str]): The middle message ID around which the interval is determined.

Returns:
    The retrieved messages in the specified interval.

### get_messages_reactions

```python
get_messages_reactions(self: 'darkob.Client', chat: str, min_id: Union[str, int], max_id: Union[str, int])
```

Get reactions of messages in a chat within a specific ID range.

Parameters:
    chat (str): Chat identifier (link, username, or GUID)
    min_id (Union[str, int]): Minimum message ID (lower bound)
    max_id (Union[str, int]): Maximum message ID (upper bound)

Returns:
    List of reactions for messages in the specified range.

### get_messages_updates

```python
get_messages_updates(self: 'darkob.Client', chat: str, state: int=round(time()) - 150)
```

Get message updates for a specific chat.

Parameters:
    chat (str): The GUID, link, or username of the chat for which updates are requested.
    state (int): The state at which updates are requested. Defaults to a timestamp approximately 150 seconds ago.

Returns:
    The message updates for the specified chat.

### get_pinned_messages

```python
get_pinned_messages(self: 'darkob.Client', chat: str)
```

Get all pinned messages from a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    Data: Dictionary containing pinned messages and optionally message IDs.

### get_poll_option_voters

```python
get_poll_option_voters(self: 'darkob.Client', poll_id: str, selection_index: Union[str, int], start_id: Optional[str]=None)
```

Get voters for a specific poll option.

Parameters:
    poll_id (str): The ID of the poll for which voters are requested.
    selection_index (Union[str, int]): The index of the poll option for which voters are requested.
    start_id (Optional[str]): The ID from which to start fetching voters. Defaults to None.

Returns:
    The voters for the specified poll option.

### get_poll_status

```python
get_poll_status(self: 'darkob.Client', poll_id: str)
```

Get the status of a specific poll.

Parameters:
    poll_id (str): The ID of the poll for which the status is requested.

Returns:
    The status of the specified poll.

### get_scheduled_messages

```python
get_scheduled_messages(self: 'darkob.Client', chat: str, start_id: str=None)
```

Get scheduled messages in a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    start_id (str, optional): The ID to start fetching from. Defaults to None.

Returns:
    The result of the API call containing scheduled messages.

### iter_messages

```python
iter_messages(self: 'darkob.Client', chat: str, *, sort: str='FromMin', filter_type: Optional[str]=None, page_size: int=25, max_items: Optional[int]=None)
```

Yield messages from *chat*, one page at a time.

Parameters:
    chat (str): Chat GUID, link or username.
    sort (str): 'FromMin' (oldest first) or 'FromMax' (newest first).
    filter_type (str, optional): 'Voice', 'File', 'Music', 'Gif',
        'Media' or 'Link'.
    page_size (int): Messages requested per round-trip.
    max_items (int, optional): Stop after this many messages.

Yields:
    Each message as a :class:`~darkob.data.Data` object.

### mark_as_read

```python
mark_as_read(self: 'darkob.Client', chat: str)
```

Mark a chat as read by seeing the last message.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    Result of the operation.

### mark_as_seen

```python
mark_as_seen(self: 'darkob.Client', chat: str, message_id: Union[str, int]=None)
```

Mark a specific message as seen.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int], optional): Specific message ID. Defaults to last message.

Returns:
    Result of the operation.

### pin_message

```python
pin_message(self: 'darkob.Client', chat: str, message_id: Union[str, int])
```

pin a message.

Parameters:
    chat (str): The GUID, link, or username of the recipient.
    message_id (Union[str, int]): The ID of the message to pin.

Returns:
    The update indicating the success of the operation.

### remove_reaction

```python
remove_reaction(self: 'darkob.Client', chat: str, message_id: Union[str, int], reaction_id: Union[int, str])
```

Remove a reaction from a specific message.

Parameters:
    chat (str): The GUID, link, or username of the chat associated with the message.
    message_id (str): The ID of the message from which the reaction will be removed.
    reaction_id (int): The ID of the reaction to be removed.

Returns:
    The update indicating the success of removing the reaction.

### report_message

```python
report_message(self: 'darkob.Client', chat: str, message_id: Union[str, int], report_type: Union[int, str], description: Optional[str]=None)
```

Report a message for a specific reason.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the message to be reported.
    report_type (Union[int, str]): The report reason.
        Can be:
            - Integer code between 100 and 106
            - String name (case-insensitive): 'Other', 'Violence',
              'Spam', 'Porn', 'ChildAbuse', 'Copyright', 'Fraud'
        If set to 100 (Other), `description` becomes required.
    description (Optional[str]): Description for the report.
        Required when `report_type` is 100 (Other).

Returns:
    The result of the API call.

### request_send_file

```python
request_send_file(self: 'darkob.Client', file_name: str, size: Union[str, int, float], mime: str=None)
```

Request sending a file.

Parameters:
    file_name (str): The name of the file to be sent.
    size (Union[str, int, float]): The size of the file to be sent.
    mime (str, optional): The MIME type of the file. If None, it will be derived from the file name.

Returns:
    The update indicating the success of the file sending request.

### retract_poll

```python
retract_poll(self: 'darkob.Client', poll_id: str)
```

Retract a poll.

Parameters:
    poll_id (str): The ID of the poll to retract.

Returns:
    The result of the API call.

### search_chat_messages

```python
search_chat_messages(self: 'darkob.Client', chat: str, search_text: str)
```

Searches for chat messages based on the specified criteria.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    search_text (str): The text to search for in messages. 

Returns:
    The search results containing messages.

### search_global_messages

```python
search_global_messages(self: 'darkob.Client', search_text: str, start_id: Optional[str]=None)
```

Search for messages globally across all chats.

Parameters:
    search_text (str): The text or hashtag to search for.
    start_id (str, optional): The ID to start fetching from. Defaults to None.

Returns:
    The result of the API call.

### search_messages

```python
search_messages(self: 'darkob.Client', chat: str, text: str)
```

Search for messages containing specific text in a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    text (str): The text to search for.

Returns:
    The search results.

### send_contact

```python
send_contact(self: 'darkob.Client', chat: str, phone_number: Union[str, int], user: str, first_name: str, last_name: str='', vcard: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None)
```

Send a contact message to a specified chat.

Parameters:
    chat (str): The GUID or username of the user or bot.
    phone_number (Union[str, int]): Contact's phone number.
    user (str): Contact's username or user GUID.
    first_name (str): Contact's first name.
    last_name (str, optional): Contact's last name. Defaults to "".
    vcard (str, optional): Custom vCard string. Defaults to None.
    reply_to_message_id (Union[str, int], optional): ID of the message
        to reply to. Defaults to None.

Returns:
    The result of the API call.

### send_file

```python
send_file(self: 'darkob.Client', chat: str, file: Union[Path, bytes]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: str=None, **kwargs)
```

Send a file.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    file (Union[Path, bytes], optional): The file data (path or bytes).
    text (Optional[str]): The caption for the file. Defaults to None.
    reply_to_message_id (Optional[Union[str, int]]): The ID of the message to which this is a reply. Defaults to None.
    via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
    schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
        When to send the message.
        - Unix timestamp (int/float): Absolute time
        - timedelta: Relative time from now
        - datetime: Absolute date and time
    schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
    base64 (str, optional): Base64 encoded file data.

Returns:
    The result of the API call.

### send_gif

```python
send_gif(self: 'darkob.Client', chat: str, gif: Union[Path, bytes]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, thumb: Optional[Union[bool, str]]=None, width: Optional[int]=None, height: Optional[int]=None, time: Optional[int]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: str=None, **kwargs)
```

Send a GIF to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    gif (Path, bytes, optional): The GIF data. Can be a file path or bytes.
    text (Optional[str]): Caption for the GIF. Defaults to None.
    reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
    via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
    thumb (Optional[Union[bool, str]]): Thumbnail behavior:
        - None or True: Auto-generate thumbnail using available libraries (default)
        - False: Use default thumbnail
        - str: Custom thumbnail as Base64 string (pure Base64, no data:image header)
    width (Optional[int]): Custom width for the GIF. Defaults to None (auto-detect).
    height (Optional[int]): Custom height for the GIF. Defaults to None (auto-detect).
    time (Optional[int]): Custom duration for the GIF in seconds. Defaults to None (auto-detect).
    schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
        When to send the message.
        - Unix timestamp (int/float): Absolute time
        - timedelta: Relative time from now
        - datetime: Absolute date and time
    schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
    base64 (str, optional): Base64 encoded GIF data.

Returns:
    The API response containing the sent message details.

### send_image

```python
send_image(self: 'darkob.Client', chat: str, image: Union[Path, bytes]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, is_spoil: bool=False, via_bot: Optional[str]=None, thumb: Optional[Union[bool, str]]=None, width: Optional[int]=None, height: Optional[int]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: str=None, **kwargs)
```

Send an image to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    image (Path, bytes, optional): The image data. Can be a file path or bytes.
    text (Optional[str]): Caption for the image. Defaults to None.
    reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
    is_spoil (bool): Whether the image should be marked as a spoiler. Defaults to False.
    via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
    thumb (Optional[Union[bool, str]]): Thumbnail behavior:
        - None or True: Auto-generate thumbnail using available libraries (or default).
        - str: Custom thumbnail as Base64 string.
    width (Optional[int]): Custom width for the image. Defaults to None (auto-detect).
    height (Optional[int]): Custom height for the image. Defaults to None (auto-detect).
    schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
        When to send the message.
        - Unix timestamp (int/float): Absolute time
        - timedelta: Relative time from now
        - datetime: Absolute date and time
    schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
    base64 (str, optional): Base64 encoded image data.

Returns:
    The API response containing the sent message details.

### send_live

```python
send_live(self: 'darkob.Client', chat: str, title: str=None, reply_to_message_id: Union[str, int]=None, thumb: Optional[Union[str, Path, bytes]]=None)
```

Send a live stream.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    title (str): Live stream title.
    reply_to_message_id (Optional[Union[str, int]]): The ID of the message to which this is a reply. Defaults to None.
    thumb (Optional[Union[str, Path, bytes]]): Thumbnail for the live stream.
        - str: Base64 encoded string, file path, or URL.
        - Path: Path to thumbnail file.
        - bytes: Raw thumbnail bytes.
        If not provided, a default thumbnail will be used.

Returns:
    The result of the API call.

### send_location

```python
send_location(self: 'darkob.Client', chat: str, latitude: float, longitude: float, reply_to_message_id: Union[str, int]=None)
```

Send a map location.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    latitude (float): Latitude (-90 to 90).
    longitude (float): Longitude (-180 to 180).
    reply_to_message_id (Optional[Union[str, int]]): The ID of the message to which this is a reply. Defaults to None.

Returns:
    The result of the API call.

### send_message

```python
send_message(self: 'darkob.Client', chat: str, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, file_inline: Optional[Union[Data, Path, bytes]]=None, base64_data: Optional[str]=None, sticker: Optional[Union[Data, dict]]=None, type: str='File', is_spoil: bool=False, thumb: Optional[Union[bool, str, Path, bytes]]=None, audio_info: bool=True, metadata: Optional[dict]=None, performer: Optional[str]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, **kwargs)
```

Send a message to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    text (Optional[str]): The text content of the message.
    reply_to_message_id (Optional[Union[str, int]]): The ID of the message to reply to.
    via_bot (Optional[str]): Bot GUID or username to send the message via.
    metadata (Optional[dict]): Additional metadata for text formatting.
    schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
        When to send the message. Accepts:
        - Unix timestamp (int/float): Absolute time
        - timedelta: Relative time from now (e.g., timedelta(hours=1))
        - datetime: Absolute date and time
    schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online.

Returns:
    MessageResult: The API response containing the sent message details,
    with action methods like edit, delete, reply, forward, pin.

### send_message_api_call

```python
send_message_api_call(self: 'darkob.Client', chat: str, message_id: Union[str, int], button_id: str)
```

Send API call response to a chat's inline keyboard button.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): ID of the message containing inline keyboard.
    button_id (str): ID of the button.

Returns:
    The result of the API call.

Example:
    >>> await client.send_message_api_call(
    ...     chat="b0C2y04506bd2306f068aa161e0502db",
    ...     message_id="1499338519906784",
    ...     button_id="b0SPm00c8ab83b689ac2eeffe16ec7db"
    ... )

### send_music

```python
send_music(self: 'darkob.Client', chat: str, music: Union[Path, bytes]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, performer: Optional[str]=None, time: Optional[int]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: str=None, **kwargs)
```

Send a music file to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    music (Path, bytes, optional): The music data. Can be a file path or bytes.
    text (Optional[str]): Caption for the music. Defaults to None.
    reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
    via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
    performer (Optional[str]): Name of the performer/artist. Defaults to None (auto-detect).
    time (Optional[int]): Custom duration for the music in seconds. Defaults to None (auto-detect).
    schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
        When to send the message.
        - Unix timestamp (int/float): Absolute time
        - timedelta: Relative time from now
        - datetime: Absolute date and time
    schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
    base64 (str, optional): Base64 encoded music data.

Returns:
    The API response containing the sent message details.

### send_now_scheduled_message

```python
send_now_scheduled_message(self: 'darkob.Client', chat: str, message_id: Union[int, str])
```

Send a scheduled message immediately.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (int): The ID of the scheduled message to send now.

Returns:
    The result of the API call.

### send_poll

```python
send_poll(self: 'darkob.Client', chat: str, question: str, options: list, is_anonymous: bool=True, multiple_answers: bool=False, reply_to_message_id: Optional[Union[str, int]]=None)
```

Send a poll message with the specified parameters.

Parameters:
    chat (str): The GUID, link or username of the chat associated with the poll (e.g., group, channel).
    question (str): The question for the poll.
    options (list): A list of string values representing the poll options.
    is_anonymous (bool): Whether the poll is anonymous or not. Defaults to True.
    multiple_answers (bool): Whether the poll allows multiple answers or not. Defaults to False.
    reply_to_message_id (Optional[Union[str, int]]): The ID of the message to reply to. Defaults to None.

Returns:
    The updated information after creating the poll.

### send_quiz

```python
send_quiz(self: 'darkob.Client', chat: str, question: str, options: list, correct_option: Union[int, str], hint: str=None, is_anonymous: bool=True, reply_to_message_id: Optional[Union[str, int]]=None)
```

Send a quiz-type poll message with the specified parameters.

Parameters:
    chat (str): The GUID or link or username of the chat associated with the quiz (e.g., group, channel).
    question (str): The question for the quiz.
    options (list): A list of string values representing the quiz options.
    correct_option (Union[int, str]): The index or ID of the correct option for quiz-type polls.
    hint (str): A hint for the correct answer in quiz-type polls. Defaults to None.
    is_anonymous (bool): Whether the poll is anonymous or not. Defaults to True.
    reply_to_message_id (Union[str, int]): The ID of the message to reply to. Defaults to None.

Returns:
    The updated information after creating the quiz-type poll.

### send_rubino_post

```python
send_rubino_post(self: 'darkob.Client', chat: str, post_id: str, post_profile_id: str, is_mute: bool=False)
```

Send a Rubino post to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    post_id (str): The post ID to send.
    post_profile_id (str): The post profile ID.
    is_mute (bool): Send silently without notification. Default is False.

Returns:
    The result of the API call.

### send_rubino_product

```python
send_rubino_product(self: 'darkob.Client', chat: str, store_id: str, product_id: str, product_varieties: List[dict])
```

Send a Rubino product to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    store_id (str): The store ID.
    product_id (str): The product ID.
    product_varieties (List[dict]): List of product varieties.

Returns:
    The result of the API call.

### send_rubino_story

```python
send_rubino_story(self: 'darkob.Client', chat: str, story_id: str, story_profile_id: str, reply_text: str='', type: Literal['Reply', 'Direct']='Reply', is_mute: bool=False)
```

Send a Rubino story reply or direct message.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    story_id (str): The story ID.
    story_profile_id (str): The story profile ID.
    reply_text (str): Reply text. Default is empty string.
    type (str): 'Reply' or 'Direct'. Default is 'Reply'.
    is_mute (bool): Send silently without notification. Default is False.

Returns:
    The result of the API call.

### send_sticker

```python
send_sticker(self: 'darkob.Client', chat: str, emoji_character: str, sticker_id: str, sticker_set_id: str, file: dict, w_h_ratio: str='1.0', reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None)
```

Send a sticker.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    emoji_character (str): The emoji character associated with the sticker.
    sticker_id (str): The ID of the sticker.
    sticker_set_id (str): The ID of the sticker set.
    file (dict): The file data for the sticker.
    w_h_ratio (str): The width-to-height ratio of the sticker. Defaults to '1.0'.
    reply_to_message_id (Optional[Union[str, int]]): The ID of the message to which this is a reply. Defaults to None.
    via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
    schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
        When to send the message.
        - Unix timestamp (int/float): Absolute time
        - timedelta: Relative time from now
        - datetime: Absolute date and time
    schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).

### send_video

```python
send_video(self: 'darkob.Client', chat: str, video: Union[Path, bytes]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, is_spoil: bool=False, via_bot: Optional[str]=None, thumb: Optional[Union[bool, str]]=None, width: Optional[int]=None, height: Optional[int]=None, time: Optional[int]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: str=None, **kwargs)
```

Send a video to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    video (Path, bytes, optional): The video data. Can be a file path or bytes.
    text (Optional[str]): Caption for the video. Defaults to None.
    reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
    is_spoil (bool): Whether the video should be marked as a spoiler. Defaults to False.
    via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
    thumb (Optional[Union[bool, str]]): Thumbnail behavior:
        - None or True: Auto-generate thumbnail using available libraries (or default).
        - str: Custom thumbnail as Base64 string.
    width (Optional[int]): Custom width for the video. Defaults to None (auto-detect).
    height (Optional[int]): Custom height for the video. Defaults to None (auto-detect).
    time (Optional[int]): Custom duration for the video in seconds. Defaults to None (auto-detect).
    schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
        When to send the message.
        - Unix timestamp (int/float): Absolute time
        - timedelta: Relative time from now
        - datetime: Absolute date and time
    schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
    base64 (str, optional): Base64 encoded video data.

Returns:
    The API response containing the sent message details.

### send_video_message

```python
send_video_message(self: 'darkob.Client', chat: str, video_message: Union[Path, bytes]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, is_spoil: bool=False, via_bot: Optional[str]=None, thumb: Optional[Union[bool, str]]=None, width: Optional[int]=None, height: Optional[int]=None, time: Optional[int]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: str=None, **kwargs)
```

Send a video message (round video) to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    video_message (Path, bytes, optional): The video message data. Can be a file path or bytes.
    text (Optional[str]): Caption for the video message. Defaults to None.
    reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
    is_spoil (bool): Whether the video message should be marked as a spoiler. Defaults to False.
    via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
    thumb (Optional[Union[bool, str]]): Thumbnail behavior:
        - None or True: Auto-generate thumbnail using available libraries (or default).
        - str: Custom thumbnail as Base64 string.
    width (Optional[int]): Custom width for the video message. Defaults to None (auto-detect).
    height (Optional[int]): Custom height for the video message. Defaults to None (auto-detect).
    time (Optional[int]): Custom duration for the video message in seconds. Defaults to None (auto-detect).
    schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
        When to send the message.
        - Unix timestamp (int/float): Absolute time
        - timedelta: Relative time from now
        - datetime: Absolute date and time
    schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
    base64 (str, optional): Base64 encoded video message data.

Returns:
    The API response containing the sent message details.

### send_voice

```python
send_voice(self: 'darkob.Client', chat: str, voice: Union[Path, bytes]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, time: Optional[int]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: str=None, **kwargs)
```

Send a voice message to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    voice (Path, bytes, optional): The voice data. Can be a file path or bytes.
    text (Optional[str]): Caption for the voice message. Defaults to None.
    reply_to_message_id (Optional[Union[str, int]]): ID of the message to reply to. Defaults to None.
    via_bot (Optional[str]): Bot GUID or username to send the message via. Defaults to None.
    time (Optional[int]): Custom duration for the voice message in seconds. Defaults to None (auto-detect).
    schedule_time (Optional[Union[int, float, timedelta, datetime]]): 
        When to send the message.
        - Unix timestamp (int/float): Absolute time
        - timedelta: Relative time from now
        - datetime: Absolute date and time
    schedule_type (Optional[Literal['Default', 'WhenOnline']]): 
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online (users only).
    base64 (str, optional): Base64 encoded voice data.

Returns:
    The API response containing the sent message details.

### stop_poll

```python
stop_poll(self: 'darkob.Client', poll_id: str)
```

Stop a poll.

Parameters:
    poll_id (str): The ID of the poll to stop.

Returns:
    The result of the API call.

### transcribe_voice

```python
transcribe_voice(self: 'darkob.Client', chat: Union[str, int], message_id: Union[str, int])
```

Transcribes voice messages.

Parameters:
    chat (str): The GUID, link, or username of the chat (chat, channel, or group) containing the voice message.
    message_id (str): The ID of the voice message.

Returns:
    The transcription result.

### unpin_all_messages

```python
unpin_all_messages(self: 'darkob.Client', chat: str)
```

Unpin all pinned messages in a group, channel, or private chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The update indicating the success of the operation.

### unpin_message

```python
unpin_message(self: 'darkob.Client', chat: str, message_id: Union[str, int])
```

unpin a message.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the message to unpin.

Returns:
    The update indicating the success of the operation.

### vote_poll

```python
vote_poll(self: 'darkob.Client', poll_id: str, selection_index: Union[str, int])
```

Vote on a poll option.

Parameters:
    poll_id (str): The ID of the poll.
    selection_index (Union[str, int]): The index of the option to vote for.

Returns:
    The update indicating the success of the vote.

## chats

### accept_all_join_requests

```python
accept_all_join_requests(self: 'darkob.Client', chat: str, exclude: Optional[Union[str, List[str]]]=None)
```

Accept all pending join requests in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    exclude (Optional[Union[str, List[str]]]): User GUID(s) or username(s) to exclude.

Returns:
    Result containing accepted count and details.

### accept_join_request

```python
accept_join_request(self: 'darkob.Client', chat: str, user: str)
```

Accept a join request for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    user (str): The user GUID or username of the requester.

Returns:
    The result of the API call.

### accept_ownership_request

```python
accept_ownership_request(self: 'darkob.Client', chat: str)
```

Accept an ownership transfer request.

Parameters:
    chat (str): The GUID, link, or username of the chat (channel/group).

Returns:
    The result of the API call.

### add_members

```python
add_members(self: 'darkob.Client', chat: str, members: Union[str, List[str]])
```

Add members to a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel/group.
    members (Union[str, List[str]]): The GUID(s) or username(s) of the member(s) to be added.

Returns:
    The result of the API call.

### archive_chat

```python
archive_chat(self: 'darkob.Client', chat: str)
```

Archive a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to archive.

Returns:
    The result of the API call.

### ban_member

```python
ban_member(self: 'darkob.Client', chat: str, member: str)
```

Ban a member from a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    member (str): The GUID or username of member to ban.

Returns:
    Result of the operation.

### ban_members

```python
ban_members(self: 'darkob.Client', chat: str, members: List[str])
```

Ban multiple members from a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    members (List[str]): List of GUIDs or usernames of members to ban.

Returns:
    Results of all operations.

### cancel_change_owner

```python
cancel_change_owner(self: 'darkob.Client', chat: str)
```

Cancels a pending ownership transfer request for a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the chat (channel/group).

Returns:
    The result of the API call.

### change_owner

```python
change_owner(self: 'darkob.Client', chat: str, new_owner: str)
```

Request to transfer ownership of a chat to another user.

Parameters:
    chat (str): The GUID, link, or username of the chat (channel/group).
    new_owner (str): The GUID or username of the user to become new owner.

Returns:
    The result of the API call.

Note:
    - Only works if you are the current owner
    - New owner must accept the request
    - Irreversible action

### check_join

```python
check_join(self: 'darkob.Client', chat: str, member: str)
```

Check if a user or bot is a member of a specific group or channel.

Parameters:
    chat (str): The GUID, link, or username of the chat to check.
    member (str): The GUID or username of the user/bot to check.

Returns:
    bool: True if user/bot is a member, False otherwise.

### clear_all_drafts

```python
clear_all_drafts(self: 'darkob.Client')
```

Clear all drafts.

Returns:
    The result of the API call.

### clear_black_list

```python
clear_black_list(self: 'darkob.Client', chat: str, exclude: Optional[Union[str, List[str]]]=None)
```

Clear black list with unban all banned members in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    exclude (Optional[Union[str, List[str]]]): Member GUID(s) or username(s) to exclude from unban. Default is None.

Returns:
    Result of unban operation.

### clear_chat_draft

```python
clear_chat_draft(self: 'darkob.Client', chat: str)
```

Clear the draft of a specific chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The result of the API call.

### click_chat_ads

```python
click_chat_ads(self: 'darkob.Client', chat_ads_id: str)
```

Register a click action on a chat ad.

The `chat_ads_id` is obtained from the `get_chat_ads` method.

Parameters:
    chat_ads_id (str): The chat ads ID to register a click on.

Returns:
    The result of the operation.

### click_keypad_button

```python
click_keypad_button(self: 'darkob.Client', chat: str, button_id: str)
```

Click a button in the chat keypad.

Parameters:
    chat (str): The GUID, link, or username of the chat (must be a bot).
    button_id (str): The button ID to click.

Returns:
    The result of the button click.

### create_join_link

```python
create_join_link(self: 'darkob.Client', chat: str, expire_time: Optional[int]=None, request_needed: bool=False, title: Optional[str]=None, usage_limit: int=0)
```

Creates an invite link for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the target group or channel.
    expire_time (Optional[int]): The expiration time of the link in seconds.
    request_needed (bool): Whether join requests must be approved manually.
    title (Optional[str]): A custom title for the invite link.
    usage_limit (int): The maximum number of times the link can be used.

Returns:
    The API response containing the created invite link.

### delete_all_avatars

```python
delete_all_avatars(self: 'darkob.Client', chat: str)
```

Delete all avatars from a chat or user profile.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    Data: Result of the operation.

Note:
    If `chat` is 'me', 'cloud', 'self', or 'myself', it will be replaced with the client's GUID.

### delete_avatar

```python
delete_avatar(self: 'darkob.Client', chat: str, avatar_id: str)
```

Delete an avatar.

Parameters:
    chat (str): The GUID, link, or username of the chat that owns the avatar.
    avatar_id (str): The identifier of the avatar to be deleted.

Returns:
    The result of the API call.

Note:
    If `chat` is 'me', 'cloud', 'self', or 'myself', it will be replaced with the client's GUID.

### delete_chat_history

```python
delete_chat_history(self: 'darkob.Client', chat: str)
```

Delete chat history up to the last message.

Parameters:
    chat (str): The GUID, link, or username of the chat (e.g., user, group).

Returns:
    The result of the API call.

### discard_voice_chat

```python
discard_voice_chat(self: 'darkob.Client', chat: str)
```

Discard/End a voice chat for a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel or group.

Returns:
    The result of the API call.

### dont_show_chat_ads

```python
dont_show_chat_ads(self: 'darkob.Client', chat_ads_id: str)
```

Register a 'don't show' action on a chat ad.

The `chat_ads_id` is obtained from the `get_chat_ads` method.

Parameters:
    chat_ads_id (str): The chat ads ID to hide.

Returns:
    The result of the operation.

### download_profile_picture

```python
download_profile_picture(self: 'darkob.Client', chat: Optional[str]=None, file_id: Optional[str]=None, access_hash_rec: Optional[str]=None, dc_id: Optional[str]=None, save_as: Optional[Union[str, bool]]=None, save_all: bool=False)
```

Download the profile picture of a user, group, or channel.

Parameters:
    chat (str, optional): The GUID, link, or username of the user, group, channel, or other chats.
    file_id (str, optional): Direct file_id for download without fetching avatars.
    access_hash_rec (str, optional): Direct access_hash_rec for download without fetching avatars.
    dc_id (str, optional): DC ID required when using file_id and access_hash_rec directly.
    save_as (str or bool, optional): Directory path to save the file(s). If True, saves in current directory. If None, returns bytes only.
    save_all (bool): If True, downloads all avatars instead of just the latest. Returns list of bytes if save_as is None.

Returns:
    bytes, List[bytes]: Binary data or saved file paths.

### edit_join_link

```python
edit_join_link(self: 'darkob.Client', chat: str, join_link: str, title: Optional[str]=None, expire_time: Optional[int]=None, request_needed: Optional[bool]=None, usage_limit: Optional[int]=None)
```

Edit an existing invite link for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the target group or channel.
    join_link (str): The join link to edit.
    expire_time (Optional[int]): The new expiration time of the link in seconds.
    request_needed (Optional[bool]): Whether join requests must be approved manually.
    title (Optional[str]): A new custom title for the invite link.
    usage_limit (Optional[int]): The new maximum number of times the link can be used.

Returns:
    The API response containing the edited invite link.

### get_all_drafts

```python
get_all_drafts(self: 'darkob.Client')
```

Get all saved message drafts.

Returns:
    The result of the API call containing all drafts.

### get_avatars

```python
get_avatars(self: 'darkob.Client', chat: str)
```

Get avatars of a specific chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to retrieve avatars for.

Returns:
    The result of the API call.

### get_banned_members

```python
get_banned_members(self: 'darkob.Client', chat: str, show_member_guids: bool=False)
```

Get a list of banned members in a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel or group.
    show_member_guids (bool, optional): Show member GUIDs in output. Default is False.

Returns:
    The result containing banned members with total count and optionally GUIDs.

### get_chat_ads

```python
get_chat_ads(self: 'darkob.Client', state: int=round(time()) - 150)
```

Retrieves advertising information for chats.

Parameters:
    state (int, optional): The timestamp state to filter chat ads. 
        Defaults to the current time minus 150 seconds.

Returns:
    The result of the API call.

### get_chat_info

```python
get_chat_info(self: 'darkob.Client', chat: str)
```

Get information about a user, group, or channel.

Parameters:
    chat (str): The GUID, link, or username of the chat (user, group, or channel).

Returns:
    The update containing information about the chat.

### get_chat_voice_chat

```python
get_chat_voice_chat(self: 'darkob.Client', chat: str)
```

Get the voice chat information for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.

Returns:
    The voice chat information.

### get_chats

```python
get_chats(self: 'darkob.Client', show_chat_guids: bool=False, auto_start_id: bool=True, start_id: str=None)
```

Get a list of all chats.

Parameters:
    show_chat_guids (bool, optional):
        If True, include chat GUIDs in the result.
        Default is False.
    auto_start_id (bool, optional):
        If True, automatically fetch all pages of chats.
        If False, only fetch one page using start_id.
        Default is True.
    start_id (str, optional):
        Starting chat ID for pagination.
        Only used when auto_start_id is False.

Returns:
    Data: The result containing chats with total count and optionally GUIDs.

### get_chats_info

```python
get_chats_info(self: 'darkob.Client', chats: Union[str, List[str]])
```

Get information about multiple chats by their GUIDs.

Parameters:
    chats (Union[str, List[str]]): A single chat (GUID, username, or link) or a list of them.

Returns:
    The result of the API call containing chats information.

### get_chats_updates

```python
get_chats_updates(self: 'darkob.Client', state: Optional[Union[str, int]]=None)
```

Get updates for chats.

Parameters:
    state (Optional[Union[str, int]]): State parameter for syncing updates. If not provided,
        it uses the current time minus 150 seconds.

Returns:
    The result of the API call.

### get_guid

```python
get_guid(self: 'darkob.Client', chat: str)
```

Retrieves the GUID of a user, group, channel, or bot.

Parameters:
    chat (str): The username, group link, channel link, or bot username.

Returns:
    str: The GUID of the chat.

### get_info_by_link

```python
get_info_by_link(self: 'darkob.Client', link: str)
```

Get group or channel preview by join link.

Parameters:
    link (str): The join link.

Returns:
    The result of the API call.

### get_info_by_username

```python
get_info_by_username(self: 'darkob.Client', username: str)
```

Get an chat (user, bot, or channel) by its username.

Parameters:
    username (str): The username of the chat.

Returns:
    The result of the API call.

### get_join_links

```python
get_join_links(self: 'darkob.Client', chat: str, creator: str=None)
```

Retrieves a list of join links for a specific group or channel.

Parameters:
    chat (str): The GUID, link, or username of the target group or channel.

Returns:
    The API response containing the join links.

### get_join_requests

```python
get_join_requests(self: 'darkob.Client', chat: str, show_user_guids: bool=False)
```

Get a list of join requests in a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel or group.
    show_user_guids (bool, optional): Show user GUIDs in output. Default is False.

Returns:
    Data: The result containing all join requests with total count.

### get_my_guid

```python
get_my_guid(self: 'darkob.Client')
```

Get the GUID of the currently authenticated user.

Returns:
    str: The user's GUID.

### get_pending_owner

```python
get_pending_owner(self: 'darkob.Client', chat: str)
```

Retrieves the pending owner information for a specified chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    An update chat containing details about the
        pending owner of the specified chat.

### get_profile_link_items

```python
get_profile_link_items(self: 'darkob.Client', chat: str)
```

Get profile link items for a given chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The result of the API call.

### get_related_chats

```python
get_related_chats(self: 'darkob.Client', chat: str)
```

Get related chats for a given chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The result of the API call.

### get_voice_chat_participants

```python
get_voice_chat_participants(self: 'darkob.Client', chat: str, show_user_guids: bool=False)
```

Get list of participants in a voice chat.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    show_user_guids (bool, optional): Show user GUIDs in output. Default is False.

Returns:
    The result containing all voice chat participants with total count.

### get_voice_chat_updates

```python
get_voice_chat_updates(self: 'darkob.Client', chat: str, state: int=None)
```

Get voice chat updates for a group.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    state (int, optional): The state for updates. If not provided, it defaults to the current time minus 150 seconds.

Returns:
    Update group containing the voice chat updates.

### heartbeat

```python
heartbeat(self: 'darkob.Client', chat_guid: str)
```

_No docstring available._

### join_chat

```python
join_chat(self: 'darkob.Client', chat: str)
```

Join a chat (channel or group).

Parameters:
    chat (str): The GUID, link, or username of the chat (channel or group).

Returns:
    The result of the API call.

### join_voice_chat

```python
join_voice_chat(self: 'darkob.Client', chat: str, sdp_offer_data: str | None = None)
```

Join to the group | channel voice chat.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    sdp_offer_data (str, optional): SDP offer data. If not provided, uses default.

Returns:
    The result of the API call.

### leave_chat

```python
leave_chat(self: 'darkob.Client', chat: str)
```

Leave a chat (channel or group).

Parameters:
    chat (str): The GUID, link, or username of the chat (channel or group).

Returns:
    The result of the API call.

### leave_voice_chat

```python
leave_voice_chat(self: 'darkob.Client', chat: str)
```

Leave a voice chat in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.

Returns:
    The result of the API call.

### member_is_admin

```python
member_is_admin(self: 'darkob.Client', chat: str, member: str)
```

Checks if a member is an admin in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    member (str): The GUID or username of the member.

Returns:
    bool: True if the user is an admin, False otherwise.

### mute_chat

```python
mute_chat(self: 'darkob.Client', chat: str, duration: Union[int, timedelta]=None)
```

Mute a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to mute.
    duration (Union[int, timedelta], optional): Duration of mute.
        - int: seconds, must be at least 1800 (30 minutes).
        - timedelta: e.g., timedelta(hours=1), timedelta(minutes=30).
        Defaults to None (permanent mute).

Returns:
    Result of the operation.

### pin_chat

```python
pin_chat(self: 'darkob.Client', chat: str)
```

Pin a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to pin.

Returns:
    Result of the operation.

### pin_chat_in_folder

```python
pin_chat_in_folder(self: 'darkob.Client', chat: str, folder_id: str)
```

Pin a chat in a folder.

Parameters:
    chat (str): The GUID, link, or username of the chat to pin.
    folder_id (str): The folder ID to pin the chat in.

Returns:
    The result of the API call.

### play_voice_chat

```python
play_voice_chat(self: 'darkob.Client', chat: str, media: pathlib.Path)
```

Plays voice media in a chat.

Parameters:
    chat: The GUID, link, or username of the chat to play the voice media in.
    media: The path to the voice media file.

### reject_join_request

```python
reject_join_request(self: 'darkob.Client', chat: str, user: str)
```

Reject a join request for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    user (str): The user GUID or username of the requester.

Returns:
    The result of the API call.

### reject_ownership_request

```python
reject_ownership_request(self: 'darkob.Client', chat: str)
```

Reject an ownership transfer request.

Parameters:
    chat (str): The GUID, link, or username of the chat (channel/group).

Returns:
    The result of the API call.

### report_chat

```python
report_chat(self: 'darkob.Client', chat: str, report_type: Union[int, str], description: Optional[str]=None)
```

Report a chat (user, channel, group, etc.) for a specific reason.

Parameters:
    chat (str): The GUID, link, or username of the chat to be reported.
    report_type (Union[int, str]): The report reason.
        Can be:
            - Integer code between 100 and 106
            - String name (case-insensitive): 'Other', 'Violence',
              'Spam', 'Porn', 'ChildAbuse', 'Copyright', 'Fraud'
        If set to 100 (Other), `description` becomes required.
    description (Optional[str]): Description for the report.
        Required when `report_type` is 100 (Other).

Returns:
    The result of the API call.

### report_chat_ads

```python
report_chat_ads(self: 'darkob.Client', chat_ads_id: str)
```

Register a report action on a chat ad.

The `chat_ads_id` is obtained from the `get_chat_ads` method.

Parameters:
    chat_ads_id (str): The chat ads ID to report.

Returns:
    The result of the operation.

### revoke_join_link

```python
revoke_join_link(self: 'darkob.Client', chat: str, join_link: str)
```

Revoke a invite link for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    join_link (str): The join link to revoke.

Returns:
    The result of the API call.

### search_global_chats

```python
search_global_chats(self: 'darkob.Client', text: str, filter_type: Optional[Union[str, List[str]]]=None, start_id: Optional[str]=None)
```

Search for global chats (users, channels, etc.) based on the given search text.

Parameters:
    text (str): The text to search for.
    filter_type (str or list, optional): Filter results by type. 
        'User', 'Channel', 'Bot' or a list of them.
    start_id (str, optional): The ID to start fetching from. Defaults to None.

Returns:
    The update containing search results.

### seen_chats

```python
seen_chats(self: 'darkob.Client', seen_list: dict)
```

Marks multiple chats as seen.

Parameters:
    seen_list (dict): A dictionary containing chat GUIDs and their last seen message IDs.

Returns:
    The result of the operation.

### send_chat_activity

```python
send_chat_activity(self: 'darkob.Client', chat: str, activity: Literal['Typing', 'Recording', 'Uploading']='Typing')
```

Sends a chat activity, such as typing, uploading, or recording.

Parameters:
    chat (str): The GUID, link, or username of the group/user.
    activity (str, optional): The type of activity. Defaults to 'Typing'.

Returns:
    The result of the operation.

Raises:
    InvalidInput: If the `activity` argument is not one of `"Typing", "Uploading", or "Recording"`.

### send_voice_chat_activity

```python
send_voice_chat_activity(self: 'darkob.Client', chat: str, activity: Literal['Speaking']='Speaking', participant_chat_guid: str=None)
```

Set voice chat activity automatically.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    activity (str): Literal['Speaking'] and Default is `Speaking`.
    participant_chat_guid (str): Participant chat guid, Default is `self.guid`.

Returns:
    The result of the API call.

### set_admin

```python
set_admin(self: 'darkob.Client', chat: str, member: str, access: Union[List[str], str]=[], custom_title: str='')
```

Set a member as admin in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    member (str): The GUID or username of member to set as admin.
    access (Union[List[str], str]): List of allowed permissions or single permission string.
        Can also be 'all' or 'All' to grant all permissions.
    custom_title (str): Custom title for admin in groups. (optional)

Returns:
    Result of the operation.

### set_ask_spam

```python
set_ask_spam(self: 'darkob.Client', chat: str, action: Literal['AddToContact', 'BlockUser', 'Cancel', 'ReportAndLeave']='Cancel')
```

Perform an action for a pending spam request.

Parameters:
    chat (str): The GUID, link, or username of the user, group, or channel.
    action (str): The action to apply:
        - For user (u0): 'AddToContact', 'BlockUser', 'Cancel'.
        - For group/channel (g0/c0): 'ReportAndLeave'.

Returns:
    The result of the API call.

### set_chat_auto_delete

```python
set_chat_auto_delete(self: 'darkob.Client', chat: Union[str, List[str]], auto_delete: Union[str, int])
```

Set auto-delete timer for one or more groups or channels.

Parameters:
    chat (Union[str, List[str]]): The GUID, link, username of a group/channel, or a list of them.
    auto_delete (Union[str, int]): Auto-delete duration. Accepts:
        - Integer: 1-365 (days)
        - String: '1m'-'60m', '1h'-'24h', '1d'-'365d', '1w'-'52w', '1y', 'off'
        - Common words: 'day', 'week', 'month', 'year', 'never', 'disabled'

Returns:
    The result of the API call.

### set_chat_protected_content

```python
set_chat_protected_content(self: 'darkob.Client', chat: str, enabled: bool)
```

Set the chat protected content setting.

Parameters:
    chat (int): The GUID or username of the target chat.
    enabled (bool): Pass True to enable the protected content setting, False to disable.

Returns:
    The result of the API call.

### set_chat_use_time

```python
set_chat_use_time(self: 'darkob.Client', chat: str, use_time: int)
```

Send chat usage time to the server.

This helps the server recognize natural user behavior
and can reduce rate limiting and bot detection.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    use_time (int): Time spent in the chat in seconds.

Returns:
    The result of the API call.

### set_voice_chat_setting

```python
set_voice_chat_setting(self: 'darkob.Client', chat: str, title: str=None, join_muted: bool=None)
```

Set voice chat settings for group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    title (str, optional): New title for voice chat.
    join_muted (bool, optional): Whether new participants join muted. (Only for groups)

Returns:
    The result of the API call.

### set_voice_chat_state

```python
set_voice_chat_state(self: 'darkob.Client', chat: str, action: typing.Literal['Mute', 'Unmute', 'RequestSpeak', 'CancelRequestSpeak']='Unmute', participant_chat_guid: str=None)
```

Set group or channel voice chat state automatically.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    action (str): Literal['Mute', 'Unmute'] and Default is `Unmute`.
    participant_chat_guid (str): Participant chat guid, Default is `self.guid`.

Returns:
    The result of the API call.

### speaking

```python
speaking(self: 'darkob.Client', chat_guid: str)
```

_No docstring available._

### start_voice_chat

```python
start_voice_chat(self: 'darkob.Client', chat: str)
```

Start a voice chat for a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel/group.

Returns:
    The result of the API call.

### unarchive_chat

```python
unarchive_chat(self: 'darkob.Client', chat: str)
```

Unarchive a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to unarchive.

Returns:
    Result of the operation.

### unban_all_members

```python
unban_all_members(self: 'darkob.Client', chat: str, exclude: Optional[Union[str, List[str]]]=None)
```

Unban all banned members in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    exclude (Optional[Union[str, List[str]]]): Member GUID(s) or username(s) to exclude from unban. Default is None.

Returns:
    Result of unban operation.

### unban_member

```python
unban_member(self: 'darkob.Client', chat: str, member: str)
```

Unban a member from a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    member (str): The GUID or username of member to unban.

Returns:
    Result of the operation.

### unban_members

```python
unban_members(self: 'darkob.Client', chat: str, members: List[str])
```

Unban multiple members from a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    members (List[str]): List of GUIDs or usernames of members to unban.

Returns:
    Results of all operations.

### unmute_chat

```python
unmute_chat(self: 'darkob.Client', chat: str)
```

Unmute a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to unmute.

Returns:
    Result of the operation.

### unpin_chat

```python
unpin_chat(self: 'darkob.Client', chat: str)
```

Unpin a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to unpin.

Returns:
    Result of the operation.

### unpin_chat_in_folder

```python
unpin_chat_in_folder(self: 'darkob.Client', chat: str, folder_id: str)
```

Unpin a chat from a folder.

Parameters:
    chat (str): The GUID, link, or username of the chat to unpin.
    folder_id (str): The folder ID to unpin the chat from.

Returns:
    The result of the API call.

### unset_admin

```python
unset_admin(self: 'darkob.Client', chat: str, member: str)
```

Unset a member as admin in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    member (str): The GUID or username of member to unset as admin.

Returns:
    Result of the operation.

### upload_avatar

```python
upload_avatar(self: 'darkob.Client', chat: str, main_image: Union[Path, str, bytes], thumbnail_image: Optional[Union[Path, str, bytes]]=None, *args, **kwargs)
```

Uploads an avatar image for a specified chat (user, group, or channel).

Parameters:
    chat (str): The GUID, link, or username of the chat for which the avatar is being uploaded.
    main_image (Union[Path, str, bytes]): The image file or bytes to be used as the avatar.
    thumbnail_image (Optional[Union[Path, str, bytes]]): The image file or bytes of the thumbnail image.

Returns:
    The result of the avatar upload operation.

Note:
    If `chat` is 'me', 'cloud', or 'self', it will be replaced with the client's GUID.
    If `main_image` is a string or Path (path to a file), the file name is extracted from the path.
        Otherwise, a default file name ('darkob.jpg') is used.
    The `upload_file` method is used internally to handle the file upload process.

### view_chat_ads

```python
view_chat_ads(self: 'darkob.Client', chat_ads_id: str)
```

Register a view action on a chat ad.

The `chat_ads_id` is obtained from the `get_chat_ads` method.

Parameters:
    chat_ads_id (str): The chat ads ID to register a view on.

Returns:
    The result of the operation.

## groups

### create_group

```python
create_group(self: 'darkob.Client', title: str, members: Union[str, List[str]], description: Optional[str]=None, avatar: Optional[Union[Path, str, bytes]]=None, thumbnail_avatar: Optional[Union[Path, str, bytes]]=None, *args, **kwargs)
```

Create a new group.

Parameters:
    title (str): The title of the group.
    members (Union[str, List[str]]): A single member GUID/Username or a list of member GUIDs/Usernames to be added to the group.
    description (Optional[str]): Description of the group (optional). Defaults to None.
    avatar (Optional[Union[Path, str, bytes]]): The image to be used as the group avatar. Default is None.
    thumbnail_avatar (Optional[Union[Path, str, bytes]]): The image to be used as the group thumbnail avatar. Default is None.

Returns:
    The result of the API call.

Note:
    If only `avatar` is provided, the thumbnail is taken from the same image.
    If none of them are provided, no avatar is set for the group.

### delete_group

```python
delete_group(self: 'darkob.Client', group: str, confirm: bool=True)
```

Delete a group.

Parameters:
    group (str): The GUID or link of the group.
    confirm (bool): If True, ask the user for confirmation before
        deleting the group. If False, delete immediately.
        Default is True.

Returns:
    The result of the API call.
    Exits if cancelled.

### edit_group_info

```python
edit_group_info(self: 'darkob.Client', group: str, title: Optional[str]=None, description: Optional[str]=None, slow_mode: Optional[str]=None, event_messages: Optional[bool]=None, is_restricted_content: Optional[bool]=None, reactions: Optional[Union[Literal['All', 'Disable'], List[int]]]=None, chat_history_for_new_members: Optional[str]=None, restricted_period: Optional[List[Dict[str, Union[List[str], str]]]]=None)
```

Edit the information of a group.

Parameters:
    group (str): The GUID or link of the group.
    title (Optional[str]): The new title for the group (max 60 characters).
    description (Optional[str]): The new description for the group (max 300 characters).
    slow_mode (Optional[str]): The new slow mode setting for the group.
    event_messages (Optional[bool]): Enable or disable event messages for the group.
    is_restricted_content (Optional[bool]): Restrict content (prevent screenshots and file saving).
    reactions (Union[Literal['All', 'Disable'], List[int]], optional): 
        - 'All': Enable all reactions
        - 'Disable': Disable all reactions
        - List[int]: List of reaction IDs to enable (e.g., [1, 2, 6, 7, 8, 23, 44])
    chat_history_for_new_members (Optional[str]): The new chat history setting for new members.
    restricted_period (Optional[List[Dict[str, Union[List[str], str]]]]): 
        Time restrictions for sending messages (list of periods). Each period should contain:
        - days_of_week: List of days ['Saturday', 'Sunday', ..., 'Friday']
        - from_time: Start time in "HH:MM" format (24-hour)
        - to_time: End time in "HH:MM" format (24-hour)
        Note: Can accept multiple periods as a list of dictionaries.

Returns:
    The result of the API call.

Examples:
    # Enable all reactions
    await client.edit_group_info(
        group="g0...",
        reactions="All"
    )

    # Disable all reactions
    await client.edit_group_info(
        group="g0...",
        reactions="Disable"
    )

    # Enable specific reactions
    await client.edit_group_info(
        group="g0...",
        reactions=[1, 2, 6, 7, 8, 23, 44]
    )

    # Single restricted period
    await client.edit_group_info(
        group="g0...",
        restricted_period=[{
            "days_of_week": ["Saturday", "Sunday"],
            "from_time": "00:00",
            "to_time": "06:00"
        }]
    )

    # Multiple restricted periods
    await client.edit_group_info(
        group="g0...",
        restricted_period=[
            {
                "days_of_week": ["Saturday", "Sunday", "Monday"],
                "from_time": "01:13",
                "to_time": "08:16"
            },
            {
                "days_of_week": ["Tuesday", "Wednesday"],
                "from_time": "22:00",
                "to_time": "04:00"  # Can cross midnight
            }
        ]
    )

### edit_group_timer

```python
edit_group_timer(self: 'darkob.Client', group: str, timer: typing.Union[str, int])
```

Parameters:
    group (str): The GUID or link of the group.
    timer (Union[str, int]): The new slow mode setting for the group.

Returns:
    The result of the API call.

### edit_group_title

```python
edit_group_title(self: 'darkob.Client', group: str, title: str)
```

Edit title of a group.

Parameters:
    group (str): The GUID or link of the group.
    title (str): The new title of the group.

Returns:
    The result of the API call.

### edit_slow_mode

```python
edit_slow_mode(self: 'darkob.Client', group: str, slow_mode: typing.Union[str, int])
```

Parameters:
    group (str): The GUID or link of the group.
    slow_mode (Union[str, int]): The new slow mode setting for the group.

Returns:
    The result of the API call.

### get_group_admin_access

```python
get_group_admin_access(self: 'darkob.Client', group: str, admin: str)
```

Get the admin access for a member in a group.

Parameters:
    group (str): The GUID or link of the group.
    admin (str): The GUID or username of the admin for whom admin access is being checked.

Returns:
    The result of the API call.

### get_group_admins

```python
get_group_admins(self: 'darkob.Client', group: str, show_admin_guids: bool=False)
```

Get the list of admins in a group.

Parameters:
    group (str): The GUID, link, or username of the group.
    show_admin_guids (bool, optional): Show admin GUIDs in output. Default is False.

Returns:
    Result containing all admins with total count.

### get_group_default_access

```python
get_group_default_access(self: 'darkob.Client', group: str)
```

Get the default access settings for a group.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### get_group_info

```python
get_group_info(self: 'darkob.Client', group: str)
```

Get information about a group.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### get_group_link

```python
get_group_link(self: 'darkob.Client', group: str)
```

Get the link associated with a group.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### get_group_members

```python
get_group_members(self: 'darkob.Client', group: str, search_text: str=None, start_id: str=None)
```

Get members of a group.

Parameters:
    group (str): The GUID or link of the group.
    search_text (str, optional): Search text for filtering members. Defaults to None.
    start_id (str, optional): The starting ID for pagination. Defaults to None.

Returns:
    The result of the API call.

### get_group_mention_list

```python
get_group_mention_list(self: 'darkob.Client', group: str, search_mention: str=None)
```

Get the mention list for a group.

Parameters:
    group (str): The GUID or link of the group.
    search_mention (str, optional): Search text for mentions.

Returns:
    The result of the API call.

### get_group_message_read_participants

```python
get_group_message_read_participants(self: 'darkob.Client', group: str, message_id: Union[str, int])
```

Get list of participants who have read a specific message in a group.

Parameters:
    group (str): The GUID or link of the group.
    message_id (Union[str, int]): The ID of the message.

Returns:
    The result of the API call containing read participants.

### get_group_online_count

```python
get_group_online_count(self: 'darkob.Client', group: str)
```

Retrieves the number of online members in a specified group.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### get_unread_mentions

```python
get_unread_mentions(self: 'darkob.Client', group: str, max_id: Union[str, int], min_id: Union[str, int], sort: str=None)
```

Get unread mentions in a group.

Parameters:
    group (str): The GUID or link of the group.
    max_id (Union[str, int]): Maximum message ID.
    min_id (Union[str, int]): Minimum message ID.
    sort (str, optional): Sort order. Defaults to None.

Returns:
    The result of the API call containing unread mentions.

### join_group

```python
join_group(self: 'darkob.Client', group: str)
```

Join a group using the provided link.

Parameters:
    group (str): The group link.

Returns:
    The result of the API call.

### leave_group

```python
leave_group(self: 'darkob.Client', group: str)
```

Leave a group.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### lock_group

```python
lock_group(self: 'darkob.Client', group: str)
```

Lock a group by disabling SendMessage access.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    Result message.

### set_group_default_access

```python
set_group_default_access(self: 'darkob.Client', group: str, access: Union[str, list])
```

Set default access for a group.

Parameters:
    group (str): The GUID or link of the group.
    access (Union[str, list]): List of allowed actions. Must be one or more of:
        - "ViewMembers": Allows viewing group members.
        - "ViewAdmins": Allows viewing group admins.
        - "SendMessages": Allows sending messages.
        - "AddMember": Allows adding members.
        If only specific actions are listed (e.g. ["SendMessages"]), ONLY those are enabled and others are disabled.
        If empty list "[]", ALL access permissions are disabled/closed.

Returns:
    The result of the API call.

### set_group_link

```python
set_group_link(self: 'darkob.Client', group: str)
```

Set private link for group.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### unlock_group

```python
unlock_group(self: 'darkob.Client', group: str)
```

Unlock a group by enabling SendMessage access.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    Result message.

## channels

### check_channel_username

```python
check_channel_username(self: 'darkob.Client', username: str)
```

Check the availability of a username for a channel.

Parameters:
    username (str): The username to check.

Returns:
    The result of the API call.

### create_channel

```python
create_channel(self: 'darkob.Client', title: str, members: Optional[Union[str, list]]=None, channel_type: str='Public', description: Optional[str]=None, avatar: Optional[Union[Path, str, bytes]]=None, thumbnail_avatar: Optional[Union[Path, str, bytes]]=None, *args, **kwargs)
```

Create a new channel.

Parameters:
    title (str): The title of the new channel.
    members (Union[str, list], optional): The GUID(s) or username(s) of the member(s) to be added to the new channel. Default is None.
    channel_type (str): Set type of the channel. 'Public' or 'Private'. Default is 'Public'.
    description (str, optional): The description of the new channel. Default is None.
    avatar (Optional[Union[Path, str, bytes]]): The image to be used as the channel avatar. Default is None.
    thumbnail_avatar (Optional[Union[Path, str, bytes]]): The image to be used as the channel thumbnail avatar. Default is None.

Returns:
    The result of the API call.

Note:
    If only `avatar` is provided, the thumbnail is taken from the same image.
    If none of them are provided, no avatar is set for the channel.

### delete_channel

```python
delete_channel(self: 'darkob.Client', channel: str, confirm: bool=True)
```

Delete a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    confirm (bool): If True, ask the user for confirmation before
        deleting the channel. If False, delete immediately.
        Default is True.

Returns:
    The result of the API call.
    Exits if cancelled.

### edit_channel_info

```python
edit_channel_info(self: 'darkob.Client', channel: str, title: Optional[str]=None, description: Optional[str]=None, username: Optional[str]=None, channel_type: Literal['Public', 'Private']=None, sign_messages: Optional[bool]=None, is_restricted_content: Optional[bool]=None, reactions: Optional[Union[Literal['All', 'Disable'], List[int]]]=None)
```

Edit information of a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    title (str, optional): The new title of the channel. Max 60 characters.
    description (str, optional): The new description of the channel. Max 300 characters.
    username (str, optional): The new username of the channel. Max 32 characters.
    channel_type (str, optional): The new type of the channel. 'Public' or 'Private'.
    sign_messages (bool, optional): Whether to sign messages in the channel.
    is_restricted_content (bool, optional): Restrict content (prevent screenshots and file saving).
    reactions (Union[Literal['All', 'Disable'], List[int]], optional): 
        - 'All': Enable all reactions
        - 'Disable': Disable all reactions
        - List[int]: List of reaction IDs to enable (e.g., [1, 2, 6, 7, 8, 23, 44])

Returns:
    The result of the API call.

### edit_channel_title

```python
edit_channel_title(self: 'darkob.Client', channel: str, title: str)
```

Edit title of a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    title (str): The new title of the channel.

Returns:
    The result of the API call.

### get_channel_admin_access

```python
get_channel_admin_access(self: 'darkob.Client', channel: str, admin: str)
```

Get the admin access list for a specific member in a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    admin (str): The GUID or username of the admin for whom admin access is being checked.

Returns:
    The result of the API call.

### get_channel_admins

```python
get_channel_admins(self: 'darkob.Client', channel: str, show_admin_guids: bool=False)
```

Get the list of admins in a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    show_admin_guids (bool, optional): Show member GUIDs in output. Default is False.

Returns:
    Result containing all admins with total count and optionally member_guids.

### get_channel_info

```python
get_channel_info(self: 'darkob.Client', channel: str)
```

Get information about a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.

Returns:
    The result of the API call.

### get_channel_link

```python
get_channel_link(self: 'darkob.Client', channel: str)
```

Get the join link of a channel.

Parameters:
    channel (str): The GUID of the channel.

Returns:
    The result of the API call.

### get_channel_members

```python
get_channel_members(self: 'darkob.Client', channel: str, search_text: str=None, start_id: str=None)
```

Get members in a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    search_text (str, optional): Text to search for in members. Defaults to None.
    start_id (str, optional): The ID to start fetching from. Defaults to None.

Returns:
    The result of the API call.

### get_channel_post_by_link

```python
get_channel_post_by_link(self: 'darkob.Client', url: str)
```

Retrieves channel post by application URL.

Parameters:
    url (str): The channel post URL.

Returns:
    Channel info and message data.

### get_channel_seen_count

```python
get_channel_seen_count(self: 'darkob.Client', channel: str, min_id: Union[str, int], max_id=Union[str, int])
```

Get the view count of a channel within a specific message ID range.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    min_id (Union[str, int]): Minimum message ID in the range (inclusive).
    max_id (Union[str, int]): Maximum message ID in the range (inclusive).

Returns:
    The result of the API call.

### get_channel_statistics

```python
get_channel_statistics(self: 'darkob.Client', channel: str)
```

Get all statistics for a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.

Returns:
    The result of the API call containing channel statistics.

### get_post_by_ask_link

```python
get_post_by_ask_link(self: 'darkob.Client', url: str)
```

Retrieves channel post by ask_join_link (go.rubika.ir link).

Parameters:
    url (str): The go.rubika.ir link.

Returns:
    Channel info and message data.

### join_channel

```python
join_channel(self: 'darkob.Client', channel: str)
```

Join a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.

Returns:
    Result of the API call.

### leave_channel

```python
leave_channel(self: 'darkob.Client', channel: str)
```

Leave a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.

Returns:
    The result of the API call.

### seen_channel_messages

```python
seen_channel_messages(self: 'darkob.Client', channel: str, min_id: Union[int, str], max_id: Union[int, str])
```

Mark channel messages as seen within a specific range.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    min_id (Union[int, str]): The minimum message ID to mark as seen.
    max_id (Union[int, str]): The maximum message ID to mark as seen.

Returns:
    The result of the API call.

### set_channel_link

```python
set_channel_link(self: 'darkob.Client', channel: str)
```

Set a custom link for the channel.

Parameters:
    channel (str): The GUID of the channel.

Returns:
    The result of the API call.

### set_channel_type

```python
set_channel_type(self: 'darkob.Client', channel: str, channel_type: typing.Literal['Public', 'Private'])
```

Set type of a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    channel_type (str): The new type of the channel. 'Public' or 'Private'.

Returns:
    The result of the API call.

### update_channel_username

```python
update_channel_username(self: 'darkob.Client', channel: str, username: str)
```

Update the username of a channel.

Parameters:
    channel (str): The GUID or username of the channel.
    username (str): The new username for the channel.
        Must be between 7 and 32 characters
        Can only contain English letters (a-z, A-Z), numbers (0-9), and underscore (_)
        Should not start with number or underscore
        Should not end with underscore

Returns:
    The result of the API call.

## users

### add_contact

```python
add_contact(self: 'darkob.Client', phone_number: Union[str, int], first_name: str, last_name: str='')
```

Adds a contact to the client's address book.

Parameters:
    phone_number (str): The phone number of the contact to be added.
    first_name (str): The first name of the contact.
    last_name (str, optional): The last name of the contact. Defaults to an empty string.

Returns:
    The result of the API call.

Note:
    The `phone_number` parameter should be a valid phone number.
    The `first_name` and `last_name` parameters represent the name of the contact.
    If the contact has no last name, `last_name` can be an empty string.

### block_user

```python
block_user(self: 'darkob.Client', user: str)
```

Block a user.

Parameters:
    user (str): The GUID or username of the user to block.

Returns:
    The result of the block operation.

### check_user_username

```python
check_user_username(self: 'darkob.Client', username: str)
```

Check the availability of a username for a user.

Parameters:
    username (str): The username to be checked.

Returns:
    The result of the username availability check.

### delete_contact

```python
delete_contact(self: 'darkob.Client', user: str)
```

Deletes a contact from the client's address book.

Parameters:
    user (str): The GUID or username of the contact to be deleted.

Returns:
    The result of the contact deletion operation.

Note:
    - The `user` parameter should be the GUID or username of the contact to be deleted.

### delete_user_chat

```python
delete_user_chat(self: 'darkob.Client', user: str)
```

Delete a user chat.

Parameters:
    user (str): The GUID or username of the user whose chat is to be deleted.

Returns:
    The result of the user chat deletion.

### discard_call

```python
discard_call(self: 'darkob.Client', call_id: str, duration: int=0, reason: str='Disconnect')
```

Discard/end an active call.

Parameters:
    call_id (str): ID of the call to discard
    duration (int): Call duration in seconds
    reason (str): Reason for ending the call.
        Common options: 'Missed' and 'Disconnect'.
        Default: 'Disconnect'

Returns:
    Result of the discard operation.

### get_blocked_users

```python
get_blocked_users(self: 'darkob.Client', show_user_guids: bool=False)
```

Get a list of all blocked users.

Parameters:
    show_user_guids (bool, optional): Show user GUIDs in output. Default is False.

Returns:
    The result containing all blocked users with total count.

### get_common_groups

```python
get_common_groups(self: 'darkob.Client', user: str)
```

Get groups in common with a user.

Parameters:
    user (str): User's GUID/username.

Returns:
    Common groups list.

### get_contacts

```python
get_contacts(self: 'darkob.Client', show_user_guids: bool=False)
```

Get a list of all contacts.

Parameters:
    show_user_guids (bool, optional): Show user GUIDs in output.
        Default is False.

Returns:
    The result containing all contacts with total count.

### get_contacts_last_online

```python
get_contacts_last_online(self: 'darkob.Client', users: Union[str, List[str]])
```

Get the last online status of multiple users.

Parameters:
    users (Union[str, List[str]]): The GUID(s) or username(s) of the contacts.

Returns:
    Last online status for each user.

### get_contacts_stories

```python
get_contacts_stories(self: 'darkob.Client')
```

Get stories from contacts in the chat page.

Returns:
    The result of the API call containing contacts stories.

### get_contacts_updates

```python
get_contacts_updates(self: 'darkob.Client', state: Optional[Union[str, int]]=round(time()) - 150)
```

Get updates related to contacts.

Parameters:
    state (Optional[Union[str, int]], optional):
        The state parameter to filter updates. Defaults to `round(time()) - 150`.

Returns:
    The update related to contacts.

### get_last_online

```python
get_last_online(self: 'darkob.Client', user: str)
```

Get the last online status of a user.

Parameters:
    user (str): The GUID, link, or username of the user.

Returns:
    Last online status with details.

### get_me

```python
get_me(self: 'darkob.Client', refresh: bool=False, ttl: float=300.0)
```

Get information about the authenticated user.

The result is cached for ``ttl`` seconds (default 5 minutes),
because profile reads are frequent and rarely change. Pass
``refresh=True`` to force a new request.

Parameters:
    refresh (bool): Ignore the cache. Defaults to False.
    ttl (float): Cache lifetime in seconds. Defaults to 300.

Returns:
    Information about the authenticated user.

### get_saved_music_playlist

```python
get_saved_music_playlist(self: 'darkob.Client', user: str)
```

Get the saved music playlist of a user.

Parameters:
    user (str): The GUID or username of the user.

Returns:
    The result of the API call containing saved music playlist.

### get_top_users

```python
get_top_users(self: 'darkob.Client')
```

Get list of top users.

Returns:
    List of top users.

### get_user_info

```python
get_user_info(self: 'darkob.Client', user: str=None)
```

Get information about a specific user.

Parameters:
    user (str): The GUID or username of the user.

Returns:
    Information about the specified user.

### remove_from_top_users

```python
remove_from_top_users(self: 'darkob.Client', user: str)
```

Remove user from top users list.

Parameters:
    user (str): The user GUID or username to remove.

Returns:
    The result of the API call.

### request_video_call

```python
request_video_call(self: 'darkob.Client', user: str, library_versions: Optional[List[str]]=None, max_layer: int=92, min_layer: int=65, sip_version: int=1, support_call_out: bool=True)
```

Request a video call with a user.

Parameters:
    user (str): The GUID or username of the user to call.
    library_versions (List[str], optional): List of supported library versions. Default: ['2.7.7', '2.4.4']
    max_layer (int): Maximum protocol layer. Default: 92
    min_layer (int): Minimum protocol layer. Default: 65
    sip_version (int): SIP version. Default: 1
    support_call_out (bool): Support outgoing calls. Default: True

Returns:
    Call request result containing session info.

### request_voice_call

```python
request_voice_call(self: 'darkob.Client', user: str, library_versions: Optional[List[str]]=None, max_layer: int=92, min_layer: int=65, sip_version: int=1, support_call_out: bool=True)
```

Request a voice call with a user.

Parameters:
    user (str): The GUID or username of the user to call.
    library_versions (List[str], optional): List of supported library versions. Default: ['2.7.7', '2.4.4']
    max_layer (int): Maximum protocol layer. Default: 92
    min_layer (int): Minimum protocol layer. Default: 65
    sip_version (int): SIP version. Default: 1
    support_call_out (bool): Support outgoing calls. Default: True

Returns:
    Call request result containing session info.

### reset_contacts

```python
reset_contacts(self: 'darkob.Client')
```

Reset all saved contacts for the authenticated user.

This method clears the entire contact list on the server side.

Returns:
    The result of the API call.

### unblock_all_users

```python
unblock_all_users(self: 'darkob.Client', exclude: Optional[Union[str, List[str]]]=None)
```

Unblock all blocked users.

Parameters:
    exclude (Optional[Union[str, List[str]]]): User GUID(s) or username(s) to exclude from unblock. Default is None.

Returns:
    Result of unblock operation.

### unblock_user

```python
unblock_user(self: 'darkob.Client', user: str)
```

Unblock a user.

Parameters:
    user (str): The GUID or username of the user to unblock.

Returns:
    The result of the unblock operation.

## settings

### abort_two_step_setup

```python
abort_two_step_setup(self: 'darkob.Client')
```

Abort the two-step verification setup process.

Returns:
    The result of the operation.

### add_folder

```python
add_folder(self: 'darkob.Client', name: str, include_chats: Optional[Union[str, List[str]]]=None, exclude_chats: Optional[Union[str, List[str]]]=None, include_chat_types: Optional[List[str]]=None, exclude_chat_types: Optional[List[str]]=None, is_add_to_top: bool=True, suggestion_folder_id: str=None, folder_id: str=None)
```

Add a new folder to organize chats.

Parameters:
    name (str): Folder name.
    include_chats: Chats (GUIDs, links, usernames) to include in folder.
    exclude_chats: Chats (GUIDs, links, usernames) to exclude from folder.
    include_chat_types: Chat types to include (case-insensitive).
        Valid values:
            'Contacts', 'NonContacts' / 'Users', 'Groups',
            'Channels', 'Bots', 'Services'.
        Note: 'Users' expands to both 'Contacts' and 'NonContacts'.
    exclude_chat_types: Chat types to exclude (case-insensitive).
        Valid values: 'Mute', 'Read', 'Archive'.
    is_add_to_top (bool): Add folder to top of list.
    suggestion_folder_id (str): Suggestion folder ID.
    folder_id (str): Folder ID.

Returns:
    The result of the API call.

### add_saved_music_playlist

```python
add_saved_music_playlist(self: 'darkob.Client', files: Union[Path, str, List[Union[Path, str]]]=None, file_inlines: List[dict]=None, time: Optional[int]=None, performer: Optional[str]=None, file_name: Optional[str]=None, **kwargs)
```

Add a saved music playlist on your profile.

Parameters:
    files: A single file path or a list of file paths to music files.
    file_inlines: Pre-uploaded file_inline dicts to add directly.
    time: Custom duration in seconds. If not provided, auto-detected.
    performer: Custom performer name. If not provided, auto-detected.
    file_name: Custom file name. If not provided, uses original file name.

Returns:
    The result of the API call.

### add_saved_music_track

```python
add_saved_music_track(self: 'darkob.Client', track: Union[Path, str]=None, file_inline: dict=None, time: Optional[int]=None, performer: Optional[str]=None, file_name: Optional[str]=None, **kwargs)
```

Add a single music track to your saved music playlist.

Parameters:
    track: A file path (str or Path) to a music file, or raw bytes.
    file_inline: A pre-uploaded file_inline dict to add directly.
    time: Custom duration in seconds. If not provided, auto-detected.
    performer: Custom performer name. If not provided, auto-detected.
    file_name: Custom file name. If not provided, uses original file name.

Returns:
    The result of the API call.

### auto_delete_account

```python
auto_delete_account(self: 'darkob.Client', setting: Union[int, str])
```

Set account auto-deletion after months of inactivity.

Parameters:
    setting (Union[int, str]): Months of inactivity. Accepts: 3, 6, 12, or 24.
        Can be int (3, 6, 12, 24) or str ("3", "6", "12", "24", "3m", "6m", "12m", "24m")

Returns:
    The updated privacy settings.

Examples:
    >>> await client.auto_delete_account(6)
    >>> await client.auto_delete_account("12m")

### change_password

```python
change_password(self: 'darkob.Client', password: str, new_password: str, new_hint: str)
```

Changes the user's password.

Parameters:
    password (str): The current password.
    new_password (str): The new password.
    new_hint (str): The new password hint.

Returns:
    The result of the API call.

### check_two_step_passcode

```python
check_two_step_passcode(self: 'darkob.Client', password: str)
```

Check if the provided two-step verification password is correct.

Parameters:
    password (str): The two-step verification password to check.

Returns:
    Result containing status and user data if successful.

### confirm_unconfirmed_session

```python
confirm_unconfirmed_session(self: 'darkob.Client', unconfirmed_session_key: str)
```

Confirm an unconfirmed (pending) session.

Parameters:
    unconfirmed_session_key (str): The session key to confirm.

Returns:
    The result of the API call.

### delete_account

```python
delete_account(self: 'darkob.Client')
```

Request to permanently delete your Rubika account.

Returns:
    str: User-friendly confirmation message.

### delete_folder

```python
delete_folder(self: 'darkob.Client', folder_id: str)
```

Delete a folder.

Parameters:
    folder_id (str): The ID of the folder to be deleted.

Returns:
    Result of the delete folder operation.

### delete_saved_music_playlist

```python
delete_saved_music_playlist(self: 'darkob.Client', position: int=None)
```

Delete tracks from the saved music playlist on your profile.

Parameters:
    position (int, optional): The position of the track to delete. If None, deletes all.

Returns:
    The result of the API call.

### deny_unconfirmed_session

```python
deny_unconfirmed_session(self: 'darkob.Client', unconfirmed_session_key: str)
```

Deny an unconfirmed (pending) session.

Parameters:
    unconfirmed_session_key (str): The session key to deny.

Returns:
    The result of the API call.

### edit_can_called_by

```python
edit_can_called_by(self: 'darkob.Client', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to control who can call you.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'
    exceptions (Optional[Dict[str, List[str]]]): 
        - 'include_users': List[str] - Users to always allow
        - 'exclude_users': List[str] - Users to always deny

        To clear exceptions, pass {'exclude_users': []}

Returns:
    The updated privacy settings after the change.

### edit_can_join_chat_by

```python
edit_can_join_chat_by(self: 'darkob.Client', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to control who can join your chats by link.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'
    exceptions (Optional[Dict[str, List[str]]]): 
        - 'include_users': List[str] - Users to always allow
        - 'exclude_users': List[str] - Users to always deny

        To clear exceptions, pass {'exclude_users': []}

Returns:
    The updated privacy settings after the change.

### edit_show_birthday

```python
edit_show_birthday(self: 'darkob.Client', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to show or hide the user's birthday.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'
    exceptions (Optional[Dict[str, List[str]]]): 
        - 'include_users': List[str] - Users to always allow
        - 'exclude_users': List[str] - Users to always deny

        To clear exceptions, pass {'exclude_users': []}

Returns:
    The updated privacy settings after the change.

### edit_show_last_online

```python
edit_show_last_online(self: 'darkob.Client', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to control who can see the user's last online status.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'
    exceptions (Optional[Dict[str, List[str]]]): 
        - 'include_users': List[str] - Users to always allow
        - 'exclude_users': List[str] - Users to always deny

        To clear exceptions, pass {'exclude_users': []}

Returns:
    The updated privacy settings after the change.

### edit_show_phone_number

```python
edit_show_phone_number(self: 'darkob.Client', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to control who can see the user's phone number.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'
    exceptions (Optional[Dict[str, List[str]]]): 
        - 'include_users': List[str] - Users to always allow
        - 'exclude_users': List[str] - Users to always deny

        To clear exceptions, pass {'exclude_users': []}

Returns:
    The updated privacy settings after the change.

### edit_show_profile_photo

```python
edit_show_profile_photo(self: 'darkob.Client', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to control who can see the user's profile photo.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'
    exceptions (Optional[Dict[str, List[str]]]): 
        - 'include_users': List[str] - Users to always allow
        - 'exclude_users': List[str] - Users to always deny

        To clear exceptions, pass {'exclude_users': []}

Returns:
    The updated privacy settings after the change.

### get_folders

```python
get_folders(self: 'darkob.Client', last_state: Union[int, str]=round(time()) - 150)
```

Get a list of folders.

Parameters:
    last_state (Union[int, str]): The last state to retrieve folders.

Returns:
    List of folders.

### get_my_sessions

```python
get_my_sessions(self: 'darkob.Client')
```

Get information about the current user's sessions.

Returns:
    Information about the user's sessions.

### get_notification_setting

```python
get_notification_setting(self: 'darkob.Client')
```

Retrieves the current notification settings for the account.

Returns:
    The result of the API call.

### get_privacy_setting

```python
get_privacy_setting(self: 'darkob.Client')
```

Get the current user's privacy setting.

Returns:
    The current user's privacy setting.

### get_suggested_folders

```python
get_suggested_folders(self: 'darkob.Client')
```

Get the suggested folders for the user.

Returns:
    The suggested folders for the user.

### get_two_passcode_status

```python
get_two_passcode_status(self: 'darkob.Client')
```

Get the two-passcode status for the user.

Returns:
    The two-passcode status for the user.

### get_unconfirmed_sessions

```python
get_unconfirmed_sessions(self: 'darkob.Client')
```

Get a list of unconfirmed (pending) sessions for the current account.

Returns:
    The result of the API call containing unconfirmed sessions.

### login_disable_two_step

```python
login_disable_two_step(self: 'darkob.Client', phone_number: str, email_code: str, forget_password_code_hash: str)
```

Disable two-step verification during login.

Parameters:
    phone_number (str): The phone number associated with the account.
    email_code (str): The verification code sent to email.
    forget_password_code_hash (str): The code hash for
        forgotten password flow.

Returns:
    The result of the API call.

### login_two_step_forget_password

```python
login_two_step_forget_password(self: 'darkob.Client', phone_number: str)
```

Start the password recovery process for two-step verification.

Use this when the user has forgotten their two-step verification password.
This will initiate the recovery flow (e.g. sending a code to email/phone).

Parameters:
    phone_number (str): The phone number associated with the account.

Returns:
    The result of the API call, typically containing a hash or
    instructions for the next step of recovery.

### logout

```python
logout(self: 'darkob.Client', confirm: bool=True)
```

Log out of the current session.

Parameters:
    confirm (bool): If True, ask the user for confirmation before
        logging out. If False, log out immediately.
        Default is True.

Returns:
    The result of the logout operation if confirmed.
    Exits if cancelled.

### register_device

```python
register_device(self: 'darkob.Client', device_model: str=None, *args, **kwargs)
```

Register the current device with the Rubika server.

Parameters:
    device_model (str, optional):
        Custom device model name.

Returns:
    The result of the API call.

### reorder_folder

```python
reorder_folder(self: 'darkob.Client', folder_ids: Union[str, List[str]])
```

Reorder folders.

Parameters:
    folder_ids (Union[str, List[str]]): A single folder ID or a list of folder IDs in the new order.

Returns:
    The result of the API call.

### request_change_phone_number

```python
request_change_phone_number(self: 'darkob.Client', new_phone_number: str)
```

Request to change the account phone number.

Parameters:
    new_phone_number (str): The new phone number (e.g., 09123456789, +989123456789, +1234567890).

Returns:
    The result of the API call containing phone_code_hash for verification.

### request_forget_password

```python
request_forget_password(self: 'darkob.Client')
```

Request to reset the account password.

Returns:
    The result of the API call.

### request_recovery_email

```python
request_recovery_email(self: 'darkob.Client', password: str, recovery_email: str)
```

Request a recovery code to be sent to the recovery email.

Parameters:
    password (str): User's current password.
    recovery_email (str): Recovery email address.

Returns:
    The result of the API call.

### set_notification

```python
set_notification(self: 'darkob.Client', user_notification: Optional[bool]=None, user_message_preview: Optional[bool]=None, group_notification: Optional[bool]=None, group_message_preview: Optional[bool]=None, channel_notification: Optional[bool]=None, channel_message_preview: Optional[bool]=None, in_app_sound: Optional[bool]=None, in_app_preview: Optional[bool]=None, new_contacts: Optional[bool]=None)
```

Update notification settings.

Parameters:
    user_notification (bool, optional): Enable/disable user notifications.
    user_message_preview (bool, optional): Show/hide user message preview.
    group_notification (bool, optional): Enable/disable group notifications.
    group_message_preview (bool, optional): Show/hide group message preview.
    channel_notification (bool, optional): Enable/disable channel notifications.
    channel_message_preview (bool, optional): Show/hide channel message preview.
    in_app_sound (bool, optional): Enable/disable in-app sound.
    in_app_preview (bool, optional): Enable/disable in-app preview.
    new_contacts (bool, optional): Enable/disable new contacts notification.

Returns:
    The updated notification settings.

### set_saved_music_playlist

```python
set_saved_music_playlist(self: 'darkob.Client', files: Union[Path, str, List[Union[Path, str]]]=None, file_inlines: List[dict]=None, time: Optional[int]=None, performer: Optional[str]=None, file_name: Optional[str]=None, **kwargs)
```

Replace the saved music playlist on your profile.

Parameters:
    files: A single file path or a list of file paths to music files.
    file_inlines: Pre-uploaded file_inline dicts to set directly.
    time: Custom duration in seconds. If not provided, auto-detected.
    performer: Custom performer name. If not provided, auto-detected.
    file_name: Custom file name. If not provided, uses original file name.

Returns:
    The result of the API call.

### set_setting

```python
set_setting(self: 'darkob.Client', show_my_last_online: Optional[PrivacyValue]=None, show_my_phone_number: Optional[PrivacyValue]=None, show_my_profile_photo: Optional[PrivacyValue]=None, link_forward_message: Optional[PrivacyValue]=None, can_join_chat_by: Optional[PrivacyValue]=None, show_my_birth_date: Optional[PrivacyValue]=None, can_called_by: Optional[PrivacyValue]=None, auto_delete_messages: Optional[Union[str, int]]=None, inactive_account_delete: Optional[int]=None, show_my_last_online_exceptions: Optional[Dict[str, List[str]]]=None, show_my_phone_number_exceptions: Optional[Dict[str, List[str]]]=None, show_my_profile_photo_exceptions: Optional[Dict[str, List[str]]]=None, can_join_chat_by_exceptions: Optional[Dict[str, List[str]]]=None, show_my_birth_date_exceptions: Optional[Dict[str, List[str]]]=None, can_called_by_exceptions: Optional[Dict[str, List[str]]]=None)
```

Set various privacy and auto-delete settings for the user.

Parameters:
    Privacy Settings (accept: 'Everybody', 'MyContacts', 'Nobody'):
        show_my_last_online: Who can see your last online status
        show_my_phone_number: Who can see your phone number
        show_my_profile_photo: Who can see your profile photo
        link_forward_message: Who can forward your message links
        can_join_chat_by: Who can join your chats by link
        show_my_birth_date: Who can see your birth date
        can_called_by: Who can call you

    Exceptions (for privacy settings except link_forward_message):
        Each exception should be a dict with:
            - 'include_users': List[str] - Users to always allow
            - 'exclude_users': List[str] - Users to always deny

        To CLEAR exceptions for a setting, pass {'exclude_users': []}:
            can_called_by_exceptions={'exclude_users': []}

        Example:
            show_my_last_online_exceptions={
                'include_users': ['u0abc123...'],
                'exclude_users': ['u0xyz789...']
            }

    Auto Delete Messages:
        auto_delete_messages: Message auto-delete duration.

    Delete Inactive Account:
        inactive_account_delete: Delete account after X months.

Returns:
    The result of the setting operation.

### set_two_step_verification

```python
set_two_step_verification(self: 'darkob.Client', password: Union[int, str], hint: str=None, recovery_email: str=None)
```

Set up two-step verification for the user.

Parameters:
    password (Union[int, str]): The current user password.
    hint (str): A hint to help remember the password. Defaults to None.
    recovery_email (str): The recovery email for two-step verification. Defaults to None.

Returns:
    The updated user information after setting up two-step verification.

### terminate_other_sessions

```python
terminate_other_sessions(self: 'darkob.Client')
```

Terminate other account sessions.

Returns:
    The result of the API call.

### terminate_session

```python
terminate_session(self: 'darkob.Client', session_key: str)
```

Terminate a user session.

Parameters:
    session_key (str): The session key of the session to be terminated.

Returns:
    The result of the API call.

### turn_off_two_step

```python
turn_off_two_step(self: 'darkob.Client', password: str)
```

Turn off two-step verification passcode for the account.

Parameters:
    password (str): Current two-step verification password

Returns:
    Result of the operation.

### update_my_bio

```python
update_my_bio(self: 'darkob.Client', bio: str)
```

Update user's biography.

Parameters:
    bio (str): The updated biography (max 150 characters).

Returns:
    The updated user information.

Raises:
    InvalidInput: If bio exceeds 150 characters.

### update_my_birthday

```python
update_my_birthday(self: 'darkob.Client', birthday: Union[str, datetime])
```

Update the birthday in your profile.

Parameters:
    birthday (str | datetime): Birthday in format YYYY-MM-DD (e.g., "2026-02-03") or a datetime object.

Returns:
    The updated user information.

### update_my_name

```python
update_my_name(self: 'darkob.Client', first_name: Optional[str]=None, last_name: Optional[str]=None)
```

Update user's first name and/or last name.

Parameters:
    first_name (Optional[str]): The updated first name (max 30 characters).
    last_name (Optional[str]): The updated last name (max 50 characters).

Returns:
    The updated user information.

### update_my_profile

```python
update_my_profile(self: 'darkob.Client', first_name: Optional[str]=None, last_name: Optional[str]=None, bio: Optional[str]=None, birthday: Optional[str]=None, location: Optional[Dict[str, Union[float, Dict[str, Union[int, List[str], float]]]]]=None)
```

Update user profile information.

Parameters:
    first_name (Optional[str]): The updated first name.
    last_name (Optional[str]): The updated last name.
    bio (Optional[str]): The updated biography.
    birthday (str): Birthday in format YYYY-MM-DD (e.g., "2026-07-05").
    location (Optional[dict]): Location information containing:
        - longitude (float): Longitude coordinate.
        - latitude (float): Latitude coordinate.
        - map_view (dict): Map view details with:
            - tile_side_count (int): Number of tile sides.
            - tile_urls (List[str]): List of tile URLs.
            - x_loc (float): X location on map.
            - y_loc (float): Y location on map.

Returns:
    The updated user information after the profile update.

### update_my_username

```python
update_my_username(self: 'darkob.Client', username: str)
```

Update the username of the user.

Parameters:
    username (str): The new username for the user.
        - Must be between 7 and 32 characters
        - Can only contain English letters (a-z, A-Z), numbers (0-9), and underscore (_)
        - Should not start with number or underscore
        - Should not end with underscore

Returns:
    The updated user information.

### upgrade_to_api6

```python
upgrade_to_api6(self: 'darkob.Client', save_as: bool=True, file_name: Optional[str]=None)
```

Upgrade from API v5 to v6 by setting an RSA public key.

This allows old v5 auth keys to be used with API v6.
After upgrade, save the returned private_key for future v6 logins.

Parameters:
    save_as (bool): If True (default), saves auth and private_key to a JSON file.
    file_name (str, optional): Custom file name for the JSON file. Defaults to 'darkob_{auth[:10]}'.

Returns:
    Data: Response with status, message, auth, and private_key.

### verify_change_phone_number

```python
verify_change_phone_number(self: 'darkob.Client', code: Union[str, int], hash: str)
```

Verify phone number change with the received code.

Parameters:
    code (str): The verification code sent to the new phone number.
    hash (str): The hash received from request_change_phone_number.

Returns:
    The result of the API call.

### verify_recovery_email

```python
verify_recovery_email(self: 'darkob.Client', password: str, code: Union[str, int])
```

Verify the recovery code sent to the recovery email.

Parameters:
    password (str): User's current password.
    code (Union[str, int]): The verification code received in email.
        Can be a string or an integer.

Returns:
    The result of the API call.

## extras

### add_live_comment

```python
add_live_comment(self: 'darkob.Client', access_token: str, live_id: str, comment: str)
```

Adds a comment to a live stream.

Parameters:
    access_token (str): The access token for authentication.
    live_id (str): The ID of the live stream.
    comment (str): The text of the comment.

Returns:
    The result of the API call.

### add_sticker_set

```python
add_sticker_set(self: 'darkob.Client', sticker_set_id: str)
```

Add a sticker set.

Parameters:
    sticker_set_id (str): The ID of the sticker set.

Returns:
    The result of the API call.

### add_to_my_gif_set

```python
add_to_my_gif_set(self: 'darkob.Client', chat: str, message_id: Union[str, int])
```

Adds a GIF message to the user's personal GIF set.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the GIF message.

Returns:
    The result of the API call.

### archive_sticker_set

```python
archive_sticker_set(self: 'darkob.Client', sticker_set_id: str)
```

Archive a sticker set.

Parameters:
    sticker_set_id (str): The ID of the sticker set.

Returns:
    The result of the API call.

### delete_all_my_gif_set

```python
delete_all_my_gif_set(self: 'darkob.Client')
```

Delete all GIFs from the user's personal GIF set.

Returns:
    Data: A Data object containing the deletion result.

### delete_my_gif_set

```python
delete_my_gif_set(self: 'darkob.Client', file_id: str)
```

Deletes a GIF from the user's personal GIF set.

Parameters:
    file_id (str): The file ID of the GIF to be removed.

Returns:
    The result of the API call.

### delete_sticker_set

```python
delete_sticker_set(self: 'darkob.Client', sticker_set_id: str)
```

Delete a sticker set.

Parameters:
    sticker_set_id (str): The ID of the sticker set.

Returns:
    The result of the API call.

### feedback_voice_transcription

```python
feedback_voice_transcription(self: 'darkob.Client', chat: Union[str, int], message_id: Union[str, int], feedback_type: str, feedback_text: str=None)
```

Send feedback for a voice transcription.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the voice message.
    feedback_type (str): 'OK' or 'Incorrect'.
    feedback_text (str, optional): Feedback text. If not provided, uses the transcription text.

Returns:
    The result of the API call.

### get_available_reactions

```python
get_available_reactions(self: 'darkob.Client')
```

Retrieve the list of available message reactions that can be used in chats.

Returns:
    Shows available reactions data from the server.

### get_link_from_app_url

```python
get_link_from_app_url(self: 'darkob.Client', url: str)
```

Get a direct link from an application URL.

Parameters:
    url (str): The application URL to extract the link from.

Returns:
    Data: The result containing the extracted link.

### get_live_comments

```python
get_live_comments(self: 'darkob.Client', live_id: str, access_token: str)
```

Get live stream comments.

Parameters:
    live_id (str): Live stream ID.
    access_token (str): Access token from send_live response.

Returns:
    The result of the API call.

### get_live_play_url

```python
get_live_play_url(self: 'darkob.Client', access_token: str, live_id: str)
```

Retrieves the play URL for a live stream.

Parameters:
    access_token (str): The access token for authentication.
    live_id (str): The ID of the live stream.

Returns:
    The result of the API call.

### get_live_status

```python
get_live_status(self: 'darkob.Client', live_id: str, access_token: str)
```

Get live stream status.

Parameters:
    live_id (str): Live stream ID.
    access_token (str): Access token from send_live response.

Returns:
    Live status info.

### get_location_view

```python
get_location_view(self: 'darkob.Client', latitude: float, longitude: float)
```

Get map view for a location.

Parameters:
    latitude (float): Latitude (-90 to 90)
    longitude (float): Longitude (-180 to 180)

Returns:
    Map view data.

### get_my_archived_sticker_sets

```python
get_my_archived_sticker_sets(self: 'darkob.Client', start_id: str=None)
```

Get archived sticker sets of the current user.

Parameters:
    start_id (str, optional): The ID to start fetching from. Defaults to None.

Returns:
    The result of the API call.

### get_my_gif_set

```python
get_my_gif_set(self: 'darkob.Client')
```

Gets the user's personal GIF set.

Returns:
    Information about the user's GIF set.

### get_my_sticker_sets

```python
get_my_sticker_sets(self: 'darkob.Client')
```

Get the sticker sets owned by the user.

Returns:
    The sticker sets owned by the user.

### get_sticker_set_by_id

```python
get_sticker_set_by_id(self: 'darkob.Client', sticker_set_id: str)
```

Get a sticker set by its ID.

Parameters:
    sticker_set_id (str): The ID of the sticker set.

Returns:
    The sticker set corresponding to the provided ID.

### get_sticker_setting

```python
get_sticker_setting(self: 'darkob.Client')
```

Get the sticker settings of the current user.

Returns:
    The result of the API call containing sticker settings.

### get_stickers_by_emoji

```python
get_stickers_by_emoji(self: 'darkob.Client', emoji: str, suggest_by: str='All')
```

Get stickers by emoji.

Parameters:
    emoji (str): The emoji character.
    suggest_by (str): The type of suggestion (default is 'All').

Returns:
    Stickers corresponding to the provided emoji and suggestion type.

### get_stickers_by_set_ids

```python
get_stickers_by_set_ids(self: 'darkob.Client', sticker_set_ids: Union[str, list])
```

Get stickers by set IDs.

Parameters:
    sticker_set_ids (Union[str, list]): The sticker set ID or a list of sticker set IDs.

Returns:
    Stickers corresponding to the provided set IDs.

### get_time

```python
get_time(self: 'darkob.Client')
```

Retrieve the current server time.

Returns:
    The result of the API call.

### get_trend_sticker_sets

```python
get_trend_sticker_sets(self: 'darkob.Client', start_id: str=None)
```

Get trending sticker sets.

Parameters:
    start_id (str): The start ID for pagination.

Returns:
    Trending sticker sets.

### get_wallet_transaction_message

```python
get_wallet_transaction_message(self: 'darkob.Client', transfer_id: str, access_transfer: str)
```

Get the message associated with a wallet transaction.

Parameters:
    transfer_id (str): The ID of the wallet transaction.
    access_transfer (str): The access hash for the transaction.

Returns:
    The result of the API call.

### get_wallpapers

```python
get_wallpapers(self: 'darkob.Client')
```

Get the current chat wallpaper settings.

Returns:
    The result of the API call containing wallpaper information.

### reorder_sticker_sets

```python
reorder_sticker_sets(self: 'darkob.Client', ordered_sticker_set_ids: Union[str, List[str]])
```

Reorder sticker sets in the user's collection.

Parameters:
    ordered_sticker_set_ids (Union[str, List[str]]): A single sticker
        set ID or a list of sticker set IDs in the desired order.

Returns:
    The result of the API call.

### report_live

```python
report_live(self: 'darkob.Client', live_id: str, report_type: Union[int, str], description: Optional[str]=None)
```

Report a live stream.

Parameters:
    live_id (str): The ID of the live stream to report.
    report_type (Union[int, str]): The report reason.
        Can be:
            - Integer code between 100 and 106
            - String name (case-insensitive): 'Other', 'Violence',
              'Spam', 'Porn', 'ChildAbuse', 'Copyright', 'Fraud'
        If set to 100 (Other), `description` becomes required.
    description (Optional[str]): Description for the report.
        Required when `report_type` is 100 (Other).

Returns:
    The result of the API call.

### reset_wallpapers

```python
reset_wallpapers(self: 'darkob.Client')
```

Reset all chat wallpapers to default.

Returns:
    The result of the API call.

### search_stickers

```python
search_stickers(self: 'darkob.Client', search_text: str='', start_id: str=None)
```

Search for stickers.

Parameters:
    search_text (str): The search text.
    start_id (str): The start ID for pagination.

Returns:
    Stickers matching the search criteria.

### set_current_live_location

```python
set_current_live_location(self: 'darkob.Client', longitude: float, latitude: float, tile_side_count: int, tile_urls: List[str], x_loc: float, y_loc: float)
```

Set the current live location.

Parameters:
    longitude (float): Longitude coordinate.
    latitude (float): Latitude coordinate.
    tile_side_count (int): Number of tiles per side.
    tile_urls (List[str]): URLs of map tiles.
    x_loc (float): X position on the map.
    y_loc (float): Y position on the map.

Returns:
    The result of the API call.

## bots

### delete_bot_chat

```python
delete_bot_chat(self: 'darkob.Client', bot: str)
```

Delete a bot chat.

Parameters:
    bot (str): The GUID or username of the bot.

Returns:
    The result of the API call.

### delete_service_chat

```python
delete_service_chat(self: 'darkob.Client', service: str)
```

Delete a service chat.

Parameters:
    service (str): The GUID of the service chat to delete.

Returns:
    The result of the API call.

### get_bot_info

```python
get_bot_info(self: 'darkob.Client', bot: str)
```

Get information about a bot.

Parameters:
    bot (str): The GUID or username of the bot.

Returns:
    The result of the API call.

### get_inline_bots

```python
get_inline_bots(self: 'darkob.Client', bots: Union[str, List[str]])
```

Retrieve information about inline bots by their GUIDs or usernames.

Parameters:
    bots (Union[str, List[str]]): A single bot GUID/username or a list of bot GUIDs/usernames.

Returns:
    The result of the API call.

### get_service_info

```python
get_service_info(self: 'darkob.Client', service: str)
```

Get information about a service.

Parameters:
    service (str): The GUID of the service.

Returns:
    The result of the API call.

### start_bot

```python
start_bot(self: 'darkob.Client', bot: str)
```

Parameters:
    bot (str): The GUID or username of the bot.

Returns:
    The result of the API call.

### stop_bot

```python
stop_bot(self: 'darkob.Client', bot: str)
```

Parameters:
    bot (str): The GUID or username of the bot.

Returns:
    The result of the API call.

## base

### close

```python
close(self: 'darkob.Client')
```

Close the connection to the Darkob server (async version).

### connect

```python
connect(self: 'darkob.Client')
```

Establish a connection to the Rubika API.

Creates an Api instance and loads stored session information
(auth, guid, private_key, user_agent) if available.

Returns:
    Client instance with active connection.

### disconnect

```python
disconnect(self: 'darkob.Client')
```

Disconnect from the Darkob server (sync version).

### download_file

```python
download_file(self: 'darkob.Client', file_inline: Optional[Union[dict, Data]]=None, dc_id: Optional[int]=None, file_id: Optional[int]=None, access_hash: Optional[str]=None, size: Optional[int]=None, chunk: int=131072, callback: Optional[Callable[[int, int], Union[None, asyncio.Future]]]=None, gather: bool=False, save_as: Optional[Union[str, bool]]=None, file_name: Optional[str]=None, as_base64: bool=False, *args, **kwargs)
```

Download a file from Rubika/Shad.

Parameters:
    file_inline (dict or Data, optional): File inline object from messages.
        If provided, dc_id, file_id, access_hash, size will be extracted.
    dc_id (int, optional): Data center ID (if file_inline not provided).
    file_id (int, optional): Unique identifier of the file.
    access_hash (str, optional): Access hash associated with the file.
    size (int, optional): Total size of the file in bytes.
    chunk (int, optional): Size of each download chunk (default: 131072).
    callback (callable, optional): Progress callback(total_size, downloaded_size).
    gather (bool, optional): Download chunks in parallel (default: False).
    save_as (str or bool, optional): Directory path or True for current dir. If None, returns bytes.
    file_name (str, optional): Custom file name.
    as_base64 (bool, optional): Return as base64 encoded string (default: False).

Returns:
    bytes, str, or Data: File content (bytes), base64 string, or Data object (when save_as used).

### get_string_session

```python
get_string_session(self: 'darkob.Client', password: Optional[str]=None)
```

Export current session as an encrypted StringSession.

Parameters:
    password (Optional[str]): Optional password for encryption.
        If provided, StringSession can only be opened with this password.

Returns:
    str: Encrypted StringSession that can be used later with
         `Messenger(string_session=..., password=...)`.

### get_updates

```python
get_updates(self: 'darkob.Client')
```

Listen for updates from Rubika's WebSocket.

Returns:
    None

### request

```python
request(self: 'darkob.Client', method: str, input: Optional[Dict]=None, tmp_session: bool=False, encrypt: bool=True)
```

Build and send a request to the Rubika API.

Parameters:
    method (str): API method name (e.g., 'sendMessage', 'getUserInfo').
    input (dict, optional): Input data for the method.
    tmp_session (bool): Use temporary session instead of auth (default: False).
        When True, the client will auto-connect if not connected yet.
    encrypt (bool): Encrypt the request data (default: True).

Returns:
    Data or None: The API response.

Raises:
    NoConnection: If the client has not been started and `tmp_session=False`.

### run

```python
run(self, coroutine: Optional[Coroutine]=None)
```

Start the client and listen for updates.

Parameters:
    coroutine: Optional coroutine to run before listening for updates.

Returns:
    None when used normally (runs forever until stopped).

### send_code

```python
send_code(self: 'darkob.Client', phone_number: str, pass_key: Optional[str]=None)
```

Send a verification code to a phone number.

Parameters:
    phone_number (str): The target phone number.
    pass_key (str): The optional account pass key.

Returns:
    The result of the API call.

### sign_in

```python
sign_in(self: 'darkob.Client', phone_number: str, phone_code: str, phone_code_hash: str, public_key: str)
```

Sign in using the verification code.

Parameters:
    phone_number (str): The phone number.
    phone_code (str): The verification code.
    phone_code_hash (str): The verification code hash.
    public_key (str): The client's public key.

Returns:
    The result of the API call.

### start

```python
start(self: 'darkob.Client', phone_number: str=None)
```

Start the client, handling authentication and registration.

Parameters:
    phone_number (str, optional): Phone number for registration.

Returns:
    Client: The initialized client instance.

### upload_file

```python
upload_file(self: 'darkob.Client', file: Union[str, bytes, None]=None, base64_data: Optional[str]=None, mime: Optional[str]=None, file_name: Optional[str]=None, chunk: int=1048576, callback: Optional[Callable[[int, int], Union[None, asyncio.Future]]]=None, *args, **kwargs)
```

Upload a file to Rubika with chunked transfer and retry logic.

Parameters:
    file (str, bytes, or None): File path, bytes, or URL to upload.
    base64_data (str, optional): Base64 encoded file data.
    mime (str, optional): MIME type of the file.
    file_name (str, optional): Name of the file.
    chunk (int, optional): Chunk size in bytes (default: 1MB).
    callback (callable, optional): Progress callback(total_size, uploaded_bytes).

Returns:
    Metadata about the uploaded file.

## core

### add_handler

```python
add_handler(self: 'darkob.Client', func: Callable, handler: Union[ChatUpdates, MessageUpdates, ShowActivities, ShowNotifications, RemoveNotifications])
```

_No docstring available._

### remove_handler

```python
remove_handler(self: 'darkob.Client', func)
```

_No docstring available._

### stop

```python
stop(self)
```

_No docstring available._

## decorators

### on_add_reaction

```python
on_add_reaction(self: 'darkob.Client', *filters: Filter)
```

Decorator for reaction added.

### on_call_signal

```python
on_call_signal(self: 'darkob.Client', *filters: Filter)
```

Decorator for call signal data.

### on_call_update

```python
on_call_update(self: 'darkob.Client', *filters: Filter)
```

Decorator for call updates.

### on_chat_updates

```python
on_chat_updates(self: 'darkob.Client', *filters: Filter)
```

Decorator for chat updates with optional filters.

### on_delete_message

```python
on_delete_message(self: 'darkob.Client', *filters: Filter)
```

Decorator for deleted messages.

### on_draft_message

```python
on_draft_message(self: 'darkob.Client', *filters: Filter)
```

Decorator for draft message updates.

### on_edit_message

```python
on_edit_message(self: 'darkob.Client', *filters: Filter)
```

Decorator for edited messages with optional filters.

### on_message

```python
on_message(self: 'darkob.Client', *filters: Filter)
```

Decorator for message updates with optional filters.

### on_new_message

```python
on_new_message(self: 'darkob.Client', *filters: Filter)
```

Decorator for new messages with optional filters.

### on_remove_notifications

```python
on_remove_notifications(self: 'darkob.Client', *args, **kwargs)
```

_No docstring available._

### on_remove_reaction

```python
on_remove_reaction(self: 'darkob.Client', *filters: Filter)
```

Decorator for reaction removed.

### on_scheduled_message

```python
on_scheduled_message(self: 'darkob.Client', *filters: Filter)
```

Decorator for scheduled message updates.

### on_show_activities

```python
on_show_activities(self: 'darkob.Client', *filters: Filter)
```

Decorator for show activities (typing, uploading, recording) with optional filters.

### on_show_notifications

```python
on_show_notifications(self: 'darkob.Client', *filters: Filter)
```

Decorator for show notifications with optional filters.

### on_unconfirmed_session

```python
on_unconfirmed_session(self: 'darkob.Client', *filters: Filter)
```

Decorator for unconfirmed session updates (anti-login).

### on_voice_chat_participant

```python
on_voice_chat_participant(self: 'darkob.Client', *filters: Filter)
```

Decorator for voice chat participant updates.

### on_voice_chat_update

```python
on_voice_chat_update(self: 'darkob.Client', *filters: Filter)
```

Decorator for voice chat updates.
