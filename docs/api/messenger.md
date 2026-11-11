# Messenger API reference

A real user account (userbot): channels, groups, voice chats, settings.

> Generated from the installed package by `scripts/generate_docs_assets.py`. Every signature below is real; do not hand-edit this file.

**378 public methods.**

## Method index

- **messages** (67): [`add_reaction`](#add-reaction), [`auto_delete_message`](#auto-delete-message), [`click_inline_button`](#click-inline-button), [`click_message_url`](#click-message-url), [`delete_all_messages`](#delete-all-messages), [`delete_message`](#delete-message), [`delete_messages`](#delete-messages), [`delete_my_messages`](#delete-my-messages), [`edit_message`](#edit-message), [`forward_message`](#forward-message), [`forward_messages`](#forward-messages), [`get_all_messages`](#get-all-messages), [`get_chat_messages`](#get-chat-messages), [`get_first_message`](#get-first-message), [`get_first_messages`](#get-first-messages), [`get_last_message`](#get-last-message), [`get_last_messages`](#get-last-messages), [`get_message_info`](#get-message-info), [`get_message_url`](#get-message-url), [`get_messages`](#get-messages), [`get_messages_by_id`](#get-messages-by-id), [`get_messages_interval`](#get-messages-interval), [`get_messages_reactions`](#get-messages-reactions), [`get_messages_updates`](#get-messages-updates), [`get_pinned_messages`](#get-pinned-messages), [`get_poll_option_voters`](#get-poll-option-voters), [`get_poll_status`](#get-poll-status), [`get_scheduled_messages`](#get-scheduled-messages), [`get_wallet_transfer_message`](#get-wallet-transfer-message), [`iter_messages`](#iter-messages), [`mark_as_read`](#mark-as-read), [`mark_as_seen`](#mark-as-seen), [`pin_message`](#pin-message), [`remove_reaction`](#remove-reaction), [`report_message`](#report-message), [`request_send_file`](#request-send-file), [`retract_poll`](#retract-poll), [`save_message_draft`](#save-message-draft), [`search_chat_messages`](#search-chat-messages), [`search_global_messages`](#search-global-messages), [`search_messages`](#search-messages), [`send_contact`](#send-contact), [`send_file`](#send-file), [`send_gif`](#send-gif), [`send_image`](#send-image), [`send_live`](#send-live), [`send_live_location`](#send-live-location), [`send_location`](#send-location), [`send_message`](#send-message), [`send_message_api_call`](#send-message-api-call), [`send_music`](#send-music), [`send_now_scheduled_message`](#send-now-scheduled-message), [`send_poll`](#send-poll), [`send_quiz`](#send-quiz), [`send_rubino_post`](#send-rubino-post), [`send_rubino_product`](#send-rubino-product), [`send_rubino_story`](#send-rubino-story), [`send_sticker`](#send-sticker), [`send_video`](#send-video), [`send_video_message`](#send-video-message), [`send_voice`](#send-voice), [`send_wallet_transfer_message`](#send-wallet-transfer-message), [`stop_poll`](#stop-poll), [`transcribe_voice`](#transcribe-voice), [`unpin_all_messages`](#unpin-all-messages), [`unpin_message`](#unpin-message), [`vote_poll`](#vote-poll)
- **chats** (93): [`accept_all_join_requests`](#accept-all-join-requests), [`accept_join_request`](#accept-join-request), [`accept_ownership_request`](#accept-ownership-request), [`add_member`](#add-member), [`add_members`](#add-members), [`archive_chat`](#archive-chat), [`ban_member`](#ban-member), [`ban_members`](#ban-members), [`cancel_change_owner`](#cancel-change-owner), [`change_owner`](#change-owner), [`check_join`](#check-join), [`check_rubino_username`](#check-rubino-username), [`check_voice_chat_participants`](#check-voice-chat-participants), [`clear_all_drafts`](#clear-all-drafts), [`clear_black_list`](#clear-black-list), [`clear_chat_draft`](#clear-chat-draft), [`click_chat_ads`](#click-chat-ads), [`click_keypad_button`](#click-keypad-button), [`create_join_link`](#create-join-link), [`delete_all_avatars`](#delete-all-avatars), [`delete_avatar`](#delete-avatar), [`delete_chat_history`](#delete-chat-history), [`delete_revoked_join_link`](#delete-revoked-join-link), [`delete_revoked_join_links`](#delete-revoked-join-links), [`discard_voice_chat`](#discard-voice-chat), [`dont_show_chat_ads`](#dont-show-chat-ads), [`download_avatars`](#download-avatars), [`download_profile_picture`](#download-profile-picture), [`edit_join_link`](#edit-join-link), [`get_abs_chats`](#get-abs-chats), [`get_all_drafts`](#get-all-drafts), [`get_avatars`](#get-avatars), [`get_banned_members`](#get-banned-members), [`get_chat_ads`](#get-chat-ads), [`get_chat_info`](#get-chat-info), [`get_chat_voice_chat`](#get-chat-voice-chat), [`get_chats`](#get-chats), [`get_chats_info`](#get-chats-info), [`get_chats_updates`](#get-chats-updates), [`get_guid`](#get-guid), [`get_info_by_link`](#get-info-by-link), [`get_info_by_username`](#get-info-by-username), [`get_join_link_user_joined`](#get-join-link-user-joined), [`get_join_links`](#get-join-links), [`get_join_requests`](#get-join-requests), [`get_my_guid`](#get-my-guid), [`get_pending_owner`](#get-pending-owner), [`get_profile_link_items`](#get-profile-link-items), [`get_related_chats`](#get-related-chats), [`get_voice_chat_participants`](#get-voice-chat-participants), [`get_voice_chat_updates`](#get-voice-chat-updates), [`heartbeat`](#heartbeat), [`invite_to_voice_chat`](#invite-to-voice-chat), [`join_chat`](#join-chat), [`join_voice_chat`](#join-voice-chat), [`leave_chat`](#leave-chat), [`leave_voice_chat`](#leave-voice-chat), [`member_is_admin`](#member-is-admin), [`member_is_joined`](#member-is-joined), [`member_is_owner`](#member-is-owner), [`mute_chat`](#mute-chat), [`pin_chat`](#pin-chat), [`pin_chat_in_folder`](#pin-chat-in-folder), [`play_voice_chat`](#play-voice-chat), [`reject_join_request`](#reject-join-request), [`reject_ownership_request`](#reject-ownership-request), [`report_chat`](#report-chat), [`report_chat_ads`](#report-chat-ads), [`revoke_join_link`](#revoke-join-link), [`search_global_chats`](#search-global-chats), [`seen_chats`](#seen-chats), [`send_chat_activity`](#send-chat-activity), [`send_voice_chat_activity`](#send-voice-chat-activity), [`set_admin`](#set-admin), [`set_ask_spam`](#set-ask-spam), [`set_avatar_as_main`](#set-avatar-as-main), [`set_chat_auto_delete`](#set-chat-auto-delete), [`set_chat_protected_content`](#set-chat-protected-content), [`set_chat_use_time`](#set-chat-use-time), [`set_voice_chat_setting`](#set-voice-chat-setting), [`set_voice_chat_state`](#set-voice-chat-state), [`speaking`](#speaking), [`start_voice_chat`](#start-voice-chat), [`unarchive_chat`](#unarchive-chat), [`unban_all_members`](#unban-all-members), [`unban_member`](#unban-member), [`unban_members`](#unban-members), [`unmute_chat`](#unmute-chat), [`unpin_chat`](#unpin-chat), [`unpin_chat_in_folder`](#unpin-chat-in-folder), [`unset_admin`](#unset-admin), [`upload_avatar`](#upload-avatar), [`view_chat_ads`](#view-chat-ads)
- **groups** (23): [`create_group`](#create-group), [`delete_group`](#delete-group), [`delete_no_access_group_chat`](#delete-no-access-group-chat), [`edit_group_info`](#edit-group-info), [`edit_group_timer`](#edit-group-timer), [`edit_group_title`](#edit-group-title), [`edit_slow_mode`](#edit-slow-mode), [`get_group_admin_access`](#get-group-admin-access), [`get_group_admins`](#get-group-admins), [`get_group_default_access`](#get-group-default-access), [`get_group_info`](#get-group-info), [`get_group_link`](#get-group-link), [`get_group_members`](#get-group-members), [`get_group_mention_list`](#get-group-mention-list), [`get_group_message_read_participants`](#get-group-message-read-participants), [`get_group_online_count`](#get-group-online-count), [`get_unread_mentions`](#get-unread-mentions), [`join_group`](#join-group), [`leave_group`](#leave-group), [`lock_group`](#lock-group), [`set_group_default_access`](#set-group-default-access), [`set_group_link`](#set-group-link), [`unlock_group`](#unlock-group)
- **channels** (21): [`check_channel_username`](#check-channel-username), [`check_channels_with_username`](#check-channels-with-username), [`create_channel`](#create-channel), [`delete_channel`](#delete-channel), [`edit_channel_info`](#edit-channel-info), [`edit_channel_title`](#edit-channel-title), [`get_channel_admin_access`](#get-channel-admin-access), [`get_channel_admins`](#get-channel-admins), [`get_channel_info`](#get-channel-info), [`get_channel_link`](#get-channel-link), [`get_channel_members`](#get-channel-members), [`get_channel_post_by_link`](#get-channel-post-by-link), [`get_channel_seen_count`](#get-channel-seen-count), [`get_channel_statistics`](#get-channel-statistics), [`get_post_by_ask_link`](#get-post-by-ask-link), [`join_channel`](#join-channel), [`leave_channel`](#leave-channel), [`seen_channel_messages`](#seen-channel-messages), [`set_channel_link`](#set-channel-link), [`set_channel_type`](#set-channel-type), [`update_channel_username`](#update-channel-username)
- **users** (32): [`accept_call`](#accept-call), [`add_contact`](#add-contact), [`block_user`](#block-user), [`call_started`](#call-started), [`check_user_username`](#check-user-username), [`delete_contact`](#delete-contact), [`delete_user_chat`](#delete-user-chat), [`discard_call`](#discard-call), [`get_blocked_users`](#get-blocked-users), [`get_call_config`](#get-call-config), [`get_call_signaling_data`](#get-call-signaling-data), [`get_calls`](#get-calls), [`get_common_groups`](#get-common-groups), [`get_contacts`](#get-contacts), [`get_contacts_last_online`](#get-contacts-last-online), [`get_contacts_stories`](#get-contacts-stories), [`get_contacts_updates`](#get-contacts-updates), [`get_last_online`](#get-last-online), [`get_me`](#get-me), [`get_saved_music_playlist`](#get-saved-music-playlist), [`get_top_users`](#get-top-users), [`get_user_info`](#get-user-info), [`import_contacts`](#import-contacts), [`rate_call`](#rate-call), [`received_call`](#received-call), [`remove_from_top_users`](#remove-from-top-users), [`request_video_call`](#request-video-call), [`request_voice_call`](#request-voice-call), [`reset_contacts`](#reset-contacts), [`send_call_signaling_data`](#send-call-signaling-data), [`unblock_all_users`](#unblock-all-users), [`unblock_user`](#unblock-user)
- **settings** (64): [`abort_set_recovery_email`](#abort-set-recovery-email), [`abort_two_step_setup`](#abort-two-step-setup), [`add_folder`](#add-folder), [`add_saved_music_playlist`](#add-saved-music-playlist), [`add_saved_music_track`](#add-saved-music-track), [`auto_delete_account`](#auto-delete-account), [`change_password`](#change-password), [`check_two_step_passcode`](#check-two-step-passcode), [`confirm_unconfirmed_session`](#confirm-unconfirmed-session), [`delete_account`](#delete-account), [`delete_folder`](#delete-folder), [`delete_saved_music_playlist`](#delete-saved-music-playlist), [`deny_unconfirmed_session`](#deny-unconfirmed-session), [`disable_two_step_by_forget_password`](#disable-two-step-by-forget-password), [`edit_can_called_by`](#edit-can-called-by), [`edit_can_join_chat_by`](#edit-can-join-chat-by), [`edit_folder`](#edit-folder), [`edit_show_birthday`](#edit-show-birthday), [`edit_show_last_online`](#edit-show-last-online), [`edit_show_phone_number`](#edit-show-phone-number), [`edit_show_profile_photo`](#edit-show-profile-photo), [`get_appearance_setting`](#get-appearance-setting), [`get_data_setting`](#get-data-setting), [`get_device_setting`](#get-device-setting), [`get_folders`](#get-folders), [`get_my_sessions`](#get-my-sessions), [`get_notification_setting`](#get-notification-setting), [`get_privacy_setting`](#get-privacy-setting), [`get_suggested_folders`](#get-suggested-folders), [`get_two_passcode_status`](#get-two-passcode-status), [`get_unconfirmed_sessions`](#get-unconfirmed-sessions), [`get_user_setting`](#get-user-setting), [`login_disable_two_step`](#login-disable-two-step), [`login_two_step_forget_password`](#login-two-step-forget-password), [`logout`](#logout), [`register_device`](#register-device), [`reorder_folder`](#reorder-folder), [`request_change_phone_number`](#request-change-phone-number), [`request_forget_password`](#request-forget-password), [`request_recovery_email`](#request-recovery-email), [`resend_code_recovery_email`](#resend-code-recovery-email), [`set_appearance_setting`](#set-appearance-setting), [`set_data_setting`](#set-data-setting), [`set_notification`](#set-notification), [`set_notification_setting`](#set-notification-setting), [`set_privacy_setting`](#set-privacy-setting), [`set_quick_reaction`](#set-quick-reaction), [`set_saved_music_playlist`](#set-saved-music-playlist), [`set_setting`](#set-setting), [`set_theme`](#set-theme), [`set_theme_background`](#set-theme-background), [`set_two_step_verification`](#set-two-step-verification), [`terminate_other_sessions`](#terminate-other-sessions), [`terminate_session`](#terminate-session), [`turn_off_two_step`](#turn-off-two-step), [`update_my_bio`](#update-my-bio), [`update_my_birthday`](#update-my-birthday), [`update_my_name`](#update-my-name), [`update_my_profile`](#update-my-profile), [`update_my_username`](#update-my-username), [`upgrade_to_api6`](#upgrade-to-api6), [`upload_wallpaper`](#upload-wallpaper), [`verify_change_phone_number`](#verify-change-phone-number), [`verify_recovery_email`](#verify-recovery-email)
- **extras** (38): [`add_live_comment`](#add-live-comment), [`add_sticker_set`](#add-sticker-set), [`add_to_my_gif_set`](#add-to-my-gif-set), [`archive_sticker_set`](#archive-sticker-set), [`delete_all_my_gif_set`](#delete-all-my-gif-set), [`delete_my_gif_set`](#delete-my-gif-set), [`delete_sticker_set`](#delete-sticker-set), [`feedback_voice_transcription`](#feedback-voice-transcription), [`get_available_reactions`](#get-available-reactions), [`get_current_live_location`](#get-current-live-location), [`get_link_from_app_url`](#get-link-from-app-url), [`get_live_comments`](#get-live-comments), [`get_live_play_url`](#get-live-play-url), [`get_live_replay_viewers`](#get-live-replay-viewers), [`get_live_report`](#get-live-report), [`get_live_status`](#get-live-status), [`get_live_viewers`](#get-live-viewers), [`get_location_view`](#get-location-view), [`get_my_archived_sticker_sets`](#get-my-archived-sticker-sets), [`get_my_gif_set`](#get-my-gif-set), [`get_my_sticker_sets`](#get-my-sticker-sets), [`get_sticker_set_by_id`](#get-sticker-set-by-id), [`get_sticker_setting`](#get-sticker-setting), [`get_stickers_by_emoji`](#get-stickers-by-emoji), [`get_stickers_by_set_ids`](#get-stickers-by-set-ids), [`get_themes`](#get-themes), [`get_time`](#get-time), [`get_trend_sticker_sets`](#get-trend-sticker-sets), [`get_wallet_transaction_message`](#get-wallet-transaction-message), [`get_wallpapers`](#get-wallpapers), [`reorder_sticker_sets`](#reorder-sticker-sets), [`report_live`](#report-live), [`reset_wallpapers`](#reset-wallpapers), [`search_stickers`](#search-stickers), [`set_current_live_location`](#set-current-live-location), [`set_live_setting`](#set-live-setting), [`stop_live`](#stop-live), [`stop_live_location`](#stop-live-location)
- **bots** (7): [`delete_bot_chat`](#delete-bot-chat), [`delete_service_chat`](#delete-service-chat), [`get_bot_info`](#get-bot-info), [`get_inline_bots`](#get-inline-bots), [`get_service_info`](#get-service-info), [`start_bot`](#start-bot), [`stop_bot`](#stop-bot)
- **base** (12): [`close`](#close), [`connect`](#connect), [`disconnect`](#disconnect), [`download_file`](#download-file), [`get_string_session`](#get-string-session), [`get_updates`](#get-updates), [`request`](#request), [`run`](#run), [`send_code`](#send-code), [`sign_in`](#sign-in), [`start`](#start), [`upload_file`](#upload-file)
- **core** (4): [`add_handler`](#add-handler), [`ask`](#ask), [`remove_handler`](#remove-handler), [`stop`](#stop)
- **decorators** (17): [`on_add_reaction`](#on-add-reaction), [`on_call_signal`](#on-call-signal), [`on_call_update`](#on-call-update), [`on_chat_updates`](#on-chat-updates), [`on_delete_message`](#on-delete-message), [`on_draft_message`](#on-draft-message), [`on_edit_message`](#on-edit-message), [`on_message`](#on-message), [`on_new_message`](#on-new-message), [`on_remove_notifications`](#on-remove-notifications), [`on_remove_reaction`](#on-remove-reaction), [`on_scheduled_message`](#on-scheduled-message), [`on_show_activities`](#on-show-activities), [`on_show_notifications`](#on-show-notifications), [`on_unconfirmed_session`](#on-unconfirmed-session), [`on_voice_chat_participant`](#on-voice-chat-participant), [`on_voice_chat_update`](#on-voice-chat-update)

## messages

### add_reaction

```python
add_reaction(self: 'darkob.Messenger', chat: str, message_id: Union[str, int], reaction_id: Union[int, str])
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
auto_delete_message(self: 'darkob.Messenger', chat: str, message_id: Union[str, int], time: Union[float, int])
```

Automatically delete a message after a specified time.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the message to be deleted.
    time (Union[float, int]): The time delay (in seconds) before deleting.

Returns:
    Confirmation of the scheduled deletion

### click_inline_button

```python
click_inline_button(self: 'darkob.Messenger', chat: str, message_id: Union[str, int], button_id: str)
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
click_message_url(self: 'darkob.Messenger', chat: str, message_id: Union[str, int], link_url: str)
```

Simulate clicking a URL contained within a specific message.

Parameters:
    chat (str): The GUID, link or username of the chat.
    message_id (Union[str, int]): The unique ID of the message that includes the URL.
    link_url (str): The URL string embedded in the message to be clicked.

Returns:
    The result of the API call.

### delete_all_messages

```python
delete_all_messages(self: 'darkob.Messenger', chat: str, exclude_message_ids: Optional[Union[str, int, List[Union[str, int]]]]=None, type: Literal['Local', 'Global', 'Scheduled']='Global')
```

Delete all messages in a chat except the first creation event message and optionally specified message IDs.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    exclude_message_ids (Union[str, int, List[Union[str, int]]], optional): Message ID(s) to preserve (not delete). Default is None.
    type (Literal['Local', 'Global', 'Scheduled']): The type of deletion. Case-insensitive. Default is 'Global'.

Returns:
    Result of the deletion operation.

### delete_message

```python
delete_message(self: 'darkob.Messenger', chat: str, message_id: Union[str, int], type: Literal['Local', 'Global', 'Scheduled']='Global')
```

Delete a single message in a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the message to delete.
    type (Literal['Local', 'Global', 'Scheduled']): The type of deletion. Case-insensitive. Default is 'Global'.

Returns:
    The result of the API call.

### delete_messages

```python
delete_messages(self: 'darkob.Messenger', chat: str, message_ids: Union[str, int, List[Union[str, int]]], type: Literal['Local', 'Global', 'Scheduled']='Global')
```

Delete specified messages associated with the given chat.

Parameters:
    chat (str): The GUID, link, or username of the chat associated with the messages
        (e.g., user, group, channel).
    message_ids (Union[str, int, List[Union[str, int]]]): The ID or list of IDs of the messages to be deleted.
    type (Literal['Local', 'Global', 'Scheduled']): The type of deletion. Case-insensitive. Default is 'Global'.

Returns:
    The result of the API call.

### delete_my_messages

```python
delete_my_messages(self: 'darkob.Messenger', chat: str, exclude_message_ids: Optional[Union[str, int, List[Union[str, int]]]]=None, type: Literal['Local', 'Global', 'Scheduled']='Global')
```

Delete all messages sent by the authenticated user in a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    exclude_message_ids (Optional[Union[str, int, List[Union[str, int]]]]):
        Message ID(s) to exclude from deletion (preserve them). Default is None.
    type (Literal['Local', 'Global', 'Scheduled']): The type of deletion. Case-insensitive. Default is 'Global'.

Returns:
    Result of the deletion operation.

### edit_message

```python
edit_message(self: 'darkob.Messenger', chat: str, message_id: Union[int, str], text: str, metadata: Optional[dict]=None)
```

Edit the specified message associated with the given chat.

Parameters:
    chat (str): The GUID, link, or username of the chat associated with the message (e.g., user, group, channel).
    message_id (Union[int, str]): The ID of the message to be edited.
    text (str): The new text content for the message.
    metadata (dict, optional): Pre-formatted metadata (Bold, Italic, etc.).

Returns:
    The updated information after editing the message.

### forward_message

```python
forward_message(self: 'darkob.Messenger', from_chat: str, message_id: Union[str, int], to_chat: str, hide_author: bool=False, is_mute: bool=False, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None)
```

Forward a single message from one chat to another.

Parameters:
    from_chat (str): The GUID, link, or username of the source chat.
    message_id (Union[str, int]): The ID of the message to forward.
    to_chat (str): The GUID, link, or username of the destination chat.
    hide_author (bool): Hide the original sender's identity. Default is False.
    is_mute (bool): Forward silently without notification. Default is False.
    schedule_time (Optional[Union[int, float, timedelta, datetime]]):
        When to send the forwarded message.
    schedule_type (Optional[Literal['Default', 'WhenOnline']]):
        'Default' uses schedule_time, 'WhenOnline' sends when user comes online.

Returns:
    The result of the API call.

### forward_messages

```python
forward_messages(self: 'darkob.Messenger', from_chat: str, message_ids: Union[str, int, List[Union[str, int]]], to_chat: str, hide_author: bool=False, is_mute: bool=False, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None)
```

Forward specified messages from one chat to another.

Parameters:
    from_chat (str): The GUID, link, or username of the source chat.
    message_ids (Union[str, int, List[Union[str, int]]]): The IDs of the messages to forward.
    to_chat (str): The GUID, link, or username of the destination chat.
    hide_author (bool): Hide the original sender's identity. Default is False.
    is_mute (bool): Forward silently without notification. Default is False.
    schedule_time (Union[int, float, timedelta, datetime], optional): When to send. Unix timestamp, timedelta, or datetime.
    schedule_type (str, optional): 'Default' or 'WhenOnline'. Case-insensitive.

Returns:
    The result of the API call.

### get_all_messages

```python
get_all_messages(self: 'darkob.Messenger', chat: str, show_message_ids: bool=False)
```

Retrieve all messages from a chat.

Parameters:
    chat (str): Chat identifier or link (username, GUID, or invite link)
    show_message_ids (bool, optional): Include message IDs in output. Default is False.

Returns:
    Result containing all messages with total count, first/last IDs, and chat GUID.

### get_chat_messages

```python
get_chat_messages(self: 'darkob.Messenger', chat: str, max_id: Optional[Union[str, int]]=None, sort: Literal['FromMax', 'FromMin']='FromMin', filter_type: Optional[Literal['Voice', 'File', 'Music', 'Gif', 'Media', 'Link']]=None, limit: Optional[int]=None, all_pages: bool=False, min_id: Optional[Union[str, int]]=None, middle_message_id: Optional[Union[str, int]]=None)
```

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

### get_first_message

```python
get_first_message(self: 'darkob.Messenger', chat: str)
```

Get the first message of a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The first message details.

### get_first_messages

```python
get_first_messages(self: 'darkob.Messenger', chat: str, limit: int=100)
```

Get the first messages of a chat up to a limit.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    limit (int): Maximum number of messages to retrieve (max 500, min 1).

Returns:
    List of first messages and count.

### get_last_message

```python
get_last_message(self: 'darkob.Messenger', chat: str)
```

Get the last message from a chat and retrieve its details.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The last message details.

### get_last_messages

```python
get_last_messages(self: 'darkob.Messenger', chat: str, limit: int=100)
```

Get the last messages of a chat up to a limit.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    limit (int): Maximum number of messages to retrieve (max 500).

Returns:
    List of last messages and count.

### get_message_info

```python
get_message_info(self: 'darkob.Messenger', chat: str, message_id: Union[str, int])
```

Get detailed information about a message.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the message to retrieve.

Returns:
    Message information.

### get_message_url

```python
get_message_url(self: 'darkob.Messenger', chat: str, message_id: Union[str, int])
```

Get the shareable URL of a specific message.

Parameters:
    chat (str): The GUID, link, or username of the chat to which the message belongs.
    message_id (Union[str, int]): The ID of the message for which to retrieve the shareable URL.

Returns:
    The shareable URL of the specified message.

### get_messages

```python
get_messages(self: 'darkob.Messenger', chat: str, types: Optional[Union[str, List[str]]]=None, logic: Literal['OR', 'AND']='OR')
```

Get messages from a chat with optional type filtering.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    types (Union[str, List[str]], optional): Type(s) of messages to filter by. Available types: text, image, video, video_message, voice, music, file, gif, live, location, poll, contact, event, edited, forwarded, sticker, me, bots, users. You can also pass a member GUID or username.
    logic (str): How to combine multiple filters. 'OR' or 'AND'. Case-insensitive. Default is 'OR'.

Returns:
    - messages: list of filtered messages.
    - count: number of filtered messages.
    - chat_guid: The GUID of the chat.
    - total_all: total messages before filtering.
    - filter_types: list of applied type filters.
    - member_guids: list of applied member GUID filters.
    - logic: the applied logic ('OR' or 'AND').

### get_messages_by_id

```python
get_messages_by_id(self: 'darkob.Messenger', chat: str, message_ids: Union[str, int, list])
```

Retrieve messages by their IDs.

Parameters:
    chat (str): The GUID, link, or username of the chat to which the messages belong.
    message_ids (Union[str, int, list]): The ID or list of IDs of the messages to retrieve.

Returns:
    The retrieved messages identified by their IDs.

### get_messages_interval

```python
get_messages_interval(self: 'darkob.Messenger', chat: str, middle_message_id: Union[int, str])
```

Retrieve messages in an interval around a middle message ID.

Parameters:
    chat (str): The GUID, link, or username of the chat to which the messages belong.
    middle_message_id (Union[int, str]): The middle message ID around which the interval is determined.

Returns:
    The retrieved messages in the specified interval.

### get_messages_reactions

```python
get_messages_reactions(self: 'darkob.Messenger', chat: str, min_id: Union[str, int], max_id: Union[str, int])
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
get_messages_updates(self: 'darkob.Messenger', chat: str, state: int=None)
```

Get message updates for a specific chat.

Parameters:
    chat (str): The GUID, link, or username of the chat for which updates are requested.
    state (int): The state at which updates are requested. Defaults to a timestamp approximately 150 seconds ago.

Returns:
    The message updates for the specified chat.

### get_pinned_messages

```python
get_pinned_messages(self: 'darkob.Messenger', chat: str)
```

Get all pinned messages from a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    Dictionary containing pinned messages and pinned IDs.

### get_poll_option_voters

```python
get_poll_option_voters(self: 'darkob.Messenger', poll_id: str, selection_index: Union[str, int], show_user_guids: bool=False, all_pages: bool=True, start_id: Optional[str]=None)
```

Get voters for a specific poll option.

Parameters:
    poll_id (str): The ID of the poll for which voters are requested.
    selection_index (Union[str, int]): The index of the poll option for which voters are requested.
    show_user_guids (bool, optional):
        If True, include a list of unique voter GUIDs in the output.
        Default is False.
    all_pages (bool, optional):
        If True, automatically fetch all pages of voters.
        If False, only fetch one page using start_id.
        Default is True.
    start_id (Optional[str]): The ID from which to start fetching voters.
        Only used when all_pages is False or as the initial point.

Returns:
    Result containing all voters, total count, and optionally voter_guids.

### get_poll_status

```python
get_poll_status(self: 'darkob.Messenger', poll_id: str)
```

Get the status of a specific poll.

Parameters:
    poll_id (str): The ID of the poll for which the status is requested.

Returns:
    The status of the specified poll.

### get_scheduled_messages

```python
get_scheduled_messages(self: 'darkob.Messenger', chat: str, start_id: Optional[str]=None)
```

Get scheduled messages in a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    start_id (str, optional): The ID to start fetching from. Defaults to None.

Returns:
    The result of the API call containing scheduled messages.

### get_wallet_transfer_message

```python
get_wallet_transfer_message(self: 'darkob.Messenger', transfer_id: str, access_transfer: str)
```

Get a wallet transfer message details.

Parameters:
    transfer_id (str): The transfer ID.
    access_transfer (str): The access transfer hash.

Returns:
    The result of the API call.

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
mark_as_read(self: 'darkob.Messenger', chat: str)
```

Mark a chat as read by seeing the last message.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    Result of the operation.

### mark_as_seen

```python
mark_as_seen(self: 'darkob.Messenger', chat: str, message_id: Optional[Union[str, int]]=None)
```

Mark a specific message as seen.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int], optional): Specific message ID. Defaults to last message.

Returns:
    Result of the operation.

### pin_message

```python
pin_message(self: 'darkob.Messenger', chat: str, message_id: Union[str, int])
```

Pin a message.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the message to pin.

Returns:
    The result of the API call.

### remove_reaction

```python
remove_reaction(self: 'darkob.Messenger', chat: str, message_id: Union[str, int], reaction_id: Union[int, str])
```

Remove a reaction from a specific message.

Parameters:
    chat (str): The GUID, link, or username of the chat associated with the message.
    message_id (Union[str, int]): The ID of the message from which the reaction will be removed.
    reaction_id (Union[int, str]): The ID of the reaction to be removed.

Returns:
    The result of the API call.

### report_message

```python
report_message(self: 'darkob.Messenger', chat: str, message_id: Union[str, int], report_type: Union[int, str], description: Optional[str]=None)
```

Report a message for a specific reason.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the message to be reported.
    report_type (Union[int, str]): The report reason. Can be int (100-106) or str name (case-insensitive): 'Other', 'Violence', 'Spam', 'Porn', 'ChildAbuse', 'Copyright', 'Fraud'. If 100 (Other), 'description' is required.
    description (str, optional): Description for the report. Required when report_type is 100 (Other).

Returns:
    The result of the API call.

### request_send_file

```python
request_send_file(self: 'darkob.Messenger', file_name: str, size: Union[str, int, float], mime: Optional[str]=None)
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
retract_poll(self: 'darkob.Messenger', poll_id: str)
```

Retract a poll.

Parameters:
    poll_id (str): The ID of the poll to retract.

Returns:
    The result of the API call.

### save_message_draft

```python
save_message_draft(self: 'darkob.Messenger', chat: str, text: str)
```

Save a message as a draft in a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat, or 'me'/'cloud'/'self'/'myself'.
    text (str): The draft text content (Max: 4096 chars, 128 lines).

Returns:
    The result of the API call.

### search_chat_messages

```python
search_chat_messages(self: 'darkob.Messenger', chat: str, search_text: str)
```

Searches for chat messages based on the specified criteria.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    search_text (str): The text to search for in messages.

Returns:
    The search results containing messages.

### search_global_messages

```python
search_global_messages(self: 'darkob.Messenger', search_text: str, all_pages: bool=True, start_id: Optional[str]=None)
```

Search for messages globally across all chats.

Parameters:
    search_text (str): The text or hashtag to search for.
    all_pages (bool, optional):
        If True, automatically fetch all pages of results.
        If False, only fetch one page using start_id.
        Default is True.
    start_id (str, optional): The ID to start fetching from.
        Only used when all_pages is False or as the initial point.

Returns:
    Result containing messages, total count, and pagination info.

### search_messages

```python
search_messages(self: 'darkob.Messenger', chat: str, text: str)
```

Search for messages containing specific text in a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    text (str): The text to search for.

Returns:
    The search results.

### send_contact

```python
send_contact(self: 'darkob.Messenger', chat: str, phone_number: Union[str, int], user: str, first_name: str, last_name: str='', vcard: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None)
```

Send a contact message to a specified chat.

Parameters:
    chat (str): The GUID or username of the user or bot.
    phone_number (Union[str, int]): Contact's phone number.
    user (str): Contact's username or user GUID.
    first_name (str): Contact's first name.
    last_name (str, optional): Contact's last name. Defaults to "".
    vcard (str, optional): Custom vCard string. Defaults to None.
    reply_to_message_id (Union[str, int], optional): ID of the message to reply to. Defaults to None.

Returns:
    The result of the API call.

### send_file

```python
send_file(self: 'darkob.Messenger', chat: str, file: Optional[Union[Path, str, bytes, 'Data']]=None, file_inline: Optional[Union[dict, 'Data']]=None, text: Optional[str]=None, type: str='File', is_spoil: bool=False, thumb: Optional[Union[bool, str, Path, bytes]]=None, audio_info: bool=True, performer: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, is_mute: bool=False, metadata: Optional[dict]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: Optional[str]=None, **kwargs)
```

Send a file (Image, Video, Voice, Music, Gif, File) to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat. Use 'me', 'cloud', 'self', or 'myself' for saved messages.
    file (Union[Path, str, bytes, Data], optional): The file data (path, URL, bytes, or Data object).
    file_inline (Union[dict, Data], optional): Pre-uploaded file object. If provided, 'file' and 'base64' are ignored.
    text (str, optional): The caption for the file (Max: 2048 chars, 64 lines).
    type (str): The type of the file ('File', 'Image', 'Video', 'Voice', 'Music', 'Gif', 'VideoMessage'). Defaults to 'File'.
    is_spoil (bool): If True, the file will be marked as spoil.
    thumb (Union[bool, str, Path, bytes], optional): Thumbnail for the file.
    audio_info (bool): If True, extracts audio info for Music/Voice.
    performer (str, optional): Music performer name.
    reply_to_message_id (Union[str, int], optional): The ID of the message to which this is a reply.
    via_bot (str, optional): Bot GUID or username to send the message via.
    is_mute (bool): If True, the message will be sent silently.
    metadata (dict, optional): Pre-formatted metadata for the caption.
    schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
    schedule_type (str, optional): 'Default' or 'WhenOnline'.
    base64 (str, optional): Base64 encoded file data.
    **kwargs: Additional parameters (e.g., file_name, width, height, time, callback).

Returns:
    The result of the API call.

### send_gif

```python
send_gif(self: 'darkob.Messenger', chat: str, gif: Optional[Union[Path, str, bytes]]=None, file_inline: Optional[Union[dict, 'Data']]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, thumb: Optional[Union[bool, str]]=None, width: Optional[int]=None, height: Optional[int]=None, time: Optional[int]=None, is_mute: bool=False, metadata: Optional[dict]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: Optional[str]=None, **kwargs)
```

Send a GIF to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    gif (Union[Path, str, bytes], optional): The GIF data (path, URL, or bytes).
    file_inline (Union[dict, Data], optional): Pre-uploaded GIF object. If provided, 'gif' and 'base64' are ignored.
    text (str, optional): Caption for the GIF (Max: 2048 chars, 64 lines).
    reply_to_message_id (Union[str, int], optional): ID of the message to reply to.
    via_bot (str, optional): Bot GUID or username to send the message via.
    thumb (Union[bool, str], optional): Thumbnail for the GIF.
    width (int, optional): Custom width for the GIF.
    height (int, optional): Custom height for the GIF.
    time (int, optional): Custom duration for the GIF in seconds.
    is_mute (bool): If True, the message will be sent silently. Defaults to False.
    metadata (dict, optional): Pre-formatted metadata for the caption.
    schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
    schedule_type (str, optional): 'Default' or 'WhenOnline'.
    base64 (str, optional): Base64 encoded GIF data.
    **kwargs: Additional parameters.

Returns:
    The result of the API call.

### send_image

```python
send_image(self: 'darkob.Messenger', chat: str, image: Optional[Union[Path, str, bytes]]=None, file_inline: Optional[Union[dict, 'Data']]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, is_spoil: bool=False, via_bot: Optional[str]=None, thumb: Optional[Union[bool, str]]=None, width: Optional[int]=None, height: Optional[int]=None, is_mute: bool=False, metadata: Optional[dict]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: Optional[str]=None, **kwargs)
```

Send an image to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    image (Union[Path, str, bytes], optional): The image data (path, URL, or bytes).
    file_inline (Union[dict, Data], optional): Pre-uploaded image object. If provided, 'image' and 'base64' are ignored.
    text (str, optional): Caption for the image (Max: 2048 chars, 64 lines).
    reply_to_message_id (Union[str, int], optional): ID of the message to reply to.
    is_spoil (bool): Whether the image should be marked as a spoiler. Defaults to False.
    via_bot (str, optional): Bot GUID or username to send the message via.
    thumb (Union[bool, str], optional): Thumbnail behavior.
    width (int, optional): Custom width for the image.
    height (int, optional): Custom height for the image.
    is_mute (bool): If True, the message will be sent silently. Defaults to False.
    metadata (dict, optional): Pre-formatted metadata for the caption.
    schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
    schedule_type (str, optional): 'Default' or 'WhenOnline'.
    base64 (str, optional): Base64 encoded image data.
    **kwargs: Additional parameters.

Returns:
    The result of the API call.

### send_live

```python
send_live(self: 'darkob.Messenger', chat: str, title: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, thumb: Optional[Union[str, Path, bytes]]=None, suggestion_comments: Optional[List[str]]=None, device_type: Literal['Software', 'Mobile']='Software')
```

Send a live stream.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    title (str, optional): Live stream title.
    reply_to_message_id (Union[str, int], optional): The ID of the message to which this is a reply.
    thumb (Union[str, Path, bytes], optional): Thumbnail for the live stream. str (base64/path/URL), Path, or bytes. Default thumbnail if not provided.
    suggestion_comments (List[str], optional): Suggested comments for the live stream.
    device_type (str): The device type. 'Software' or 'Mobile'. Case-insensitive. Defaults to 'Software'.

Returns:
    The result of the API call.

### send_live_location

```python
send_live_location(self: 'darkob.Messenger', chat: str, latitude: float, longitude: float, live_period: int=60, reply_to_message_id: Optional[Union[str, int]]=None)
```

Send a live location.

Parameters:
    chat (str): The GUID, link, or username of the chat, or 'me'/'cloud'/'self'/'myself'.
    latitude (float): Latitude (-90 to 90).
    longitude (float): Longitude (-180 to 180).
    live_period (int): Live location duration in seconds. Default: 60.
    reply_to_message_id (Optional[Union[str, int]]): The ID of the message to reply to. Defaults to None.

Returns:
    The result of the API call.

### send_location

```python
send_location(self: 'darkob.Messenger', chat: str, latitude: float, longitude: float, reply_to_message_id: Optional[Union[str, int]]=None, map_view: Optional[Dict]=None)
```

Send a map location.

Parameters:
    chat (str): The GUID, link, or username of the chat, or 'me'/'cloud'/'self'/'myself'.
    latitude (float): Latitude (-90 to 90).
    longitude (float): Longitude (-180 to 180).
    reply_to_message_id (Union[str, int], optional): The ID of the message to which this is a reply.
    map_view (dict, optional): Custom map view with keys: tile_side_count (int), tile_urls (list[str]), x_loc (float), y_loc (float).
        Example:
            map_view= {
                "tile_side_count": 3,
                "tile_urls": ["https://tile/...", ...],
                "x_loc": 0.5,
                "y_loc": 0.5
            }

Returns:
    The result of the API call.

### send_message

```python
send_message(self: 'darkob.Messenger', chat: str, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, file_inline=None, base64_data: Optional[str]=None, sticker=None, type: str='File', is_spoil: bool=False, thumb=None, audio_info: bool=True, metadata: Optional[dict]=None, performer: Optional[str]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[str]=None, is_mute: bool=False, **kwargs)
```

Send text, an uploaded file or a sticker.

The long parameter list is intentional compatibility: 1.18 moved file
arguments into ``send_file`` and removed them from this method. Keep
the original positional layout instead of silently misrouting callers.
Keyword-only use of upstream's ``metadata`` and ``is_mute`` is
supported as before.

### send_message_api_call

```python
send_message_api_call(self: 'darkob.Messenger', chat: str, message_id: str | int, button_id: str)
```

Send API call response to a chat's inline keyboard button.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): ID of the message containing inline keyboard.
    button_id (str): ID of the button.

Returns:
    The result of the API call.

Example:
    >>> await client.send_message_api_call(  # doctest: +SKIP
    ...     chat="b0C2y04506bd2306f068aa161e0502db",
    ...     message_id="1499338519906784",
    ...     button_id="100"
    ... )

### send_music

```python
send_music(self: 'darkob.Messenger', chat: str, music: Optional[Union[Path, str, bytes]]=None, file_inline: Optional[Union[dict, 'Data']]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, performer: Optional[str]=None, time: Optional[int]=None, is_mute: bool=False, metadata: Optional[dict]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: Optional[str]=None, **kwargs)
```

Send a music file to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    music (Union[Path, str, bytes], optional): The music data (path, URL, or bytes).
    file_inline (Union[dict, Data], optional): Pre-uploaded music object. If provided, 'music' and 'base64' are ignored.
    text (str, optional): Caption for the music (Max: 2048 chars, 64 lines).
    reply_to_message_id (Union[str, int], optional): ID of the message to reply to.
    via_bot (str, optional): Bot GUID or username to send the message via.
    performer (str, optional): Name of the performer/artist. Auto-detected if not provided.
    time (int, optional): Custom duration for the music in seconds. Auto-detected if not provided.
    is_mute (bool): If True, the message will be sent silently. Defaults to False.
    metadata (dict, optional): Pre-formatted metadata for the caption.
    schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
    schedule_type (str, optional): 'Default' or 'WhenOnline'.
    base64 (str, optional): Base64 encoded music data.
    **kwargs: Additional parameters.

Returns:
    The result of the API call.

### send_now_scheduled_message

```python
send_now_scheduled_message(self: 'darkob.Messenger', chat: str, message_id: Union[int, str])
```

Send a scheduled message immediately.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[int, str]): The ID of the scheduled message to send now.

Returns:
    The result of the API call.

### send_poll

```python
send_poll(self: 'darkob.Messenger', chat: str, question: str, options: list, is_anonymous: bool=True, multiple_answers: bool=False, reply_to_message_id: Optional[Union[str, int]]=None, is_mute: bool=False)
```

Send a poll message with the specified parameters.

Parameters:
    chat (str): The GUID, link or username of the chat associated with the poll (e.g., group, channel).
    question (str): The question for the poll.
    options (list): A list of string values representing the poll options.
    is_anonymous (bool): Whether the poll is anonymous or not. Defaults to True.
    multiple_answers (bool): Whether the poll allows multiple answers or not. Defaults to False.
    reply_to_message_id (Optional[Union[str, int]]): The ID of the message to reply to. Defaults to None.
    is_mute (bool): Whether the poll message is sent silently (without notification). Defaults to False.

Returns:
    The updated information after creating the poll.

### send_quiz

```python
send_quiz(self: 'darkob.Messenger', chat: str, question: str, options: list, correct_option: Union[int, str], hint: Optional[str]=None, is_anonymous: bool=True, reply_to_message_id: Optional[Union[str, int]]=None, is_mute: bool=False)
```

Send a quiz-type poll message.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    question (str): The question for the quiz (Max: 255 chars).
    options (list): A list of quiz options (2 to 10 items, each Max: 100 chars).
    correct_option (Union[int, str]): The index or text of the correct option.
    hint (str, optional): A hint for the correct answer (Max: 200 chars).
    is_anonymous (bool): Whether the poll is anonymous. Defaults to True.
    reply_to_message_id (Union[str, int], optional): The ID of the message to reply to.
    is_mute (bool): Whether the quiz message is sent silently. Defaults to False.

Returns:
    The updated information after creating the quiz-type poll.

### send_rubino_post

```python
send_rubino_post(self: 'darkob.Messenger', chat: str, post_id: str, post_profile_id: str, is_mute: bool=False)
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
send_rubino_product(self: 'darkob.Messenger', chat: str, store_id: str, product_id: str, product_varieties: List[Dict[str, Any]])
```

Send a Rubino product to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    store_id (str): The store ID.
    product_id (str): The product ID.
    product_varieties (List[Dict[str, Any]]): List of product varieties.

Returns:
    The result of the API call.

### send_rubino_story

```python
send_rubino_story(self: 'darkob.Messenger', chat: str, story_id: str, story_profile_id: str, reply_text: str='', type: Literal['Reply', 'Direct']='Reply', is_mute: bool=False)
```

Send a Rubino story reply or direct message.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    story_id (str): The story ID.
    story_profile_id (str): The story profile ID.
    reply_text (str): Reply text. Default is empty string.
    type (str): 'Reply' or 'Direct'. Case-insensitive. Default is 'Reply'.
    is_mute (bool): Send silently without notification. Default is False.

Returns:
    The result of the API call.

### send_sticker

```python
send_sticker(self: 'darkob.Messenger', chat: str, emoji_character: str, sticker_id: str, sticker_set_id: str, file: dict, w_h_ratio: str='1.0', reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, is_mute: bool=False, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None)
```

Send a sticker.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    emoji_character (str): The emoji character associated with the sticker.
    sticker_id (str): The ID of the sticker.
    sticker_set_id (str): The ID of the sticker set.
    file (dict): The file data for the sticker.
    w_h_ratio (str): The width-to-height ratio of the sticker. Defaults to '1.0'.
    reply_to_message_id (Union[str, int], optional): The ID of the message to which this is a reply.
    via_bot (str, optional): Bot GUID or username to send the message via.
    is_mute (bool): If True, the message will be sent silently. Defaults to False.
    schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
    schedule_type (str, optional): 'Default' or 'WhenOnline' (users only).

Returns:
    The result of the API call.

### send_video

```python
send_video(self: 'darkob.Messenger', chat: str, video: Optional[Union[Path, str, bytes]]=None, file_inline: Optional[Union[dict, 'Data']]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, is_spoil: bool=False, via_bot: Optional[str]=None, thumb: Optional[Union[bool, str]]=None, width: Optional[int]=None, height: Optional[int]=None, time: Optional[int]=None, is_mute: bool=False, metadata: Optional[dict]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: Optional[str]=None, **kwargs)
```

Send a video to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    video (Union[Path, str, bytes], optional): The video data (path, URL, or bytes).
    file_inline (Union[dict, Data], optional): Pre-uploaded video object. If provided, 'video' and 'base64' are ignored.
    text (str, optional): Caption for the video (Max: 2048 chars, 64 lines).
    reply_to_message_id (Union[str, int], optional): ID of the message to reply to.
    is_spoil (bool): Whether the video should be marked as a spoiler. Defaults to False.
    via_bot (str, optional): Bot GUID or username to send the message via.
    thumb (Union[bool, str], optional): Thumbnail behavior.
    width (int, optional): Custom width for the video.
    height (int, optional): Custom height for the video.
    time (int, optional): Custom duration for the video in seconds.
    is_mute (bool): If True, the message will be sent silently. Defaults to False.
    metadata (dict, optional): Pre-formatted metadata for the caption.
    schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
    schedule_type (str, optional): 'Default' or 'WhenOnline'.
    base64 (str, optional): Base64 encoded video data.
    **kwargs: Additional parameters.

Returns:
    The result of the API call.

### send_video_message

```python
send_video_message(self: 'darkob.Messenger', chat: str, video_message: Optional[Union[Path, str, bytes]]=None, file_inline: Optional[Union[dict, 'Data']]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, is_spoil: bool=False, via_bot: Optional[str]=None, thumb: Optional[Union[bool, str]]=None, width: Optional[int]=None, height: Optional[int]=None, time: Optional[int]=None, is_mute: bool=False, metadata: Optional[dict]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: Optional[str]=None, **kwargs)
```

Send a video message (round video) to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    video_message (Union[Path, str, bytes], optional): The video message data (path, URL, or bytes).
    file_inline (Union[dict, Data], optional): Pre-uploaded video message object. If provided, 'video_message' and 'base64' are ignored.
    text (str, optional): Caption for the video message (Max: 2048 chars, 64 lines).
    reply_to_message_id (Union[str, int], optional): ID of the message to reply to.
    is_spoil (bool): Whether the video message should be marked as a spoiler. Defaults to False.
    via_bot (str, optional): Bot GUID or username to send the message via.
    thumb (Union[bool, str], optional): Thumbnail behavior.
    width (int, optional): Custom width for the video message.
    height (int, optional): Custom height for the video message.
    time (int, optional): Custom duration for the video message in seconds.
    is_mute (bool): If True, the message will be sent silently. Defaults to False.
    metadata (dict, optional): Pre-formatted metadata for the caption.
    schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
    schedule_type (str, optional): 'Default' or 'WhenOnline'.
    base64 (str, optional): Base64 encoded video message data.
    **kwargs: Additional parameters.

Returns:
    The result of the API call.

### send_voice

```python
send_voice(self: 'darkob.Messenger', chat: str, voice: Optional[Union[Path, str, bytes]]=None, file_inline: Optional[Union[dict, 'Data']]=None, text: Optional[str]=None, reply_to_message_id: Optional[Union[str, int]]=None, via_bot: Optional[str]=None, time: Optional[int]=None, is_mute: bool=False, metadata: Optional[dict]=None, schedule_time: Optional[Union[int, float, timedelta, datetime]]=None, schedule_type: Optional[Literal['Default', 'WhenOnline']]=None, base64: Optional[str]=None, **kwargs)
```

Send a voice message to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    voice (Union[Path, str, bytes], optional): The voice data (path, URL, or bytes).
    file_inline (Union[dict, Data], optional): Pre-uploaded voice object. If provided, 'voice' and 'base64' are ignored.
    text (str, optional): Caption for the voice message (Max: 2048 chars, 64 lines).
    reply_to_message_id (Union[str, int], optional): ID of the message to reply to.
    via_bot (str, optional): Bot GUID or username to send the message via.
    time (int, optional): Custom duration for the voice message in seconds. Auto-detected if not provided.
    is_mute (bool): If True, the message will be sent silently. Defaults to False.
    metadata (dict, optional): Pre-formatted metadata for the caption.
    schedule_time (Union[int, float, timedelta, datetime], optional): When to send the message.
    schedule_type (str, optional): 'Default' or 'WhenOnline'.
    base64 (str, optional): Base64 encoded voice data.
    **kwargs: Additional parameters.

Returns:
    The result of the API call.

### send_wallet_transfer_message

```python
send_wallet_transfer_message(self: 'darkob.Messenger', chat: str, transfer_id: str, access_transfer: str)
```

Send a wallet transfer message to a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    transfer_id (str): The transfer ID.
    access_transfer (str): The access transfer hash.

Returns:
    The result of the API call.

### stop_poll

```python
stop_poll(self: 'darkob.Messenger', poll_id: str)
```

Stop a poll.

Parameters:
    poll_id (str): The ID of the poll to stop.

Returns:
    The result of the API call.

### transcribe_voice

```python
transcribe_voice(self: 'darkob.Messenger', chat: Union[str, int], message_id: Union[str, int])
```

Transcribes voice messages.

Parameters:
    chat (Union[str, int]): The GUID, link, or username of the chat containing the voice message.
    message_id (Union[str, int]): The ID of the voice message.

Returns:
    The transcription result.

### unpin_all_messages

```python
unpin_all_messages(self: 'darkob.Messenger', chat: str)
```

Unpin all pinned messages in a group, channel, or private chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The result of the API call.

### unpin_message

```python
unpin_message(self: 'darkob.Messenger', chat: str, message_id: Union[str, int])
```

Unpin a message.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the message to unpin.

Returns:
    The result of the API call.

### vote_poll

```python
vote_poll(self: 'darkob.Messenger', poll_id: str, selection_index: Union[str, int])
```

Vote on a poll option.

Parameters:
    poll_id (str): The ID of the poll.
    selection_index (Union[str, int]): The index of the option to vote for.

Returns:
    The result of the API call.

## chats

### accept_all_join_requests

```python
accept_all_join_requests(self: 'darkob.Messenger', chat: str, exclude: Optional[Union[str, List[str]]]=None)
```

Accept all pending join requests in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    exclude (Optional[Union[str, List[str]]]): User GUID(s) or username(s) to exclude.

Returns:
    Result containing accepted count and details.

### accept_join_request

```python
accept_join_request(self: 'darkob.Messenger', chat: str, user: str)
```

Accept a join request for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    user (str): The user GUID or username of the requester.

Returns:
    The result of the API call.

### accept_ownership_request

```python
accept_ownership_request(self: 'darkob.Messenger', chat: str)
```

Accept an ownership transfer request.

Parameters:
    chat (str): The GUID, link, or username of the chat (channel/group).

Returns:
    The result of the API call.

### add_member

```python
add_member(self: 'darkob.Messenger', chat: str, member: str)
```

Add a single member to a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel/group.
    member (str): The GUID or username of the member to add.

Returns:
    The result of the API call.

### add_members

```python
add_members(self: 'darkob.Messenger', chat: str, members: Union[str, List[str]])
```

Add members to a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel/group.
    members (Union[str, List[str]]): The GUID(s) or username(s) of the member(s) to be added.

Returns:
    The result of the API call.

### archive_chat

```python
archive_chat(self: 'darkob.Messenger', chat: str)
```

Archive a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to archive.

Returns:
    The result of the API call.

### ban_member

```python
ban_member(self: 'darkob.Messenger', chat: str, member: str)
```

Ban a member from a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    member (str): The GUID or username of member to ban.

Returns:
    Result of the operation.

### ban_members

```python
ban_members(self: 'darkob.Messenger', chat: str, members: List[str])
```

Ban multiple members from a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    members (List[str]): List of GUIDs or usernames of members to ban.

Returns:
    Result containing total count, success/failed counts, and banned/failed members.

### cancel_change_owner

```python
cancel_change_owner(self: 'darkob.Messenger', chat: str)
```

Cancels a pending ownership transfer request for a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the chat (channel/group).

Returns:
    The result of the API call.

### change_owner

```python
change_owner(self: 'darkob.Messenger', chat: str, new_owner: str)
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
check_join(self: 'darkob.Messenger', chat: str, member: str)
```

Check if a user or bot is a member of a specific group or channel.

Parameters:
    chat (str): The GUID, link, or username of the chat to check.
    member (str): The GUID or username of the user/bot to check.

Returns:
    bool: True if user/bot is a member, False otherwise.

### check_rubino_username

```python
check_rubino_username(self: 'darkob.Messenger', username: str)
```

Check the availability of a Rubino page.

Parameters:
    username (str): The username to check.

Returns:
    The result of the API call.

### check_voice_chat_participants

```python
check_voice_chat_participants(self: 'darkob.Messenger', chat: str, users: Union[str, List[str]], voice_chat_id: Optional[str]=None)
```

Check which of the given users/bots are currently in the group/channel voice chat.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    users (Union[str, List[str]]): A single user GUID, username, link, or a list of them.
    voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

Returns:
    The result of the API call, containing only the participants from the provided list.

### clear_all_drafts

```python
clear_all_drafts(self: 'darkob.Messenger')
```

Clear all drafts.

Returns:
    The result of the API call.

### clear_black_list

```python
clear_black_list(self: 'darkob.Messenger', chat: str, exclude: Optional[Union[str, List[str]]]=None)
```

Clear black list with unban all banned members in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    exclude (Optional[Union[str, List[str]]]): Member GUID(s) or username(s) to exclude from unban. Default is None.

Returns:
    Result of unban operation.

### clear_chat_draft

```python
clear_chat_draft(self: 'darkob.Messenger', chat: str)
```

Clear the draft of a specific chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The result of the API call.

### click_chat_ads

```python
click_chat_ads(self: 'darkob.Messenger', chat_ads_id: str)
```

Register a click action on a chat ad.

The `chat_ads_id` is obtained from the `get_chat_ads` method.

Parameters:
    chat_ads_id (str): The chat ads ID to register a click on.

Returns:
    The result of the operation.

### click_keypad_button

```python
click_keypad_button(self: 'darkob.Messenger', chat: str, button_id: str)
```

Click a button in the chat keypad.

Parameters:
    chat (str): The GUID, link, or username of the chat (must be a bot).
    button_id (str): The button ID to click.

Returns:
    The result of the button click.

### create_join_link

```python
create_join_link(self: 'darkob.Messenger', chat: str, expire_time: Optional[int]=None, request_needed: bool=False, title: Optional[str]=None, usage_limit: int=0)
```

Creates an invite link for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the target group or channel.
    expire_time (int, optional): The expiration time of the link in seconds.
    request_needed (bool): Whether join requests must be approved manually.
    title (str, optional): A custom title for the invite link.
    usage_limit (int): The maximum number of times the link can be used.

Returns:
    The API response containing the created invite link.

### delete_all_avatars

```python
delete_all_avatars(self: 'darkob.Messenger', chat: str)
```

Delete all avatars from a chat or user profile.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    Data or dict: Result of the operation.

Note:
    If `chat` is 'me', 'cloud', 'self', or 'myself', it will be replaced with the client's GUID.

### delete_avatar

```python
delete_avatar(self: 'darkob.Messenger', chat: str, avatar_id: str)
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
delete_chat_history(self: 'darkob.Messenger', chat: str)
```

Delete chat history up to the last message.

Parameters:
    chat (str): The GUID, link, or username of the chat (e.g., user, group).

Returns:
    Data or dict: The result of the API call.

### delete_revoked_join_link

```python
delete_revoked_join_link(self: 'darkob.Messenger', chat: str, join_link: str)
```

Delete a specific revoked join link.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    join_link (str): The join link to delete.

Returns:
    The result of the API call.

### delete_revoked_join_links

```python
delete_revoked_join_links(self: 'darkob.Messenger', chat: str, creator: str)
```

Delete all revoked join links created by a specific user.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    creator (str): The creator's GUID or username, or 'me'/'cloud'/'self'/'myself' for the current user.

Returns:
    The result of the API call.

### discard_voice_chat

```python
discard_voice_chat(self: 'darkob.Messenger', chat: str, voice_chat_id: Optional[str]=None)
```

Discard/end a voice chat for a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel or group.
    voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

Returns:
    The result of the API call.

### dont_show_chat_ads

```python
dont_show_chat_ads(self: 'darkob.Messenger', chat_ads_id: str)
```

Register a 'don't show' action on a chat ad.

The `chat_ads_id` is obtained from the `get_chat_ads` method.

Parameters:
    chat_ads_id (str): The chat ads ID to hide.

Returns:
    The result of the operation.

### download_avatars

```python
download_avatars(self: 'darkob.Messenger', chat: str, save_as: Optional[Union[str, bool]]=None, limit: Optional[int]=None)
```

Download all avatars (or a limited number) of a user, group, or channel.

Parameters:
    chat (str): The GUID, link, or username of the user, group, or channel.
    save_as (str | bool, optional): Directory path to save the files. If True, saves in current directory. If None, returns bytes list.
    limit (int, optional): Maximum number of avatars to download. If None, downloads all.

Returns:
    List[bytes], Data, or dict: List of binary data, saved file paths, or result.

### download_profile_picture

```python
download_profile_picture(self: 'darkob.Messenger', chat: Optional[str]=None, file_id: Optional[str]=None, access_hash_rec: Optional[str]=None, dc_id: Optional[str]=None, save_as: Optional[Union[str, bool]]=None, save_all: bool=False)
```

Download the profile picture of a user, group, or channel.

Parameters:
    chat (str, optional): The GUID, link, or username of the user, group, channel, or other chats.
    file_id (str, optional): Direct file_id for download without fetching avatars.
    access_hash_rec (str, optional): Direct access_hash_rec for download without fetching avatars.
    dc_id (str, optional): DC ID required when using file_id and access_hash_rec directly.
    save_as (str | bool, optional): Directory path to save the file(s). If True, saves in current directory. If None, returns bytes only.
    save_all (bool): If True, downloads all avatars instead of just the latest. Returns list of bytes if save_as is None.

Returns:
    bytes, List[bytes], Data, or dict: Binary data, saved file paths, or result.

### edit_join_link

```python
edit_join_link(self: 'darkob.Messenger', chat: str, join_link: str, title: Optional[str]=None, expire_time: Optional[int]=None, request_needed: Optional[bool]=None, usage_limit: Optional[int]=None)
```

Edit an existing invite link for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the target group or channel.
    join_link (str): The join link to edit.
    title (str, optional): A new custom title for the invite link.
    expire_time (int, optional): The new expiration time of the link in seconds.
    request_needed (bool, optional): Whether join requests must be approved manually.
    usage_limit (int, optional): The new maximum number of times the link can be used.

Returns:
    The API response containing the edited invite link.

### get_abs_chats

```python
get_abs_chats(self: 'darkob.Messenger', chats: Union[str, List[str]])
```

Get abstract info (title, avatar, etc.) for multiple chats (users, bots, groups, channels).

Parameters:
    chats (Union[str, List[str]]): A single chat (GUID, username, or link) or a list of them.

Returns:
    The result of the API call, containing `abs_objects`.

### get_all_drafts

```python
get_all_drafts(self: 'darkob.Messenger')
```

Get all saved message drafts.

Returns:
    The result of the API call containing all drafts.

### get_avatars

```python
get_avatars(self: 'darkob.Messenger', chat: str)
```

Get avatars of a specific chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to retrieve avatars for.

Returns:
    The result of the API call.

### get_banned_members

```python
get_banned_members(self: 'darkob.Messenger', chat: str, show_member_guids: bool=False, all_pages: bool=True, start_id: Optional[str]=None)
```

Get a list of banned members in a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel or group.
    show_member_guids (bool, optional): Show member GUIDs in output. Default is False.
    all_pages (bool, optional):
        If True, automatically fetch all pages of banned members.
        If False, only fetch one page using start_id.
        Default is True.
    start_id (str, optional):
        Starting member ID for pagination.
        Only used when all_pages is False.

Returns:
    The result containing banned members with total count and optionally GUIDs.

### get_chat_ads

```python
get_chat_ads(self: 'darkob.Messenger', state: int=None)
```

Retrieves advertising information for chats.

Parameters:
    state (int, optional): The timestamp state to filter chat ads. Defaults to the current time minus 150 seconds.

Returns:
    The result of the API call.

### get_chat_info

```python
get_chat_info(self: 'darkob.Messenger', chat: str)
```

Get information about a user, group, or channel.

Parameters:
    chat (str): The GUID, link, or username of the chat (user, group, or channel).

Returns:
    The update containing information about the chat.

### get_chat_voice_chat

```python
get_chat_voice_chat(self: 'darkob.Messenger', chat: str, voice_chat_id: Optional[str]=None)
```

Get the voice chat information for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

Returns:
    The result of the API call.

### get_chats

```python
get_chats(self: 'darkob.Messenger', show_chat_guids: bool=False, all_pages: bool=True, start_id: Optional[str]=None)
```

Get a list of all chats.

Parameters:
    show_chat_guids (bool, optional): If True, include chat GUIDs in the result. Default is False.
    all_pages (bool, optional): If True, fetch all pages. If False, only one page using start_id. Default is True.
    start_id (str, optional): Starting chat ID for pagination. Only used when all_pages is False.

Returns:
    The result of the API call.

### get_chats_info

```python
get_chats_info(self: 'darkob.Messenger', chats: Union[str, List[str]])
```

Get information about multiple chats by their GUIDs.

Parameters:
    chats (Union[str, List[str]]): A single chat (GUID, username, or link) or a list of them.

Returns:
    The result of the API call containing chats information.

### get_chats_updates

```python
get_chats_updates(self: 'darkob.Messenger', state: Optional[Union[str, int]]=None)
```

Get updates for chats.

Parameters:
    state (Union[str, int], optional): State parameter for syncing updates. If not provided, uses current time minus 150 seconds.

Returns:
    The result of the API call.

### get_guid

```python
get_guid(self: 'darkob.Messenger', chat: str)
```

Retrieves the GUID of a user, group, channel, or bot.

Parameters:
    chat (str): The username, group link, channel link, or bot username.

Returns:
    str: The GUID of the chat.

### get_info_by_link

```python
get_info_by_link(self: 'darkob.Messenger', link: str)
```

Get group or channel preview by join link.

Parameters:
    link (str): The join link.

Returns:
    The result of the API call.

### get_info_by_username

```python
get_info_by_username(self: 'darkob.Messenger', username: str)
```

Get a chat (user, bot, or channel) by its username.

Parameters:
    username (str): The username of the chat.

Returns:
    The result of the API call.

### get_join_link_user_joined

```python
get_join_link_user_joined(self: 'darkob.Messenger', chat: str, join_link: str, all_pages: bool=True, start_id: Optional[str]=None)
```

Get users who joined via a specific join link.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    join_link (str): The join link (e.g., 'https://rubika.ir/joing/...').
    all_pages (bool, optional): If True, fetch all pages. If False, only one page using start_id. Default is True.
    start_id (str, optional): Pagination start ID. Only used when all_pages is False.

Returns:
    The result of the API call.

### get_join_links

```python
get_join_links(self: 'darkob.Messenger', chat: str, creator: Optional[str]=None)
```

Retrieves a list of join links for a specific group or channel.

Parameters:
    chat (str): The GUID, link, or username of the target group or channel.
    creator (str, optional): The user GUID or username of the link creator to filter by.

Returns:
    The API response containing the join links.

### get_join_requests

```python
get_join_requests(self: 'darkob.Messenger', chat: str, show_user_guids: bool=False, search_text: Optional[str]=None, join_link: Optional[str]=None, all_pages: bool=True, start_id: Optional[str]=None)
```

Get a list of join requests in a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel or group.
    show_user_guids (bool, optional): Show user GUIDs in output. Default is False.
    search_text (str, optional): Search text to filter requests. Defaults to None.
    join_link (str, optional): Filter requests by a specific join link.
    all_pages (bool, optional):
        If True, automatically fetch all pages of join requests.
        If False, only fetch one page using start_id.
        Default is True.
    start_id (str, optional):
        Starting request ID for pagination.
        Only used when all_pages is False.

Returns:
    Data or dict: The result containing all join requests with total count.

### get_my_guid

```python
get_my_guid(self: 'darkob.Messenger')
```

Get the GUID of the currently authenticated user.

Returns:
    str: The user's GUID.

### get_pending_owner

```python
get_pending_owner(self: 'darkob.Messenger', chat: str)
```

Retrieves the pending owner information for a specified chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The result of the API call.

### get_profile_link_items

```python
get_profile_link_items(self: 'darkob.Messenger', chat: str)
```

Get profile link items for a given chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.

Returns:
    The result of the API call.

### get_related_chats

```python
get_related_chats(self: 'darkob.Messenger', chat: str, start_id: Optional[str]=None)
```

Get related chats for a given chat.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    start_id (str, optional): Starting item ID for pagination.

Returns:
    The result of the API call.

### get_voice_chat_participants

```python
get_voice_chat_participants(self: 'darkob.Messenger', chat: str, show_user_guids: bool=False, voice_chat_id: Optional[str]=None, all_pages: bool=True, start_id: Optional[str]=None)
```

Get list of participants in a voice chat.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    show_user_guids (bool, optional): Show user GUIDs in output. Default is False.
    voice_chat_id (str, optional): Voice chat ID. If not provided, it will be fetched automatically.
    all_pages (bool, optional): If True, fetch all pages. If False, only one page using start_id. Default is True.
    start_id (str, optional): Starting participant ID for pagination. Only used when all_pages is False.

Returns:
    The result of the API call.

### get_voice_chat_updates

```python
get_voice_chat_updates(self: 'darkob.Messenger', chat: str, state: Optional[Union[int, str]]=None, voice_chat_id: Optional[str]=None)
```

Get voice chat updates for a group.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    state (Union[int, str], optional): The state for updates. If not provided, it defaults to the current time minus 150 seconds.
    voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

Returns:
    The result of the API call.

### heartbeat

```python
heartbeat(self: 'darkob.Messenger', chat_guid: str, voice_chat_id: Optional[str]=None)
```

_No docstring available._

### invite_to_voice_chat

```python
invite_to_voice_chat(self: 'darkob.Messenger', chat: str, invite_user: str, voice_chat_id: Optional[str]=None)
```

Invite a user to a voice chat.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    invite_user (str): The GUID, username, or link of the user to invite.
    voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

Returns:
    The result of the API call.

### join_chat

```python
join_chat(self: 'darkob.Messenger', chat: str)
```

Join a chat (channel or group).

Parameters:
    chat (str): The GUID, link, or username of the chat (channel or group).

Returns:
    The result of the API call.

### join_voice_chat

```python
join_voice_chat(self: 'darkob.Messenger', chat: str, sdp_offer_data: Optional[str]=None, voice_chat_id: Optional[str]=None)
```

Join a group/channel voice chat.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    sdp_offer_data (Optional[str]): SDP offer data. If not provided, uses a default dummy SDP.
    voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

Returns:
    The result of the API call.

### leave_chat

```python
leave_chat(self: 'darkob.Messenger', chat: str)
```

Leave a chat (channel or group).

Parameters:
    chat (str): The GUID, link, or username of the chat (channel or group).

Returns:
    The result of the API call.

### leave_voice_chat

```python
leave_voice_chat(self: 'darkob.Messenger', chat: str, voice_chat_id: Optional[str]=None)
```

Leave a voice chat in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

Returns:
    The result of the API call.

### member_is_admin

```python
member_is_admin(self: 'darkob.Messenger', chat: str, member: str)
```

Checks if a member is an admin in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    member (str): The GUID or username of the member.

Returns:
    bool: True if the user is an admin, False otherwise.

### member_is_joined

```python
member_is_joined(self: 'darkob.Messenger', chat: str, member: str)
```

Check if a user or bot is a member of a specific group or channel.

Alias for `check_join`.

Parameters:
    chat (str): The GUID, link, or username of the chat to check.
    member (str): The GUID or username of the user/bot to check.

Returns:
    bool: True if user/bot is a member, False otherwise.

### member_is_owner

```python
member_is_owner(self: 'darkob.Messenger', chat: str, member: str)
```

Checks if a member is the owner (creator) of a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    member (str): The GUID or username of the member.

Returns:
    bool: True if the user is the owner, False otherwise.

### mute_chat

```python
mute_chat(self: 'darkob.Messenger', chat: str, duration: Optional[Union[int, timedelta]]=None)
```

Mute a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to mute.
    duration (Union[int, timedelta], optional): Duration of mute. int: seconds, must be at least 1800. timedelta: e.g., timedelta(hours=1). Defaults to None (permanent mute).

Returns:
    The result of the API call.

### pin_chat

```python
pin_chat(self: 'darkob.Messenger', chat: str)
```

Pin a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to pin.

Returns:
    Result of the operation.

### pin_chat_in_folder

```python
pin_chat_in_folder(self: 'darkob.Messenger', chat: str, folder_id: str)
```

Pin a chat in a folder.

Parameters:
    chat (str): The GUID, link, or username of the chat to pin.
    folder_id (str): The folder ID to pin the chat in.

Returns:
    The result of the API call.

### play_voice_chat

```python
play_voice_chat(self: 'darkob.Messenger', chat: str, media: pathlib.Path) -> 'VoiceChatConnection'
```

Plays voice media in a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to play the voice media in.
    media (pathlib.Path): The path to the voice media file.

### reject_join_request

```python
reject_join_request(self: 'darkob.Messenger', chat: str, user: str)
```

Reject a join request for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    user (str): The user GUID or username of the requester.

Returns:
    The result of the API call.

### reject_ownership_request

```python
reject_ownership_request(self: 'darkob.Messenger', chat: str)
```

Reject an ownership transfer request.

Parameters:
    chat (str): The GUID, link, or username of the chat (channel/group).

Returns:
    The result of the API call.

### report_chat

```python
report_chat(self: 'darkob.Messenger', chat: str, report_type: Union[int, str], description: Optional[str]=None)
```

Report a chat (user, channel, group, etc.) for a specific reason.

Parameters:
    chat (str): The GUID, link, or username of the chat to be reported.
    report_type (Union[int, str]): The report reason. Can be int (100-106) or str name (case-insensitive): 'Other', 'Violence', 'Spam', 'Porn', 'ChildAbuse', 'Copyright', 'Fraud'. If 100 (Other), 'description' is required.
    description (str, optional): Description for the report. Required when report_type is 100 (Other).

Returns:
    The result of the API call.

### report_chat_ads

```python
report_chat_ads(self: 'darkob.Messenger', chat_ads_id: str)
```

Register a report action on a chat ad.

The `chat_ads_id` is obtained from the `get_chat_ads` method.

Parameters:
    chat_ads_id (str): The chat ads ID to report.

Returns:
    The result of the operation.

### revoke_join_link

```python
revoke_join_link(self: 'darkob.Messenger', chat: str, join_link: str)
```

Revoke an invite link for a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    join_link (str): The join link to revoke.

Returns:
    The result of the API call.

### search_global_chats

```python
search_global_chats(self: 'darkob.Messenger', text: str, filter_type: Optional[Union[str, List[str]]]=None, start_id: Optional[str]=None)
```

Search for global chats (users, channels, etc.) based on the given search text.

Parameters:
    text (str): The text to search for.
    filter_type (Union[str, List[str]], optional): 'User', 'Channel', 'Bot' or a list of them. Case-insensitive.
    start_id (str, optional): The ID to start fetching from. Defaults to None.

Returns:
    The update containing search results.

### seen_chats

```python
seen_chats(self: 'darkob.Messenger', seen_list: dict)
```

Marks multiple chats as seen.

Parameters:
    seen_list (dict): A dictionary containing chat GUIDs and their last seen message IDs.

Returns:
    The result of the operation.

### send_chat_activity

```python
send_chat_activity(self: 'darkob.Messenger', chat: str, activity: Literal['Typing', 'Recording', 'Uploading']='Typing')
```

Sends a chat activity, such as typing, uploading, or recording.

Parameters:
    chat (str): The GUID, link, or username of the group/user.
    activity (str): The type of activity. 'Typing', 'Recording', or 'Uploading'. Case-insensitive. Defaults to 'Typing'.

Returns:
    The result of the API call.

Raises:
    InvalidInput: If the `activity` argument is not one of "Typing", "Uploading", or "Recording".

### send_voice_chat_activity

```python
send_voice_chat_activity(self: 'darkob.Messenger', chat: str, activity: Literal['Speaking']='Speaking', participant_chat_guid: Optional[str]=None, voice_chat_id: Optional[str]=None)
```

Send voice chat activity (e.g., speaking).

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    activity (str): Activity type. Only 'Speaking' is allowed. Case-insensitive. Default: 'Speaking'.
    participant_chat_guid (str, optional): Participant chat GUID. Default is self.guid.
    voice_chat_id (str, optional): Voice chat ID. If not provided, it will be fetched automatically.

Returns:
    The result of the API call.

### set_admin

```python
set_admin(self: 'darkob.Messenger', chat: str, member: str, access: Union[List[str], str]=[], custom_title: str='')
```

Set a member as admin in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    member (str): The GUID or username of member to set as admin.
    access (Union[List[str], str]): List of allowed permissions or single permission string. Case-insensitive. Can also be 'all' to grant all permissions.
    custom_title (str): Custom title for admin in groups. (optional)

Returns:
    Result of the operation.

### set_ask_spam

```python
set_ask_spam(self: 'darkob.Messenger', chat: str, action: Literal['AddToContact', 'BlockUser', 'Cancel', 'ReportAndLeave']='Cancel')
```

Perform an action for a pending spam request.

Parameters:
    chat (str): The GUID, link, or username of the user, group, or channel.
    action (str): The action to apply. Case-insensitive. For user (u0): 'AddToContact', 'BlockUser', 'Cancel'. For group/channel (g0/c0): 'ReportAndLeave'.

Returns:
    The result of the API call.

### set_avatar_as_main

```python
set_avatar_as_main(self: 'darkob.Messenger', chat: str, avatar_id: str)
```

Set an avatar as the main avatar for a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat, or 'me'/'cloud'/'self'/'myself'.
    avatar_id (str): The ID of the avatar to set as main.

Returns:
    The result of the API call.

### set_chat_auto_delete

```python
set_chat_auto_delete(self: 'darkob.Messenger', chat: Union[str, List[str]], auto_delete: Union[str, int])
```

Set auto-delete timer for one or more groups or channels.

Parameters:
    chat (Union[str, List[str]]): The GUID, link, username of a group/channel, or a list of them.
    auto_delete (Union[str, int]): Auto-delete duration. Accepts: int (1-365 days), str ('1m'-'60m', '1h'-'24h', '1d'-'365d', '1w'-'52w', '1y', 'off'), or words ('day', 'week', 'month', 'year', 'never', 'disabled').

Returns:
    The result of the API call.

### set_chat_protected_content

```python
set_chat_protected_content(self: 'darkob.Messenger', chat: str, enabled: bool)
```

Set the chat protected content setting.

Parameters:
    chat (str): The GUID or username of the target chat.
    enabled (bool): Pass True to enable the protected content setting, False to disable.

Returns:
    The result of the API call.

### set_chat_use_time

```python
set_chat_use_time(self: 'darkob.Messenger', chat: str, use_time: int)
```

Send chat usage time to the server.

This helps the server recognize natural user behavior and can reduce rate limiting and bot detection.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    use_time (int): Time spent in the chat in seconds.

Returns:
    The result of the API call.

### set_voice_chat_setting

```python
set_voice_chat_setting(self: 'darkob.Messenger', chat: str, title: Optional[str]=None, join_muted: Optional[bool]=None, voice_chat_id: Optional[str]=None)
```

Set voice chat settings for group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    title (Optional[str]): New title for voice chat.
    join_muted (Optional[bool]): Whether new participants join muted. (Only for groups)
    voice_chat_id (Optional[str]): Voice chat ID. If not provided, it will be fetched automatically.

Returns:
    The result of the API call.

### set_voice_chat_state

```python
set_voice_chat_state(self: 'darkob.Messenger', chat: str, action: Literal['Mute', 'Unmute', 'RequestSpeak', 'CancelRequestSpeak']='Unmute', participant_chat_guid: Optional[str]=None, voice_chat_id: Optional[str]=None)
```

Set group or channel voice chat state automatically.

Parameters:
    chat (str): The GUID, link, or username of the group/channel.
    action (str): Action to apply. 'Mute', 'Unmute', 'RequestSpeak', or 'CancelRequestSpeak'. Case-insensitive. Default is 'Unmute'.
    participant_chat_guid (str, optional): Participant chat GUID. Default is self.guid.
    voice_chat_id (str, optional): Voice chat ID. If not provided, it will be fetched automatically.

Returns:
    The result of the API call.

### speaking

```python
speaking(self: 'darkob.Messenger', chat_guid: str, voice_chat_id: Optional[str]=None)
```

_No docstring available._

### start_voice_chat

```python
start_voice_chat(self: 'darkob.Messenger', chat: str, version: int=1)
```

Start a voice chat for a channel or group.

Parameters:
    chat (str): The GUID, link, or username of the channel/group.
    version (int): Voice chat protocol version. Default: 1.

Returns:
    The result of the API call.

### unarchive_chat

```python
unarchive_chat(self: 'darkob.Messenger', chat: str)
```

Unarchive a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to unarchive.

Returns:
    Result of the operation.

### unban_all_members

```python
unban_all_members(self: 'darkob.Messenger', chat: str, exclude: Optional[Union[str, List[str]]]=None)
```

Unban all banned members in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of the group or channel.
    exclude (Optional[Union[str, List[str]]]): Member GUID(s) or username(s) to exclude from unban. Default is None.

Returns:
    Result of unban operation.

### unban_member

```python
unban_member(self: 'darkob.Messenger', chat: str, member: str)
```

Unban a member from a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    member (str): The GUID or username of member to unban.

Returns:
    Result of the operation.

### unban_members

```python
unban_members(self: 'darkob.Messenger', chat: str, members: List[str])
```

Unban multiple members from a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    members (List[str]): List of GUIDs or usernames of members to unban.

Returns:
    Data or dict: Result containing total count, success/failed counts, and unbanned/failed members.

### unmute_chat

```python
unmute_chat(self: 'darkob.Messenger', chat: str)
```

Unmute a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to unmute.

Returns:
    Result of the operation.

### unpin_chat

```python
unpin_chat(self: 'darkob.Messenger', chat: str)
```

Unpin a chat.

Parameters:
    chat (str): The GUID, link, or username of the chat to unpin.

Returns:
    Result of the operation.

### unpin_chat_in_folder

```python
unpin_chat_in_folder(self: 'darkob.Messenger', chat: str, folder_id: str)
```

Unpin a chat from a folder.

Parameters:
    chat (str): The GUID, link, or username of the chat to unpin.
    folder_id (str): The folder ID to unpin the chat from.

Returns:
    The result of the API call.

### unset_admin

```python
unset_admin(self: 'darkob.Messenger', chat: str, member: str)
```

Unset a member as admin in a group or channel.

Parameters:
    chat (str): The GUID, link, or username of group/channel.
    member (str): The GUID or username of member to unset as admin.

Returns:
    Result of the operation.

### upload_avatar

```python
upload_avatar(self: 'darkob.Messenger', chat: str, main_image: Optional[Union[Path, str, bytes]]=None, thumbnail_image: Optional[Union[Path, str, bytes]]=None, main_file_id: Optional[Union[str, int]]=None, thumbnail_file_id: Optional[Union[str, int]]=None, *args, **kwargs)
```

Uploads an avatar image for a specified chat (user, group, or channel).

Parameters:
    chat (str): The GUID, link, or username of the chat for which the avatar is being uploaded.
    main_image (Optional[Union[Path, str, bytes]]): The image file or bytes to be used as the avatar.
    thumbnail_image (Optional[Union[Path, str, bytes]]): The image file or bytes of the thumbnail image.
    main_file_id (Optional[Union[str, int]]): The file ID of the main image (if already uploaded).
    thumbnail_file_id (Optional[Union[str, int]]): The file ID of the thumbnail image (if already uploaded).

Returns:
    The result of the API call.

Note:
    If `chat` is 'me', 'cloud', or 'self', it will be replaced with the client's GUID.
    If `main_file_id` and `thumbnail_file_id` are provided, no file upload will be performed.

### view_chat_ads

```python
view_chat_ads(self: 'darkob.Messenger', chat_ads_id: str)
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
create_group(self: 'darkob.Messenger', title: str, members: Union[str, List[str]], description: Optional[str]=None, avatar: Optional[Union[Path, str, bytes]]=None, thumbnail_avatar: Optional[Union[Path, str, bytes]]=None, main_file_id: Optional[Union[str, int]]=None, thumbnail_file_id: Optional[Union[str, int]]=None, *args, **kwargs)
```

Create a new group.

Parameters:
    title (str): The title of the group.
    members (Union[str, List[str]]): A single member GUID/Username or a list of member GUIDs/Usernames.
    description (str, optional): Description of the group.
    avatar (Path | str | bytes, optional): The image to be used as the group avatar.
    thumbnail_avatar (Path | str | bytes, optional): The image to be used as the group thumbnail avatar.
    main_file_id (Union[str, int], optional): Pre-uploaded main avatar file ID.
    thumbnail_file_id (Union[str, int], optional): Pre-uploaded thumbnail avatar file ID.

Returns:
    The result of the API call.

Note:
    If a file ID is provided, the corresponding image is not uploaded.
    If no thumbnail is provided, it is taken from the main image.

### delete_group

```python
delete_group(self: 'darkob.Messenger', group: str, confirm: bool=True)
```

Delete a group.

Parameters:
    group (str): The GUID or link of the group.
    confirm (bool): If True, ask the user for confirmation before deleting the group. If False, delete immediately. Default is True.

Returns:
    The result of the API call. Exits if cancelled.

### delete_no_access_group_chat

```python
delete_no_access_group_chat(self: 'darkob.Messenger', group: str)
```

Delete (leave) a group chat that the user has no access to.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### edit_group_info

```python
edit_group_info(self: 'darkob.Messenger', group: str, title: Optional[str]=None, description: Optional[str]=None, slow_mode: Optional[str]=None, event_messages: Optional[bool]=None, is_restricted_content: Optional[bool]=None, reactions: Optional[Union[Literal['All', 'Disable'], List[int]]]=None, chat_history_for_new_members: Optional[str]=None, restricted_period: Optional[List[Dict[str, Union[List[str], str]]]]=None)
```

Edit the information of a group.

Parameters:
    group (str): The GUID or link of the group.
    title (str, optional): The new title for the group (max 60 characters).
    description (str, optional): The new description for the group (max 300 characters).
    slow_mode (str, optional): The new slow mode setting for the group.
    event_messages (bool, optional): Enable or disable event messages for the group.
    is_restricted_content (bool, optional): Restrict content (prevent screenshots and file saving).
    reactions (Union[Literal['All', 'Disable'], List[int]], optional): 'All' to enable all reactions, 'Disable' to disable all, or a list of reaction IDs to enable (e.g., [1, 2, 6, 7, 8, 23, 44]). Case-insensitive.
    chat_history_for_new_members (str, optional): The new chat history setting for new members ('Hidden' or 'Visible'). Case-insensitive.
    restricted_period (List[Dict[str, Union[List[str], str]]], optional): Time restrictions for sending messages (list of periods). Each period should contain days_of_week (list of days ['Saturday', 'Sunday', ..., 'Friday'], case-insensitive), from_time (start time in "HH:MM" format, 24-hour), and to_time (end time in "HH:MM" format, 24-hour). Can accept multiple periods as a list of dictionaries.

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
edit_group_timer(self: 'darkob.Messenger', group: str, timer: Union[str, int])
```

Edit the slow mode timer for a group.

Parameters:
    group (str): The GUID or link of the group.
    timer (Union[str, int]): The new slow mode setting for the group.

Returns:
    The result of the API call.

### edit_group_title

```python
edit_group_title(self: 'darkob.Messenger', group: str, title: str)
```

Edit title of a group.

Parameters:
    group (str): The GUID or link of the group.
    title (str): The new title of the group.

Returns:
    The result of the API call.

### edit_slow_mode

```python
edit_slow_mode(self: 'darkob.Messenger', group: str, slow_mode: Union[str, int])
```

Parameters:
    group (str): The GUID or link of the group.
    slow_mode (Union[str, int]): The new slow mode setting for the group.

Returns:
    The result of the API call.

### get_group_admin_access

```python
get_group_admin_access(self: 'darkob.Messenger', group: str, admin: str)
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
get_group_default_access(self: 'darkob.Messenger', group: str)
```

Get the default access settings for a group.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### get_group_info

```python
get_group_info(self: 'darkob.Messenger', group: str)
```

Get information about a group.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### get_group_link

```python
get_group_link(self: 'darkob.Messenger', group: str)
```

Get the link associated with a group.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### get_group_members

```python
get_group_members(self: 'darkob.Messenger', group: str, search_text: Optional[str]=None, start_id: Optional[str]=None)
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
get_group_mention_list(self: 'darkob.Messenger', group: str, search_mention: Optional[str]=None)
```

Get the mention list for a group.

Parameters:
    group (str): The GUID or link of the group.
    search_mention (str, optional): Search text for mentions.

Returns:
    The result of the API call.

### get_group_message_read_participants

```python
get_group_message_read_participants(self: 'darkob.Messenger', group: str, message_id: Union[str, int])
```

Get list of participants who have read a specific message in a group.

Parameters:
    group (str): The GUID or link of the group.
    message_id (Union[str, int]): The ID of the message.

Returns:
    The result of the API call containing read participants.

### get_group_online_count

```python
get_group_online_count(self: 'darkob.Messenger', group: str)
```

Retrieves the number of online members in a specified group.

Parameters:
    group (str): The GUID or link of the group.

Returns:
    The result of the API call.

### get_unread_mentions

```python
get_unread_mentions(self: 'darkob.Messenger', group: str, max_id: Union[str, int], min_id: Union[str, int], sort: Optional[str]=None)
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
join_group(self: 'darkob.Messenger', group: str)
```

Join a group using the provided link.

Parameters:
    group (str): The group link.

Returns:
    The result of the API call.

### leave_group

```python
leave_group(self: 'darkob.Messenger', group: str)
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
set_group_default_access(self: 'darkob.Messenger', group: str, access: Union[str, list])
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
        If empty list "[]", ALL access permissions are disabled/closed. Case-insensitive.

Returns:
    The result of the API call.

### set_group_link

```python
set_group_link(self: 'darkob.Messenger', group: str)
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
check_channel_username(self: 'darkob.Messenger', username: str)
```

Check the availability of a username for a channel.

Parameters:
    username (str): The username to check.

Returns:
    The result of the API call.

### check_channels_with_username

```python
check_channels_with_username(self: 'darkob.Messenger', usernames: Union[str, List[str]])
```

Check which channels have the given usernames.

Parameters:
    usernames (Union[str, List[str]]): A single username or a list of usernames.

Returns:
    The result of the API call.

### create_channel

```python
create_channel(self: 'darkob.Messenger', title: str, members: Optional[Union[str, list]]=None, channel_type: str='Public', description: Optional[str]=None, avatar: Optional[Union[Path, str, bytes]]=None, thumbnail_avatar: Optional[Union[Path, str, bytes]]=None, main_file_id: Optional[Union[str, int]]=None, thumbnail_file_id: Optional[Union[str, int]]=None, *args, **kwargs)
```

Create a new channel.

Parameters:
    title (str): The title of the new channel.
    members (Union[str, list], optional): The member(s) to add. Default is None.
    channel_type (str): 'Public' or 'Private'. Case-insensitive. Default is 'Public'.
    description (str, optional): The description. Default is None.
    avatar (Path | str | bytes, optional): The channel avatar. Default is None.
    thumbnail_avatar (Path | str | bytes, optional): The thumbnail avatar. Default is None.
    main_file_id (Union[str, int], optional): Pre-uploaded main avatar file ID. Default is None.
    thumbnail_file_id (Union[str, int], optional): Pre-uploaded thumbnail avatar file ID. Default is None.

Returns:
    The result of the API call.

Note:
    If a file ID is provided, the corresponding image is not uploaded.
    If no thumbnail is provided, it is taken from the main image.

### delete_channel

```python
delete_channel(self: 'darkob.Messenger', channel: str, confirm: bool=True)
```

Delete a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    confirm (bool): If True, ask for confirmation before deleting. Default is True.

Returns:
    The result of the API call.
    Exits if cancelled.

### edit_channel_info

```python
edit_channel_info(self: 'darkob.Messenger', channel: str, title: Optional[str]=None, description: Optional[str]=None, username: Optional[str]=None, channel_type: Optional[Literal['Public', 'Private']]=None, sign_messages: Optional[bool]=None, is_restricted_content: Optional[bool]=None, reactions: Optional[Union[Literal['All', 'Disable'], List[int]]]=None)
```

Edit information of a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    title (str, optional): The new title. Max 60 characters.
    description (str, optional): The new description. Max 300 characters.
    username (str, optional): The new username. Max 32 characters.
    channel_type (str, optional): 'Public' or 'Private'. Case-insensitive.
    sign_messages (bool, optional): Whether to sign messages in the channel.
    is_restricted_content (bool, optional): Restrict content (prevent screenshots and file saving).
    reactions (Union[Literal['All', 'Disable'], List[int]], optional): 'All', 'Disable', or a list of reaction IDs.

Returns:
    The result of the API call.

### edit_channel_title

```python
edit_channel_title(self: 'darkob.Messenger', channel: str, title: str)
```

Edit title of a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    title (str): The new title of the channel.

Returns:
    The result of the API call.

### get_channel_admin_access

```python
get_channel_admin_access(self: 'darkob.Messenger', channel: str, admin: str)
```

Get the admin access list for a specific member in a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    admin (str): The GUID or username of the admin.

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
get_channel_info(self: 'darkob.Messenger', channel: str)
```

Get information about a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.

Returns:
    The result of the API call.

### get_channel_link

```python
get_channel_link(self: 'darkob.Messenger', channel: str)
```

Get the join link of a channel.

Parameters:
    channel (str): The GUID of the channel.

Returns:
    The result of the API call.

### get_channel_members

```python
get_channel_members(self: 'darkob.Messenger', channel: str, search_text: Optional[str]=None, start_id: Optional[str]=None)
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
get_channel_post_by_link(self: 'darkob.Messenger', url: str)
```

Retrieves channel post by application URL.

Parameters:
    url (str): The channel post URL.

Returns:
    Channel info and message data.

### get_channel_seen_count

```python
get_channel_seen_count(self: 'darkob.Messenger', channel: str, min_id: Union[str, int], max_id: Union[str, int])
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
get_channel_statistics(self: 'darkob.Messenger', channel: str)
```

Get all statistics for a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.

Returns:
    The result of the API call containing channel statistics.

### get_post_by_ask_link

```python
get_post_by_ask_link(self: 'darkob.Messenger', url: str)
```

Retrieves channel post by ask_join_link (go.rubika.ir link).

Parameters:
    url (str): The go.rubika.ir link.

Returns:
    Channel info and message data.

### join_channel

```python
join_channel(self: 'darkob.Messenger', channel: str)
```

Join a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.

Returns:
    Result of the API call.

### leave_channel

```python
leave_channel(self: 'darkob.Messenger', channel: str)
```

Leave a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.

Returns:
    The result of the API call.

### seen_channel_messages

```python
seen_channel_messages(self: 'darkob.Messenger', channel: str, min_id: Union[int, str], max_id: Union[int, str])
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
set_channel_link(self: 'darkob.Messenger', channel: str)
```

Set a custom link for the channel.

Parameters:
    channel (str): The GUID of the channel.

Returns:
    The result of the API call.

### set_channel_type

```python
set_channel_type(self: 'darkob.Messenger', channel: str, channel_type: Literal['Public', 'Private'])
```

Set type of a channel.

Parameters:
    channel (str): The GUID, link, or username of the channel.
    channel_type (str): The new type of the channel. 'Public' or 'Private'.

Returns:
    The result of the API call.

### update_channel_username

```python
update_channel_username(self: 'darkob.Messenger', channel: str, username: str)
```

Update the username of a channel.

Parameters:
    channel (str): The GUID or username of the channel.
    username (str): The new username. 7-32 chars, letters/numbers/underscore, cannot start with number/underscore, cannot end with underscore.

Returns:
    The result of the API call.

## users

### accept_call

```python
accept_call(self: 'darkob.Messenger', call_id: str, library_versions: Optional[List[str]]=None, max_layer: int=92, min_layer: int=65)
```

Accept an incoming call.

Parameters:
    call_id (str): The ID of the call to accept.
    library_versions (List[str], optional): List of supported library versions. Default: ['2.7.7', '2.4.4']
    max_layer (int): Maximum protocol layer. Default: 92
    min_layer (int): Minimum protocol layer. Default: 65

Returns:
    The result of the API call.

### add_contact

```python
add_contact(self: 'darkob.Messenger', phone_number: Union[str, int], first_name: str, last_name: str='')
```

Adds a contact to the client's address book.

Parameters:
    phone_number (str): The phone number of the contact to be added.
    first_name (str): The first name of the contact.
    last_name (str, optional): The last name of the contact. Defaults to an empty string.

Returns:
    The result of the API call.

Note:
    The `phone_number` parameter should be a valid phone number. The `first_name` and `last_name` parameters represent the name of the contact. If the contact has no last name, `last_name` can be an empty string.

### block_user

```python
block_user(self: 'darkob.Messenger', user: str)
```

Block a user.

Parameters:
    user (str): The GUID or username of the user to block.

Returns:
    The result of the block operation.

### call_started

```python
call_started(self: 'darkob.Messenger', call_id: str)
```

Notify the server that a call has started.

Parameters:
    call_id (str): The ID of the call that has started.

Returns:
    The result of the API call.

### check_user_username

```python
check_user_username(self: 'darkob.Messenger', username: str)
```

Check the availability of a username for a user.

Parameters:
    username (str): The username to be checked.

Returns:
    The result of the username availability check.

### delete_contact

```python
delete_contact(self: 'darkob.Messenger', user: str)
```

Deletes a contact from the client's address book.

Parameters:
    user (str): The GUID or username of the contact to be deleted.

Returns:
    The result of the contact deletion operation.

Note:
    The `user` parameter should be the GUID or username of the contact to be deleted.

### delete_user_chat

```python
delete_user_chat(self: 'darkob.Messenger', user: str)
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

### get_call_config

```python
get_call_config(self: 'darkob.Messenger')
```

Get the voice call configuration (WebRTC technical settings).

Returns:
    The result of the API call, containing the `call_config` object.

### get_call_signaling_data

```python
get_call_signaling_data(self: 'darkob.Messenger', call_id: str)
```

Get signaling data for a call (needed for WebRTC connection).

Parameters:
    call_id (str): The ID of the call.

Returns:
    The result of the API call, containing signaling data.

### get_calls

```python
get_calls(self: 'darkob.Messenger', sort: Literal['FromMin', 'FromMax']='FromMax', filter_type: Literal['All', 'Missed']='All', max_id: Optional[Union[str, int]]=None, min_id: Optional[Union[str, int]]=None)
```

Get the list of calls.

Parameters:
    sort (Literal['FromMin', 'FromMax']): Sort order. Required. Default: 'FromMax'
    filter_type (Literal['All', 'Missed']): Filter calls by type. Default: 'All'
    max_id (Union[str, int], optional): Maximum call ID for pagination. Defaults to None.
    min_id (Union[str, int], optional): Minimum call ID for pagination. Defaults to None.

Returns:
    The result of the API call.

### get_common_groups

```python
get_common_groups(self: 'darkob.Messenger', user: str)
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
get_contacts_last_online(self: 'darkob.Messenger', users: Union[str, List[str]])
```

Get the last online status of multiple users.

Parameters:
    users (Union[str, List[str]]): The GUID(s) or username(s) of the contacts.

Returns:
    Last online status for each user.

### get_contacts_stories

```python
get_contacts_stories(self: 'darkob.Messenger')
```

Get stories from contacts in the chat page.

Returns:
    The result of the API call containing contacts stories.

### get_contacts_updates

```python
get_contacts_updates(self: 'darkob.Client', state: Optional[Union[str, int]]=None)
```

Get updates related to contacts.

Parameters:
    state (Optional[Union[str, int]], optional):
        The state parameter to filter updates. Defaults to `round(time()) - 150`.

Returns:
    The update related to contacts.

### get_last_online

```python
get_last_online(self: 'darkob.Messenger', user: str)
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
get_saved_music_playlist(self: 'darkob.Messenger', user: str)
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
get_user_info(self: 'darkob.Messenger', user: Optional[str]=None)
```

Get information about a specific user.

Parameters:
    user (str, optional): The GUID or username of the user.

Returns:
    Information about the specified user.

### import_contacts

```python
import_contacts(self: 'darkob.Messenger', contacts: List[Dict[str, str]])
```

Import (upload) the phone's contacts to Rubika.

Parameters:
    contacts (List[Dict[str, str]]): A list of contacts, where each contact is a dict with 'first_name', 'last_name', and 'phone' keys.

Returns:
    The result of the API call.

### rate_call

```python
rate_call(self: 'darkob.Messenger', call_id: str, star_count: int, comment: Optional[str]=None)
```

Rate a call.

Parameters:
    call_id (str): The ID of the call to rate.
    star_count (int): Rating stars (usually 1 to 5).
    comment (str, optional): Optional comment about the call. Defaults to None.

Returns:
    The result of the API call.

### received_call

```python
received_call(self: 'darkob.Messenger', call_id: str)
```

Notify the server that an incoming call has been received.

Parameters:
    call_id (str): The ID of the received call.

Returns:
    The result of the API call.

### remove_from_top_users

```python
remove_from_top_users(self: 'darkob.Messenger', user: str)
```

Remove user from top users list.

Parameters:
    user (str): The user GUID or username to remove.

Returns:
    The result of the API call.

### request_video_call

```python
request_video_call(self: 'darkob.Messenger', user: str, library_versions: Optional[List[str]]=None, max_layer: int=92, min_layer: int=65, sip_version: int=1, support_call_out: bool=True)
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
request_voice_call(self: 'darkob.Messenger', user: str, library_versions: Optional[List[str]]=None, max_layer: int=92, min_layer: int=65, sip_version: int=1, support_call_out: bool=True)
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
reset_contacts(self: 'darkob.Messenger')
```

Reset all saved contacts for the authenticated user.

This method clears the entire contact list on the server side.

Returns:
    The result of the API call.

### send_call_signaling_data

```python
send_call_signaling_data(self: 'darkob.Messenger', call_id: str, data: str)
```

Send signaling data for a call.

Parameters:
    call_id (str): The ID of the call.
    data (str): Signaling data as a string (e.g., JSON-encoded SDP/ICE).

Returns:
    The result of the API call.

### unblock_all_users

```python
unblock_all_users(self: 'darkob.Messenger', exclude: Optional[Union[str, List[str]]]=None)
```

Unblock all blocked users.

Parameters:
    exclude (Union[str, List[str]], optional): User GUID(s) or username(s) to exclude from unblock. Default is None.

Returns:
    Result of unblock operation.

### unblock_user

```python
unblock_user(self: 'darkob.Messenger', user: str)
```

Unblock a user.

Parameters:
    user (str): The GUID or username of the user to unblock.

Returns:
    The result of the unblock operation.

## settings

### abort_set_recovery_email

```python
abort_set_recovery_email(self: 'darkob.Messenger', password: str)
```

Abort the process of setting a recovery email.

Parameters:
    password (str): The two-step verification password.

Returns:
    The result of the API call.

### abort_two_step_setup

```python
abort_two_step_setup(self: 'darkob.Messenger')
```

Abort the two-step verification setup process.

Returns:
    The result of the operation.

### add_folder

```python
add_folder(self: 'darkob.Messenger', name: str, include_chats: Optional[Union[str, List[str]]]=None, exclude_chats: Optional[Union[str, List[str]]]=None, include_chat_types: Optional[List[str]]=None, exclude_chat_types: Optional[List[str]]=None, is_add_to_top: bool=True, suggestion_folder_id: Optional[str]=None, folder_id: Optional[str]=None)
```

Add a new folder to organize chats.

Parameters:
    name (str): Folder name.
    include_chats (Union[str, List[str]], optional): Chats (GUIDs, links, usernames) to include.
    exclude_chats (Union[str, List[str]], optional): Chats to exclude.
    include_chat_types (List[str], optional): Chat types to include (case-insensitive): 'Contacts', 'NonContacts'/'Users', 'Groups', 'Channels', 'Bots', 'Services'.
    exclude_chat_types (List[str], optional): Chat types to exclude (case-insensitive): 'Mute', 'Read', 'Archive'.
    is_add_to_top (bool): Add folder to top of list.
    suggestion_folder_id (str, optional): Suggestion folder ID.

Returns:
    The result of the API call.

### add_saved_music_playlist

```python
add_saved_music_playlist(self: 'darkob.Messenger', files: Optional[Union[Path, str, List[Union[Path, str]]]]=None, file_inlines: Optional[List[dict]]=None, time: Optional[int]=None, performer: Optional[str]=None, file_name: Optional[str]=None, **kwargs)
```

Add a saved music playlist on your profile.

Parameters:
    files (Union[Path, str, List], optional): A single file path or a list of file paths.
    file_inlines (List[dict], optional): Pre-uploaded file_inline dicts to add directly.
    time (int, optional): Custom duration in seconds. Auto-detected if not provided.
    performer (str, optional): Custom performer name. Auto-detected if not provided.
    file_name (str, optional): Custom file name. Uses original file name if not provided.

Returns:
    The result of the API call.

### add_saved_music_track

```python
add_saved_music_track(self: 'darkob.Messenger', track: Optional[Union[Path, str, bytes]]=None, file_inline: Optional[dict]=None, time: Optional[int]=None, performer: Optional[str]=None, file_name: Optional[str]=None, **kwargs)
```

Add a single music track to your saved music playlist.

Parameters:
    track (Union[Path, str, bytes], optional): A file path or raw bytes.
    file_inline (dict, optional): A pre-uploaded file_inline dict to add directly.
    time (int, optional): Custom duration in seconds. Auto-detected if not provided.
    performer (str, optional): Custom performer name. Auto-detected if not provided.
    file_name (str, optional): Custom file name. Uses original file name if not provided.

Returns:
    The result of the API call.

### auto_delete_account

```python
auto_delete_account(self: 'darkob.Messenger', setting: Union[int, str])
```

Set account auto-deletion after months of inactivity.

Parameters:
    setting (Union[int, str]): Months of inactivity. Accepts: 3, 6, 12, or 24. Can be int (3, 6, 12, 24) or str ("3", "6", "12", "24", "3m", "6m", "12m", "24m").

Returns:
    The updated privacy settings.

Examples:
    >>> await client.auto_delete_account(6)  # doctest: +SKIP
    >>> await client.auto_delete_account("12m")  # doctest: +SKIP

### change_password

```python
change_password(self: 'darkob.Messenger', password: str, new_password: str, new_hint: str)
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
check_two_step_passcode(self: 'darkob.Messenger', password: str)
```

Check if the provided two-step verification password is correct.

Parameters:
    password (str): The two-step verification password to check.

Returns:
    Result containing status and user data if successful.

### confirm_unconfirmed_session

```python
confirm_unconfirmed_session(self: 'darkob.Messenger', unconfirmed_session_key: str)
```

Confirm an unconfirmed (pending) session.

Parameters:
    unconfirmed_session_key (str): The session key to confirm.

Returns:
    The result of the API call.

### delete_account

```python
delete_account(self: 'darkob.Messenger')
```

Request to permanently delete your Rubika account.

Returns:
    Confirmation message about the deletion request.

### delete_folder

```python
delete_folder(self: 'darkob.Messenger', folder_id: str)
```

Delete a folder.

Parameters:
    folder_id (str): The ID of the folder to be deleted.

Returns:
    Result of the delete folder operation.

### delete_saved_music_playlist

```python
delete_saved_music_playlist(self: 'darkob.Messenger', position: Optional[int]=None)
```

Delete tracks from the saved music playlist on your profile.

Parameters:
    position (int, optional): The position of the track to delete. If None, deletes all.

Returns:
    The result of the API call.

### deny_unconfirmed_session

```python
deny_unconfirmed_session(self: 'darkob.Messenger', unconfirmed_session_key: str)
```

Deny an unconfirmed (pending) session.

Parameters:
    unconfirmed_session_key (str): The session key to deny.

Returns:
    The result of the API call.

### disable_two_step_by_forget_password

```python
disable_two_step_by_forget_password(self: 'darkob.Messenger', code: Union[str, int])
```

Disable two-step verification using the recovery code.

Parameters:
    code (Union[str, int]): The verification code sent to the user.

Returns:
    The result of the API call.

### edit_can_called_by

```python
edit_can_called_by(self: 'darkob.Messenger', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to control who can call you.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'.
    exceptions (Dict[str, List[str]], optional): 'include_users' (always allow) and 'exclude_users' (always deny). Pass {'exclude_users': []} to clear.

Returns:
    The updated privacy settings after the change.

### edit_can_join_chat_by

```python
edit_can_join_chat_by(self: 'darkob.Messenger', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to control who can join your chats by link.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'.
    exceptions (Dict[str, List[str]], optional): 'include_users' (always allow) and 'exclude_users' (always deny). Pass {'exclude_users': []} to clear.

Returns:
    The updated privacy settings after the change.

### edit_folder

```python
edit_folder(self: 'darkob.Messenger', folder_id: str, name: Optional[str]=None, include_chats: Optional[Union[str, List[str]]]=None, exclude_chats: Optional[Union[str, List[str]]]=None, include_chat_types: Optional[List[str]]=None, exclude_chat_types: Optional[List[str]]=None, is_add_to_top: Optional[bool]=None)
```

Edit an existing folder.

Parameters:
    folder_id (str): The ID of the folder to edit.
    name (str, optional): New folder name.
    include_chats (Union[str, List[str]], optional): Chats to include.
    exclude_chats (Union[str, List[str]], optional): Chats to exclude.
    include_chat_types (List[str], optional): Chat types to include.
    exclude_chat_types (List[str], optional): Chat types to exclude.
    is_add_to_top (bool, optional): Add folder to top of list.

Returns:
    The result of the API call.

### edit_show_birthday

```python
edit_show_birthday(self: 'darkob.Messenger', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to show or hide the user's birthday.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'.
    exceptions (Dict[str, List[str]], optional): 'include_users' (always allow) and 'exclude_users' (always deny). Pass {'exclude_users': []} to clear.

Returns:
    The updated privacy settings after the change.

### edit_show_last_online

```python
edit_show_last_online(self: 'darkob.Messenger', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to control who can see the user's last online status.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'.
    exceptions (Dict[str, List[str]], optional): 'include_users' (always allow) and 'exclude_users' (always deny). Pass {'exclude_users': []} to clear.

Returns:
    The updated privacy settings after the change.

### edit_show_phone_number

```python
edit_show_phone_number(self: 'darkob.Messenger', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to control who can see the user's phone number.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'.
    exceptions (Dict[str, List[str]], optional): 'include_users' (always allow) and 'exclude_users' (always deny). Pass {'exclude_users': []} to clear.

Returns:
    The updated privacy settings after the change.

### edit_show_profile_photo

```python
edit_show_profile_photo(self: 'darkob.Messenger', setting: str, exceptions: Optional[Dict[str, List[str]]]=None)
```

Edits the setting to control who can see the user's profile photo.

Parameters:
    setting (str): 'Everybody', 'MyContacts' or 'Nobody'.
    exceptions (Dict[str, List[str]], optional): 'include_users' (always allow) and 'exclude_users' (always deny). Pass {'exclude_users': []} to clear.

Returns:
    The updated privacy settings after the change.

### get_appearance_setting

```python
get_appearance_setting(self: 'darkob.Messenger')
```

Get the user's appearance settings (chat background, font size, emoji, night mode, themes, etc.).

Returns:
    The result of the API call, containing the `appearance_setting` object.

### get_data_setting

```python
get_data_setting(self: 'darkob.Messenger')
```

Get the user's data and media auto-download settings.

Returns:
    The result of the API call, containing the `data_setting` object.

### get_device_setting

```python
get_device_setting(self: 'darkob.Messenger')
```

Get all device settings (data, appearance, and notification).

Returns:
    The result of the API call, containing `data_setting`, `appearance_setting`, and `notification_setting`.

### get_folders

```python
get_folders(self: 'darkob.Messenger', last_state: Union[int, str]=None)
```

Get a list of folders.

Parameters:
    last_state (Union[int, str]): The last state to retrieve folders.

Returns:
    List of folders.

### get_my_sessions

```python
get_my_sessions(self: 'darkob.Messenger')
```

Get information about the current user's sessions.

Returns:
    Information about the user's sessions.

### get_notification_setting

```python
get_notification_setting(self: 'darkob.Messenger')
```

Retrieves the current notification settings for the account.

Returns:
    The result of the API call.

### get_privacy_setting

```python
get_privacy_setting(self: 'darkob.Messenger')
```

Get the current user's privacy setting.

Returns:
    The current user's privacy setting.

### get_suggested_folders

```python
get_suggested_folders(self: 'darkob.Messenger')
```

Get the suggested folders for the user.

Returns:
    The suggested folders for the user.

### get_two_passcode_status

```python
get_two_passcode_status(self: 'darkob.Messenger')
```

Get the two-passcode status for the user.

Returns:
    The two-passcode status for the user.

### get_unconfirmed_sessions

```python
get_unconfirmed_sessions(self: 'darkob.Messenger')
```

Get a list of unconfirmed (pending) sessions for the current account.

Returns:
    The result of the API call containing unconfirmed sessions.

### get_user_setting

```python
get_user_setting(self: 'darkob.Messenger')
```

Get user account settings, similar to `get_privacy_setting`.

Returns:
    The result of the API call. Includes the `privacy_setting` object (same as `get_privacy_setting`) plus an additional `access_list`.

### login_disable_two_step

```python
login_disable_two_step(self: 'darkob.Messenger', phone_number: str, email_code: str, forget_password_code_hash: str)
```

Disable two-step verification during login.

Parameters:
    phone_number (str): The phone number associated with the account.
    email_code (str): The verification code sent to email.
    forget_password_code_hash (str): The code hash for forgotten password flow.

Returns:
    The result of the API call.

### login_two_step_forget_password

```python
login_two_step_forget_password(self: 'darkob.Messenger', phone_number: str)
```

Start the password recovery process for two-step verification.

Use this when the user has forgotten their two-step verification password. This will initiate the recovery flow (e.g. sending a code to email/phone).

Parameters:
    phone_number (str): The phone number associated with the account.

Returns:
    The result of the API call, typically containing a hash or instructions for the next step of recovery.

### logout

```python
logout(self: 'darkob.Messenger', confirm: bool=True)
```

Log out of the current session.

Parameters:
    confirm (bool): If True, ask the user for confirmation before logging out. If False, log out immediately. Default is True.

Returns:
    The result of the logout operation if confirmed. Exits if cancelled.

### register_device

```python
register_device(self: 'darkob.Messenger', device_model: Optional[str]=None, *args, **kwargs)
```

Register the current device with the Rubika server.

Parameters:
    device_model (str, optional):
        Custom device model name.

Returns:
    The result of the API call.

### reorder_folder

```python
reorder_folder(self: 'darkob.Messenger', folder_ids: Union[str, List[str]])
```

Reorder folders.

Parameters:
    folder_ids (Union[str, List[str]]): A single folder ID or a list of folder IDs in the new order.

Returns:
    The result of the API call.

### request_change_phone_number

```python
request_change_phone_number(self: 'darkob.Messenger', new_phone_number: str)
```

Request to change the account phone number.

Parameters:
    new_phone_number (str): The new phone number (e.g., 09123456789, +989123456789, +1234567890).

Returns:
    The result of the API call containing phone_code_hash for verification.

### request_forget_password

```python
request_forget_password(self: 'darkob.Messenger')
```

Request to reset the account password.

Returns:
    The result of the API call.

### request_recovery_email

```python
request_recovery_email(self: 'darkob.Messenger', password: str, recovery_email: str)
```

Request a recovery code to be sent to the recovery email.

Parameters:
    password (str): User's current password.
    recovery_email (str): Recovery email address.

Returns:
    The result of the API call.

### resend_code_recovery_email

```python
resend_code_recovery_email(self: 'darkob.Messenger', password: str)
```

Resend the recovery email verification code.

Parameters:
    password (str): The two-step verification password.

Returns:
    The result of the API call.

### set_appearance_setting

```python
set_appearance_setting(self: 'darkob.Messenger', large_emoji: Optional[bool]=None, android_font_size: Optional[int]=None, auto_night_mode: Optional[bool]=None, auto_night_mode_type: Optional[NightModeType]=None, message_corner: Optional[int]=None, chat_list_view: Optional[ChatListViewType]=None, chat_list_swipe_gesture: Optional[SwipeGestureType]=None, scheduled_use_local_sunset: Optional[bool]=None, scheduled_from_time: Optional[Dict[str, int]]=None, scheduled_to_time: Optional[Dict[str, int]]=None, adaptive_brightness_threshold: Optional[int]=None, direct_share: Optional[bool]=None, enable_animation: Optional[bool]=None, save_to_gallery: Optional[bool]=None, send_by_enter: Optional[bool]=None, default_tab: Optional[str]=None, quick_reaction: Optional[Dict[str, str]]=None)
```

Update appearance settings (excluding theme and theme background).

Parameters:
    large_emoji (bool, optional): Enable/disable large emojis.
    android_font_size (int, optional): Font size for Android.
    auto_night_mode (bool, optional): Enable/disable auto night mode.
    auto_night_mode_type (str, optional): 'Disable', 'Scheduled', 'Adaptive'. Case-insensitive.
    message_corner (int, optional): Message bubble corner radius.
    chat_list_view (str, optional): 'TwoLines' or 'ThreeLines'. Case-insensitive.
    chat_list_swipe_gesture (str, optional): 'ChangeFolder', 'Pin', 'Read', 'Mute', 'Delete'. Case-insensitive.
    scheduled_use_local_sunset (bool, optional): Use local sunset for scheduled night mode.
    scheduled_from_time (Dict[str, int], optional): Scheduled night mode start time (e.g., {'hour': 20, 'minute': 0}).
    scheduled_to_time (Dict[str, int], optional): Scheduled night mode end time (e.g., {'hour': 7, 'minute': 0}).
    adaptive_brightness_threshold (int, optional): Adaptive brightness threshold.
    direct_share (bool, optional): Enable/disable direct share.
    enable_animation (bool, optional): Enable/disable animations.
    save_to_gallery (bool, optional): Enable/disable saving to gallery.
    send_by_enter (bool, optional): Enable/disable sending by Enter key.
    default_tab (str, optional): Default tab.
    quick_reaction (Dict[str, str], optional): Quick reaction with 'reaction_id', 'emoji_char', and 'name'.

Returns:
    The updated settings.

### set_data_setting

```python
set_data_setting(self: 'darkob.Messenger', auto_download_media: Optional[bool]=None, wifi_auto_download: Optional[bool]=None, cellular_auto_download: Optional[bool]=None, gif_auto_play: Optional[bool]=None, video_auto_play: Optional[bool]=None, stream_videos_and_audio_files: Optional[bool]=None, keep_media: Optional[KeepMediaType]=None, wifi_photo_auto_download: Optional[Dict[str, int]]=None, cellular_photo_auto_download: Optional[Dict[str, int]]=None, wifi_video_auto_download: Optional[Dict[str, int]]=None, cellular_video_auto_download: Optional[Dict[str, int]]=None, wifi_file_auto_download: Optional[Dict[str, int]]=None, cellular_file_auto_download: Optional[Dict[str, int]]=None, wifi_gif_auto_download: Optional[Dict[str, int]]=None, cellular_gif_auto_download: Optional[Dict[str, int]]=None, wifi_music_auto_download: Optional[Dict[str, int]]=None, cellular_music_auto_download: Optional[Dict[str, int]]=None)
```

Update data (auto-download) settings.

Parameters:
    auto_download_media (bool, optional): Global auto-download toggle.
    wifi_auto_download (bool, optional): WiFi auto-download toggle.
    cellular_auto_download (bool, optional): Cellular auto-download toggle.
    gif_auto_play (bool, optional): Auto-play GIFs.
    video_auto_play (bool, optional): Auto-play videos.
    stream_videos_and_audio_files (bool, optional): Stream videos and audio.
    keep_media (str, optional): Keep media duration. Only 'Forever' is accepted.
    wifi_photo_auto_download (dict, optional): Auto-download config with 'max_download_size' and contact/user/group/channel keys.
    cellular_photo_auto_download (dict, optional): Same as above for cellular.
    wifi_video_auto_download (dict, optional): Same as above for video on WiFi.
    cellular_video_auto_download (dict, optional): Same as above for video on cellular.
    wifi_file_auto_download (dict, optional): Same as above for files on WiFi.
    cellular_file_auto_download (dict, optional): Same as above for files on cellular.
    wifi_gif_auto_download (dict, optional): Same as above for GIFs on WiFi.
    cellular_gif_auto_download (dict, optional): Same as above for GIFs on cellular.
    wifi_music_auto_download (dict, optional): Same as above for music on WiFi.
    cellular_music_auto_download (dict, optional): Same as above for music on cellular.

Returns:
    The updated device settings.

### set_notification

```python
set_notification(self: 'darkob.Messenger', user_notification: Optional[bool]=None, user_message_preview: Optional[bool]=None, group_notification: Optional[bool]=None, group_message_preview: Optional[bool]=None, channel_notification: Optional[bool]=None, channel_message_preview: Optional[bool]=None, in_app_sound: Optional[bool]=None, in_app_preview: Optional[bool]=None, new_contacts: Optional[bool]=None)
```

Update notification settings. (Deprecated)

.. deprecated::
    This method is deprecated and will be removed soon.
    Use `set_notification_setting` instead.

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

### set_notification_setting

```python
set_notification_setting(self: 'darkob.Messenger', user_notification: Optional[bool]=None, user_message_preview: Optional[bool]=None, group_notification: Optional[bool]=None, group_message_preview: Optional[bool]=None, channel_notification: Optional[bool]=None, channel_message_preview: Optional[bool]=None, in_app_sound: Optional[bool]=None, in_app_preview: Optional[bool]=None, new_contacts: Optional[bool]=None, user_notification_popup: Optional[PopupType]=None, group_notification_popup: Optional[PopupType]=None, channel_notification_popup: Optional[PopupType]=None, user_notification_importance: Optional[ImportanceType]=None, group_notification_importance: Optional[ImportanceType]=None, channel_notification_importance: Optional[ImportanceType]=None, user_notification_vibrate: Optional[VibrateType]=None, group_notification_vibrate: Optional[VibrateType]=None, channel_notification_vibrate: Optional[VibrateType]=None, in_app_vibrate: Optional[bool]=None, vibrate_voice_calls: Optional[VibrateType]=None)
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
    user_notification_popup (str, optional): 'NoPopup', 'OnlyScreenOn', 'OnlyScreenOff', 'Always'. Case-insensitive.
    group_notification_popup (str, optional): Same as user.
    channel_notification_popup (str, optional): Same as user.
    user_notification_importance (str, optional): 'Low', 'Medium', 'High', 'Urgent'. Case-insensitive.
    group_notification_importance (str, optional): Same as user.
    channel_notification_importance (str, optional): Same as user.
    user_notification_vibrate (str, optional): 'Disabled', 'Default', 'Short', 'Long', 'OnlySilent'. Case-insensitive.
    group_notification_vibrate (str, optional): Same as user.
    channel_notification_vibrate (str, optional): Same as user.
    in_app_vibrate (bool, optional): Enable/disable in-app vibrate.
    vibrate_voice_calls (str, optional): 'Disabled', 'Default', 'Short', 'Long', 'OnlySilent'. Case-insensitive.

Returns:
    The updated notification settings.

### set_privacy_setting

```python
set_privacy_setting(self: 'darkob.Messenger', show_my_last_online: Optional[PrivacyValue]=None, show_my_phone_number: Optional[PrivacyValue]=None, show_my_profile_photo: Optional[PrivacyValue]=None, link_forward_message: Optional[PrivacyValue]=None, can_join_chat_by: Optional[PrivacyValue]=None, show_my_birth_date: Optional[PrivacyValue]=None, can_called_by: Optional[PrivacyValue]=None, auto_delete_messages: Optional[Union[str, int]]=None, inactive_account_delete: Optional[int]=None, show_my_last_online_exceptions: Optional[Dict[str, List[str]]]=None, show_my_phone_number_exceptions: Optional[Dict[str, List[str]]]=None, show_my_profile_photo_exceptions: Optional[Dict[str, List[str]]]=None, can_join_chat_by_exceptions: Optional[Dict[str, List[str]]]=None, show_my_birth_date_exceptions: Optional[Dict[str, List[str]]]=None, can_called_by_exceptions: Optional[Dict[str, List[str]]]=None)
```

Update privacy and auto-delete settings.

Parameters:
    Privacy Settings (accept: 'Everybody', 'MyContacts', 'Nobody'):
        show_my_last_online (str, optional): Who can see your last online status.
        show_my_phone_number (str, optional): Who can see your phone number.
        show_my_profile_photo (str, optional): Who can see your profile photo.
        link_forward_message (str, optional): Who can forward your message links.
        can_join_chat_by (str, optional): Who can join your chats by link.
        show_my_birth_date (str, optional): Who can see your birth date.
        can_called_by (str, optional): Who can call you.

    Exceptions (for privacy settings except link_forward_message):
        Each exception should be a dict with 'include_users' and 'exclude_users' (List[str]).

    Auto Delete Messages:
        auto_delete_messages (Union[str, int], optional): Message auto-delete duration.

    Delete Inactive Account:
        inactive_account_delete (int, optional): Delete account after X months.

Returns:
    The updated privacy settings.

### set_quick_reaction

```python
set_quick_reaction(self: 'darkob.Messenger', reaction_id: Union[str, int], emoji_char: str, name: str)
```

Set the quick reaction for the current user.

Parameters:
    reaction_id (str): The reaction ID.
    emoji_char (str): The emoji character (e.g., '👍').
    name (str): The reaction name (e.g., 'Thumbs Up').

Returns:
    The updated settings.

### set_saved_music_playlist

```python
set_saved_music_playlist(self: 'darkob.Messenger', files: Optional[Union[Path, str, List[Union[Path, str]]]]=None, file_inlines: Optional[List[dict]]=None, time: Optional[int]=None, performer: Optional[str]=None, file_name: Optional[str]=None, **kwargs)
```

Replace the saved music playlist on your profile.

Parameters:
    files (Union[Path, str, List], optional): A single file path or a list of file paths.
    file_inlines (List[dict], optional): Pre-uploaded file_inline dicts to set directly.
    time (int, optional): Custom duration in seconds. Auto-detected if not provided.
    performer (str, optional): Custom performer name. Auto-detected if not provided.
    file_name (str, optional): Custom file name. Uses original file name if not provided.

Returns:
    The result of the API call.

### set_setting

```python
set_setting(self: 'darkob.Messenger', show_my_last_online: Optional[PrivacyValue]=None, show_my_phone_number: Optional[PrivacyValue]=None, show_my_profile_photo: Optional[PrivacyValue]=None, link_forward_message: Optional[PrivacyValue]=None, can_join_chat_by: Optional[PrivacyValue]=None, show_my_birth_date: Optional[PrivacyValue]=None, can_called_by: Optional[PrivacyValue]=None, auto_delete_messages: Optional[Union[str, int]]=None, inactive_account_delete: Optional[int]=None, show_my_last_online_exceptions: Optional[Dict[str, List[str]]]=None, show_my_phone_number_exceptions: Optional[Dict[str, List[str]]]=None, show_my_profile_photo_exceptions: Optional[Dict[str, List[str]]]=None, can_join_chat_by_exceptions: Optional[Dict[str, List[str]]]=None, show_my_birth_date_exceptions: Optional[Dict[str, List[str]]]=None, can_called_by_exceptions: Optional[Dict[str, List[str]]]=None)
```

Set various privacy and auto-delete settings for the user.

.. deprecated::
    This method is deprecated and will be removed soon.
    Use `set_privacy_setting` instead.

Parameters:
    See `set_privacy_setting` for detailed parameter descriptions.

Returns:
    The updated privacy settings.

### set_theme

```python
set_theme(self: 'darkob.Messenger', theme_id: str)
```

Activate a theme for the current user.

Parameters:
    theme_id (str): The theme ID to activate.

Returns:
    The updated appearance settings.

### set_theme_background

```python
set_theme_background(self: 'darkob.Messenger', theme_id: str, type: Literal['System', 'ClientTheme']='ClientTheme', chat_background_type: Literal['Color', 'Wallpaper']='Wallpaper', wallpaper_id: Optional[str]=None, color: Optional[Dict[str, int]]=None)
```

Set the background of a theme via setSetting.

Parameters:
    theme_id (str): Target theme ID.
    type (str): Theme type. 'System' or 'ClientTheme'. Case-insensitive. Default: 'ClientTheme'.
    chat_background_type (str): Background type. 'Color' or 'Wallpaper'. Case-insensitive. Default: 'Wallpaper'.
    wallpaper_id (str, optional): Wallpaper ID (required if chat_background_type='Wallpaper').
    color (dict, optional): RGBA color dict (required if chat_background_type='Color').

Returns:
    The updated appearance settings after applying the change.

### set_two_step_verification

```python
set_two_step_verification(self: 'darkob.Messenger', password: Union[int, str], hint: Optional[str]=None, recovery_email: Optional[str]=None)
```

Set up two-step verification for the user.

Parameters:
    password (Union[int, str]): The current user password.
    hint (str, optional): A hint to help remember the password.
    recovery_email (str, optional): The recovery email for two-step verification.

Returns:
    The updated user information after setting up two-step verification.

### terminate_other_sessions

```python
terminate_other_sessions(self: 'darkob.Messenger')
```

Terminate other account sessions.

Returns:
    The result of the API call.

### terminate_session

```python
terminate_session(self: 'darkob.Messenger', session_key: str)
```

Terminate a user session.

Parameters:
    session_key (str): The session key of the session to be terminated.

Returns:
    The result of the API call.

### turn_off_two_step

```python
turn_off_two_step(self: 'darkob.Messenger', password: str)
```

Turn off two-step verification passcode for the account.

Parameters:
    password (str): Current two-step verification password

Returns:
    Result of the operation.

### update_my_bio

```python
update_my_bio(self: 'darkob.Messenger', bio: str)
```

Update user's biography.

Parameters:
    bio (str): The updated biography (max 150 characters).

Returns:
    The updated user information.

### update_my_birthday

```python
update_my_birthday(self: 'darkob.Messenger', birthday: Union[str, datetime])
```

Update the birthday in your profile.

Parameters:
    birthday (Union[str, datetime]): Birthday in format YYYY-MM-DD (e.g., "2026-02-03") or a datetime object.

Returns:
    The updated user information.

### update_my_name

```python
update_my_name(self: 'darkob.Messenger', first_name: Optional[str]=None, last_name: Optional[str]=None)
```

Update user's first name and/or last name.

Parameters:
    first_name (str, optional): The updated first name (max 30 characters).
    last_name (str, optional): The updated last name (max 50 characters).

Returns:
    The updated user information.

### update_my_profile

```python
update_my_profile(self: 'darkob.Messenger', first_name: Optional[str]=None, last_name: Optional[str]=None, bio: Optional[str]=None, birthday: Optional[str]=None, location: Optional[Dict[str, Union[float, Dict[str, Union[int, List[str], float]]]]]=None)
```

Update user profile information.

Parameters:
    first_name (str, optional): The updated first name (max 30 characters).
    last_name (str, optional): The updated last name (max 50 characters).
    bio (str, optional): The updated biography (max 150 characters).
    birthday (str, optional): Birthday in format YYYY-MM-DD (e.g., "2026-07-05").
    location (dict, optional): Location with keys: longitude (float), latitude (float), map_view (dict with tile_side_count, tile_urls, x_loc, y_loc).

Returns:
    The updated user information after the profile update.

### update_my_username

```python
update_my_username(self: 'darkob.Messenger', username: str)
```

Update the username of the user.

Parameters:
    username (str): The new username (7-32 chars, letters/numbers/underscore, cannot start with number/underscore, cannot end with underscore).

Returns:
    The updated user information.

### upgrade_to_api6

```python
upgrade_to_api6(self: 'darkob.Messenger', save_as: bool=True, file_name: Optional[str]=None)
```

Upgrade from API v5 to v6 by setting an RSA public key.

This allows old v5 auth keys to be used with API v6.
After upgrade, save the returned private_key for future v6 logins.

Parameters:
    save_as (bool): If True (default), saves auth and private_key to a JSON file.
    file_name (str, optional): Custom file name for the JSON file. Defaults to 'darkob_{auth[:10]}'.

Returns:
    Data: Response with status, message, auth, and private_key.

### upload_wallpaper

```python
upload_wallpaper(self: 'darkob.Messenger', theme_id: str, main_image: Optional[Union[Path, str, bytes]]=None, thumbnail_image: Optional[Union[Path, str, bytes]]=None, main_file_id: Optional[Union[str, int]]=None, main_access_hash_rec: Optional[str]=None, thumbnail_file_id: Optional[Union[str, int]]=None, thumb_access_hash_rec: Optional[str]=None, *args, **kwargs)
```

Upload a wallpaper for a theme.

Parameters:
    theme_id (str): Target theme ID (obtainable via get_themes).
    main_image (Path | str | bytes, optional): The main wallpaper file or bytes.
    thumbnail_image (Path | str | bytes, optional): The thumbnail file or bytes. Reuses main if not provided.
    main_file_id (Union[str, int], optional): Pre-uploaded main wallpaper file ID.
    main_access_hash_rec (str, optional): Pre-uploaded main wallpaper access hash.
    thumbnail_file_id (Union[str, int], optional): Pre-uploaded thumbnail file ID.
    thumb_access_hash_rec (str, optional): Pre-uploaded thumbnail access hash.

Returns:
    The result of the API call.

### verify_change_phone_number

```python
verify_change_phone_number(self: 'darkob.Messenger', code: Union[str, int], hash: str)
```

Verify phone number change with the received code.

Parameters:
    code (Union[str, int]): The verification code sent to the new phone number.
    hash (str): The hash received from request_change_phone_number.

Returns:
    The result of the API call.

### verify_recovery_email

```python
verify_recovery_email(self: 'darkob.Messenger', password: str, code: Union[str, int])
```

Verify the recovery code sent to the recovery email.

Parameters:
    password (str): User's current password.
    code (Union[str, int]): The verification code received in email.

Returns:
    The result of the API call.

## extras

### add_live_comment

```python
add_live_comment(self: 'darkob.Messenger', *args, live_id: str=_UNSET, access_token: str=_UNSET, comment: str=_UNSET)
```

Adds a comment to a live stream.

Keyword arguments are canonical and unambiguous. Positional arguments
accept both legacy ``(access_token, live_id, comment)`` and upstream
``(live_id, access_token, comment)``. Upstream order is selected only
when the first argument is all digits and the second starts with
``u0`` or ``b0``; otherwise legacy order is retained, since arbitrary
strings cannot always be distinguished reliably.

Parameters:
    live_id (str): The ID of the live stream.
    access_token (str): The access token for authentication.
    comment (str): The text of the comment.

Returns:
    The result of the API call.

### add_sticker_set

```python
add_sticker_set(self: 'darkob.Messenger', sticker_set_id: str)
```

Add a sticker set.

Parameters:
    sticker_set_id (str): The ID of the sticker set.

Returns:
    The result of the API call.

### add_to_my_gif_set

```python
add_to_my_gif_set(self: 'darkob.Messenger', chat: str, message_id: Union[str, int])
```

Adds a GIF message to the user's personal GIF set.

Parameters:
    chat (str): The GUID, link, or username of the chat.
    message_id (Union[str, int]): The ID of the GIF message.

Returns:
    The result of the API call.

### archive_sticker_set

```python
archive_sticker_set(self: 'darkob.Messenger', sticker_set_id: str)
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
delete_my_gif_set(self: 'darkob.Messenger', file_id: str)
```

Deletes a GIF from the user's personal GIF set.

Parameters:
    file_id (str): The file ID of the GIF to be removed.

Returns:
    The result of the API call.

### delete_sticker_set

```python
delete_sticker_set(self: 'darkob.Messenger', sticker_set_id: str)
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
get_available_reactions(self: 'darkob.Messenger')
```

Retrieve the list of available message reactions that can be used in chats.

Returns:
    Shows available reactions data from the server.

### get_current_live_location

```python
get_current_live_location(self: 'darkob.Messenger', live_loc_track_id: str)
```

Get the current live location by its track ID.

Parameters:
    live_loc_track_id (str): The live location track ID.

Returns:
    The result of the API call.

### get_link_from_app_url

```python
get_link_from_app_url(self: 'darkob.Messenger', url: str)
```

Get a direct link from an application URL.

Parameters:
    url (str): The application URL to extract the link from.

Returns:
    The result containing the extracted link.

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
get_live_play_url(self: 'darkob.Messenger', *args, live_id: str=_UNSET, access_token: str=_UNSET)
```

Retrieves the play URL for a live stream.

Keyword arguments are canonical and unambiguous. Positional arguments
accept both legacy ``(access_token, live_id)`` and upstream
``(live_id, access_token)``. Upstream order is selected only when the
first argument is all digits and the second starts with ``u0`` or
``b0``; otherwise legacy order is retained, since arbitrary strings
cannot always be distinguished reliably.

Parameters:
    live_id (str): The ID of the live stream.
    access_token (str): The access token for authentication.

Returns:
    The result of the API call.

### get_live_replay_viewers

```python
get_live_replay_viewers(self: 'darkob.Messenger', live_id: str, start_id: Optional[str]=None)
```

Get the list of replay (VOD) viewers for a live stream.

Parameters:
    live_id (str): Live stream ID.
    start_id (str, optional): The starting viewer ID for pagination. Defaults to None.

Returns:
    The result of the API call, containing a list of replay viewers.

### get_live_report

```python
get_live_report(self: 'darkob.Messenger', live_id: str)
```

Get the report and statistics of a completed live stream.

Parameters:
    live_id (str): The ID of the live stream.

Returns:
    The result of the API call, containing live stats and graphs.

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

### get_live_viewers

```python
get_live_viewers(self: 'darkob.Messenger', live_id: str, start_id: Optional[str]=None)
```

Get the list of viewers for a live stream.

Parameters:
    live_id (str): Live stream ID.
    start_id (str, optional): The starting viewer ID for pagination. Defaults to None.

Returns:
    The result of the API call, containing a list of viewers.

### get_location_view

```python
get_location_view(self: 'darkob.Messenger', latitude: float, longitude: float)
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
get_sticker_set_by_id(self: 'darkob.Messenger', sticker_set_id: str)
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
get_stickers_by_set_ids(self: 'darkob.Messenger', sticker_set_ids: Union[str, list])
```

Get stickers by set IDs.

Parameters:
    sticker_set_ids (Union[str, list]): The sticker set ID or a list of sticker set IDs.

Returns:
    Stickers corresponding to the provided set IDs.

### get_themes

```python
get_themes(self: 'darkob.Messenger')
```

Get the list of available themes.

Returns:
    The result of the API call, containing the list of themes.

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
get_wallet_transaction_message(self: 'darkob.Messenger', transfer_id: str, access_transfer: str)
```

Get the message associated with a wallet transaction.

Parameters:
    transfer_id (str): The ID of the wallet transaction.
    access_transfer (str): The access hash for the transaction.

Returns:
    The result of the API call.

### get_wallpapers

```python
get_wallpapers(self: 'darkob.Messenger')
```

Get the current chat wallpaper settings.

Returns:
    The result of the API call containing wallpaper information.

### reorder_sticker_sets

```python
reorder_sticker_sets(self: 'darkob.Messenger', ordered_sticker_set_ids: Union[str, List[str]])
```

Reorder sticker sets in the user's collection.

Parameters:
    ordered_sticker_set_ids (Union[str, List[str]]): A single sticker set ID or a list of sticker set IDs in the desired order.

Returns:
    The result of the API call.

### report_live

```python
report_live(self: 'darkob.Messenger', live_id: str, report_type: Union[int, str], description: Optional[str]=None)
```

Report a live stream.

Parameters:
    live_id (str): The ID of the live stream to report.
    report_type (Union[int, str]): The report reason. Can be an integer code between 100 and 106, or a string name (case-insensitive): 'Other', 'Violence', 'Spam', 'Porn', 'ChildAbuse', 'Copyright', 'Fraud'. If set to 100 (Other), `description` becomes required.
    description (str, optional): Description for the report. Required when `report_type` is 100 (Other).

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

### set_live_setting

```python
set_live_setting(self: 'darkob.Messenger', live_id: str, title: Optional[str]=None, allow_comment: Optional[bool]=None)
```

Update settings for a live stream.

Parameters:
    live_id (str): Live stream ID.
    title (str, optional): New title for the live stream.
    allow_comment (bool, optional): Whether to allow comments on the live stream.

Returns:
    The result of the API call.

### stop_live

```python
stop_live(self: 'darkob.Messenger', live_id: str)
```

Stop a live stream.

Parameters:
    live_id (str): Live stream ID.

Returns:
    The result of the API call.

### stop_live_location

```python
stop_live_location(self: 'darkob.Messenger', live_loc_track_id: str)
```

Stop a live location by its track ID.

Parameters:
    live_loc_track_id (str): The live location track ID.

Returns:
    The result of the API call.

## bots

### delete_bot_chat

```python
delete_bot_chat(self: 'darkob.Messenger', bot: str)
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
get_bot_info(self: 'darkob.Messenger', bot: str)
```

Get information about a bot.

Parameters:
    bot (str): The GUID or username of the bot.

Returns:
    The result of the API call.

### get_inline_bots

```python
get_inline_bots(self: 'darkob.Messenger', bots: Union[str, List[str]])
```

Retrieve information about inline bots by their GUIDs or usernames.

Parameters:
    bots (Union[str, List[str]]): A single bot GUID/username or a list of bot GUIDs/usernames.

Returns:
    The result of the API call.

### get_service_info

```python
get_service_info(self: 'darkob.Messenger', service: str)
```

Get information about a service.

Parameters:
    service (str): The GUID of the service.

Returns:
    The result of the API call.

### start_bot

```python
start_bot(self: 'darkob.Messenger', bot: str)
```

Start a bot.

Parameters:
    bot (str): The GUID or username of the bot.

Returns:
    The result of the API call.

### stop_bot

```python
stop_bot(self: 'darkob.Messenger', bot: str)
```

Stop a bot.

Parameters:
    bot (str): The GUID or username of the bot.

Returns:
    The result of the API call.

## base

### close

```python
close(self: 'darkob.Messenger')
```

Close the connection to the Darkob server (async version).

### connect

```python
connect(self: 'darkob.Messenger')
```

Establish a connection to the Rubika API.

Creates an Api instance and loads stored session information
(auth, guid, private_key, user_agent) if available.

Returns:
    Messenger instance with active connection.

### disconnect

```python
disconnect(self: 'darkob.Messenger')
```

Disconnect from the Darkob server (sync version).

### download_file

```python
download_file(self: 'darkob.Messenger', file_inline: Optional[Union[dict, 'Data']]=None, dc_id: Optional[int]=None, file_id: Optional[int]=None, access_hash: Optional[str]=None, size: Optional[int]=None, chunk: int=131072, callback: Optional[Callable[[int, int], Optional['asyncio.Future']]]=None, gather: bool=False, save_as: Optional[Union[str, bool]]=None, file_name: Optional[str]=None, as_base64: bool=False)
```

Download a file from Rubika/Shad.

Parameters:
    file_inline (dict | Data, optional): File inline object from messages.
        If provided, dc_id, file_id, access_hash, size will be extracted.
    dc_id (int, optional): Data Center ID (if file_inline not provided).
    file_id (int, optional): Unique identifier of the file.
    access_hash (str, optional): Access hash associated with the file.
    size (int, optional): Total size of the file in bytes.
    chunk (int, optional): Size of each download chunk (default: 131072).
    callback (callable, optional): Progress callback(total_size, downloaded_size).
    gather (bool, optional): Download chunks in parallel (default: False).
    save_as (str | bool, optional): Directory path or True for current dir. If None, returns bytes.
    file_name (str, optional): Custom file name.
    as_base64 (bool, optional): Return as base64 encoded string (default: False).

Returns:
    bytes, str, or Data: File content (bytes), base64 string, or Data object (when save_as used).

### get_string_session

```python
get_string_session(self: 'darkob.Messenger', password: Optional[str]=None)
```

Export current session as an encrypted StringSession.

Parameters:
    password (str, optional): Optional password for encryption.
        If provided, StringSession can only be opened with this password.

Returns:
    str: Encrypted StringSession that can be used later with
         `Messenger(string_session=..., password=...)`.

### get_updates

```python
get_updates(self: 'darkob.Messenger')
```

Listen for updates from Rubika's WebSocket.

Returns:
    None

### request

```python
request(self: 'darkob.Messenger', method: str, input: Optional[Dict]=None, tmp_session: bool=False, encrypt: bool=True)
```

Build and send a request to the Rubika API.

Parameters:
    method (str): API method name (e.g., 'sendMessage', 'getUserInfo').
    input (dict, optional): Input data for the method.
    tmp_session (bool): Use temporary session instead of auth (default: False).
    encrypt (bool): Encrypt the request data (default: True).

Returns:
    Data, Event, dict, or None: The API response.
        - If `as_dict=True` on the client, returns a plain dict.
        - Otherwise, returns a Data object.

Raises:
    NoConnection: If the client has not been started and `tmp_session=False`.

### run

```python
run(self: 'darkob.Messenger', coroutine: Optional[Coroutine]=None)
```

Start the client and listen for updates.

Parameters:
    coroutine (Coroutine, optional): Optional coroutine to run before listening for updates.

Returns:
    None when used normally (runs forever until stopped).

### send_code

```python
send_code(self: 'darkob.Messenger', phone_number: str, pass_key: Optional[str]=None)
```

Send a verification code to a phone number.

Parameters:
    phone_number (str): The target phone number.
    pass_key (str, optional): The optional account pass key.

Returns:
    The result of the API call.

### sign_in

```python
sign_in(self: 'darkob.Messenger', phone_number: str, phone_code: str, phone_code_hash: str, public_key: str)
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
start(self: 'darkob.Messenger', phone_number: Optional[str]=None)
```

Start the client, handling authentication and registration.

Parameters:
    phone_number (str, optional): Phone number for registration.

Returns:
    Messenger: The initialized client instance.

### upload_file

```python
upload_file(self: 'darkob.Messenger', file: Union[str, bytes, None]=None, base64_data: Optional[str]=None, mime: Optional[str]=None, file_name: Optional[str]=None, chunk: int=1048576, callback: Optional[Callable[[int, int], Optional['asyncio.Future']]]=None)
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
    Data or dict: Metadata about the uploaded file.
        - If `as_dict=True` on the client, returns a plain dict.
        - Otherwise, returns a Data object.

## core

### add_handler

```python
add_handler(self: 'darkob.Client', func: Callable, handler: Union[ChatUpdates, MessageUpdates, ShowActivities, ShowNotifications, RemoveNotifications])
```

_No docstring available._

### ask

```python
ask(self, chat_id: str, text: Optional[str]=None, *, filters: Optional[list]=None, timeout: float=60.0, inline_keypad: Any=None, chat_keypad: Any=None)
```

Send a prompt and await the next matching reply in that chat.

The reply is returned to you instead of being dispatched to
handlers while the prompt is pending.

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
on_add_reaction(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for reaction added.

### on_call_signal

```python
on_call_signal(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for call signal data.

### on_call_update

```python
on_call_update(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for call updates.

### on_chat_updates

```python
on_chat_updates(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for chat updates with optional filters.

### on_delete_message

```python
on_delete_message(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for deleted messages.

### on_draft_message

```python
on_draft_message(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for draft message updates.

### on_edit_message

```python
on_edit_message(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for edited messages with optional filters.

### on_message

```python
on_message(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for message updates with optional filters.

### on_new_message

```python
on_new_message(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for new messages with optional filters.

### on_remove_notifications

```python
on_remove_notifications(self: 'darkob.Messenger', *args, **kwargs)
```

_No docstring available._

### on_remove_reaction

```python
on_remove_reaction(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for reaction removed.

### on_scheduled_message

```python
on_scheduled_message(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for scheduled message updates.

### on_show_activities

```python
on_show_activities(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for show activities (typing, uploading, recording) with optional filters.

### on_show_notifications

```python
on_show_notifications(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for show notifications with optional filters.

### on_unconfirmed_session

```python
on_unconfirmed_session(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for unconfirmed session updates (anti-login).

### on_voice_chat_participant

```python
on_voice_chat_participant(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for voice chat participant updates.

### on_voice_chat_update

```python
on_voice_chat_update(self: 'darkob.Messenger', *filters: Filter)
```

Decorator for voice chat updates.
