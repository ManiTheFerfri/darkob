# Rubino API reference

The Rubino social platform, using a Messenger session or an auth key.

> Generated from the checkout source by `scripts/generate_docs_assets.py`. Every signature below is real; do not hand-edit this file.

**101 public methods.**

## Method index

- **rubino** (101): [`accept_follow_request`](#accept_follow_request), [`accept_message_owner`](#accept_message_owner), [`accept_profile_admin`](#accept_profile_admin), [`add_impression_ids`](#add_impression_ids), [`add_post`](#add_post), [`add_post_comment`](#add_post_comment), [`add_story`](#add_story), [`add_usage_time`](#add_usage_time), [`block_profile`](#block_profile), [`create_page`](#create_page), [`delete_page`](#delete_page), [`delete_page_avatar`](#delete_page_avatar), [`delete_post`](#delete_post), [`delete_post_comment`](#delete_post_comment), [`delete_story`](#delete_story), [`deny_message_owner`](#deny_message_owner), [`deny_profile_admin`](#deny_profile_admin), [`download_post`](#download_post), [`download_story`](#download_story), [`follow_page`](#follow_page), [`get_blocked_profiles`](#get_blocked_profiles), [`get_boost_url`](#get_boost_url), [`get_events`](#get_events), [`get_explore_post_topics`](#get_explore_post_topics), [`get_explore_posts`](#get_explore_posts), [`get_feed_data`](#get_feed_data), [`get_follow_requests`](#get_follow_requests), [`get_info_by_username`](#get_info_by_username), [`get_me`](#get_me), [`get_metrics_config`](#get_metrics_config), [`get_my_close_friends`](#get_my_close_friends), [`get_my_profile_id`](#get_my_profile_id), [`get_my_profile_settings`](#get_my_profile_settings), [`get_post_by_link`](#get_post_by_link), [`get_post_comment_likes`](#get_post_comment_likes), [`get_post_comments`](#get_post_comments), [`get_post_id`](#get_post_id), [`get_post_likes`](#get_post_likes), [`get_post_link`](#get_post_link), [`get_posts_by_hashtag`](#get_posts_by_hashtag), [`get_posts_by_ids`](#get_posts_by_ids), [`get_profile_admins`](#get_profile_admins), [`get_profile_followers`](#get_profile_followers), [`get_profile_followings`](#get_profile_followings), [`get_profile_id`](#get_profile_id), [`get_profile_info`](#get_profile_info), [`get_profile_posts`](#get_profile_posts), [`get_profile_stories`](#get_profile_stories), [`get_related_posts`](#get_related_posts), [`get_saved_posts`](#get_saved_posts), [`get_setting_admin_permissions`](#get_setting_admin_permissions), [`get_story_viewers`](#get_story_viewers), [`get_suggested_profiles`](#get_suggested_profiles), [`hide_post_comment`](#hide_post_comment), [`like_post`](#like_post), [`like_post_comment`](#like_post_comment), [`not_interested_profile`](#not_interested_profile), [`pin_post_comment`](#pin_post_comment), [`post_collaborator_action`](#post_collaborator_action), [`profile_created_at`](#profile_created_at), [`reject_follow_request`](#reject_follow_request), [`remove_follower`](#remove_follower), [`remove_message_owner`](#remove_message_owner), [`remove_profile_admin`](#remove_profile_admin), [`report_comment`](#report_comment), [`report_hashtag`](#report_hashtag), [`report_live`](#report_live), [`report_post`](#report_post), [`report_profile`](#report_profile), [`report_story`](#report_story), [`request`](#request), [`request_send_file`](#request_send_file), [`save_post`](#save_post), [`search_hashtag`](#search_hashtag), [`search_location`](#search_location), [`search_post`](#search_post), [`search_profile`](#search_profile), [`set_close_friends`](#set_close_friends), [`set_page_avatar`](#set_page_avatar), [`set_post_feedback`](#set_post_feedback), [`set_profile_admin`](#set_profile_admin), [`set_profile_setting`](#set_profile_setting), [`set_profile_status`](#set_profile_status), [`set_profile_type`](#set_profile_type), [`track_client_metrics`](#track_client_metrics), [`unblock_profile`](#unblock_profile), [`unfollow_page`](#unfollow_page), [`unhide_post_comment`](#unhide_post_comment), [`unlike_post`](#unlike_post), [`unlike_post_comment`](#unlike_post_comment), [`unpin_post_comment`](#unpin_post_comment), [`unsave_post`](#unsave_post), [`unset_close_friends`](#unset_close_friends), [`unset_profile_admin`](#unset_profile_admin), [`update_page`](#update_page), [`update_post`](#update_post), [`update_post_share_count`](#update_post_share_count), [`upload_file`](#upload_file), [`view_feed_data`](#view_feed_data), [`view_post`](#view_post), [`view_story`](#view_story)

## rubino

### accept_follow_request

```python
accept_follow_request(self: 'darkob.Rubino', target_profile: str, post_track_id: Optional[str]=None, profile_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Accept a follow request.

Parameters:
    target_profile (str): The profile ID or username that sent the follow request.
    post_track_id (str, optional): The post track ID. Only used in API version 1.
    profile_track_id (str, optional): The profile track ID. Only used in API version 1.
    my_profile (str, optional): The profile that accepts. Defaults to self.profile_id.

Returns:
    The response data.

### accept_message_owner

```python
accept_message_owner(self: 'darkob.Rubino', target_profile: str, my_profile: Optional[str]=None)
```

Accept a message request from a profile.

Parameters:
    target_profile (str): The profile ID or username that sent the message request.
    my_profile (str, optional): The profile that accepts. Defaults to self.profile_id.

Returns:
    The response data.

### accept_profile_admin

```python
accept_profile_admin(self: 'darkob.Rubino', target_profile: str, my_profile: Optional[str]=None)
```

Accept a profile admin invitation.

Parameters:
    target_profile (str): The profile ID or username of the page that sent the admin invitation.
    my_profile (str, optional): The profile that accepts the invitation. Defaults to self.profile_id.

Returns:
    The response data.

### add_impression_ids

```python
add_impression_ids(self: 'darkob.Rubino', impression_data_list: List[Dict], my_profile: Optional[str]=None)
```

Register impressions for posts or profiles to improve content recommendations.

Parameters:
    impression_data_list (List[Dict]): List of impression data objects. Each item must contain 'type' ('Post' or 'Profile'); 'track_id' is optional. For 'Post' type, provide 'post_data_id' as a dict with 'post_id' and 'post_profile_id'. For 'Profile' type, provide 'profile_id'.
    my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

Returns:
    The response data.

Examples:
    # Register a profile impression
    await client.add_impression_ids(
        impression_data_list=[
            {
                "type": "Profile",
                "profile_id": "6a8819ce04fe81a4c8af4455"
            }
        ],
        my_profile="MAXRubikaTest"
    )

    # Register a post impression
    await client.add_impression_ids(
        impression_data_list=[
            {
                "type": "Post",
                "post_data_id": {
                    "post_id": "6ae61abdfc4eff521f9f0448",
                    "post_profile_id": "6a8819ce04fe81a4c8af4455"
                }
            }
        ],
        my_profile="MAXRubikaTest"
    )

### add_post

```python
add_post(self: 'darkob.Rubino', file: str, caption: str='', width: int=1080, height: int=1080, thumbnail_file: Optional[str]=None, video_duration: Optional[int]=None, post_type: Literal['Simple', 'Reels']='Simple', my_profile: Optional[str]=None, location_id: Optional[str]=None, collaborators: Optional[list]=None, hide_comment_count: bool=False, hide_like_count: bool=False, show_only_close_friend: bool=False, hide_share_count: bool=False)
```

Add a new post to a profile.

Parameters:
    file (str): Local path to the main picture or video file.
    caption (str, optional): The post caption. Defaults to empty string.
    width (int, optional): The post width in pixels. Default is 1080. For 'Simple' use square or landscape dimensions; for 'Reels' use vertical (e.g. 1080x1920).
    height (int, optional): The post height in pixels. Default is 1080.
    thumbnail_file (str, optional): Local path to a separate thumbnail/cover image. For pictures, defaults to re-uploading the main file. For videos, if not provided, the cover is extracted from the video using MediaThumbnail.
    video_duration (int, optional): Video duration in seconds. Required for videos when MediaThumbnail is not available (optional libraries missing).
    post_type (Literal['Simple', 'Reels']): The post type. Case-insensitive. Default is 'Simple'.
    my_profile (str, optional): The profile that uploads and owns the post. Defaults to self.profile_id.
    location_id (str, optional): The location ID for the post.
    collaborators (list, optional): List of collaborator profile IDs or usernames.
    hide_comment_count (bool, optional): Hide the comment count on the post. Default is False.
    hide_like_count (bool, optional): Hide the like count on the post. Default is False.
    show_only_close_friend (bool, optional): Show the post only to close friends. Default is False.
    hide_share_count (bool, optional): Hide the share count on the post. Default is False.

Returns:
    The response data.

Raises:
    InvalidInput: If required optional libraries are missing for video processing without `thumbnail_file`/`video_duration`, or if the file is invalid.

Examples:
    # Simple square picture post
    await client.add_post(
        file="photo.jpg",
        caption="Hello world!"
    )

    # Reels video post (cover and duration auto-extracted)
    await client.add_post(
        file="reel.mp4",
        caption="A cool reel",
        post_type="Reels",
        width=1080,
        height=1920
    )

    # Reels video with explicit cover and duration in seconds (no optional libraries needed)
    await client.add_post(
        file="reel.mp4",
        caption="Manual cover",
        post_type="Reels",
        width=1080,
        height=1920,
        thumbnail_file="cover.jpg",
        video_duration=15
    )

### add_post_comment

```python
add_post_comment(self: 'darkob.Rubino', target_profile: str, post: str, text: str, type: Literal['Main', 'Reply']='Main', parent_id: Optional[str]=None, post_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Add a comment to a post.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post (str): The post link or post ID.
    text (str): The comment text.
    type (Literal['Main', 'Reply']): The comment type. Case-insensitive. Default is 'Main'.
    parent_id (str, optional): The parent comment ID (used with 'Reply'). Defaults to None.
    post_track_id (str, optional): The post track ID. Defaults to None.
    my_profile (str, optional): The profile that comments. Defaults to self.profile_id.

Returns:
    The response data.

### add_story

```python
add_story(self: 'darkob.Rubino', file: str, width: int=1080, height: int=1920, thumbnail_file: Optional[str]=None, video_duration: Optional[int]=None, story_type: Optional[Literal['Picture', 'Video']]=None, allow_comment: bool=True, show_only_close_friend: bool=False, reply_status: Optional[Literal['Following', 'All', 'Nobody']]=None, for_close_friend: Optional[list]=None, brand_partnership_profile_ids: Optional[list]=None, widget_story_list: Optional[list]=None, my_profile: Optional[str]=None)
```

Add a new story to a profile.

Parameters:
    file (str): Local path to the main picture or video file.
    width (int, optional): The story width in pixels. Default is 1080.
    height (int, optional): The story height in pixels. Default is 1920.
    thumbnail_file (str, optional): Local path to a separate thumbnail/cover image. For pictures, defaults to re-uploading the main file. For videos, if not provided, the cover is extracted from the video using MediaThumbnail.
    video_duration (int, optional): Video duration in MILLISECONDS. Required for videos when MediaThumbnail is not available.
    story_type (Literal['Picture', 'Video'], optional): The story type. Auto-detected from the file extension if not provided.
    allow_comment (bool, optional): Allow comments on the story. Default is True.
    show_only_close_friend (bool, optional): Show the story only to close friends. Default is False.
    reply_status (Literal['Following', 'All', 'Nobody'], optional): Who can reply to the story. Case-insensitive. Defaults to 'All'.
    for_close_friend (list, optional): List of profile IDs allowed to view the story as close friends.
    brand_partnership_profile_ids (list, optional): List of brand partnership profile IDs.
    widget_story_list (list, optional): List of widget dictionaries (poll, hashtag, mention, emoji_slider, post_to_story, story_link, quiz, count_down, question, story_to_story, add_yours). Each widget must contain 'type' and 'position'.
    my_profile (str, optional): The profile that uploads and owns the story. Defaults to self.profile_id.

Returns:
    The response data.

Raises:
    InvalidInput: If required optional libraries are missing for video processing without `thumbnail_file`/`video_duration`, or if the file is invalid.

Examples:
    # Simple picture story
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest"
    )

    # Video story with explicit cover and duration (milliseconds)
    await client.add_story(
        file="video.mp4",
        thumbnail_file="cover.jpg",
        video_duration=10000,
        my_profile="MAXRubikaTest"
    )

    # Story with custom settings
    await client.add_story(
        file="photo.jpg",
        allow_comment=False,
        show_only_close_friend=True,
        reply_status="Following",
        my_profile="MAXRubikaTest"
    )

    # Story with a Poll widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "Poll",
            "position": {
                "point_position": {"x": 0.5, "y": 0.5},
                "width": 0.6,
                "height": 0.2,
                "rotation": 0.0
            },
            "poll": {
                "content": "Which one?",
                "choices_list": ["Yes", "No"]
            }
        }]
    )

    # Story with a Hashtag widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "Hashtag",
            "position": {
                "point_position": {"x": 0.3, "y": 0.7},
                "width": 0.4,
                "height": 0.1,
                "rotation": 0.0
            },
            "hashtag": {"hashtag": "rubika"}
        }]
    )

    # Story with a Mention widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "Mention",
            "position": {
                "point_position": {"x": 0.5, "y": 0.6},
                "width": 0.4,
                "height": 0.1,
                "rotation": 0.0
            },
            "mention": {"profile_id": "u0abc123def"}
        }]
    )

    # Story with a StoryLink widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "StoryLink",
            "position": {
                "point_position": {"x": 0.5, "y": 0.8},
                "width": 0.6,
                "height": 0.1,
                "rotation": 0.0
            },
            "story_link": {
                "link": "https://rubika.ir",
                "text": "Rubika website"
            }
        }]
    )

    # Story with a Quiz widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "Quiz",
            "position": {
                "point_position": {"x": 0.5, "y": 0.3},
                "width": 0.7,
                "height": 0.3,
                "rotation": 0.0
            },
            "quiz": {
                "content": "Capital of Iran?",
                "choices_list": ["Tehran", "Isfahan", "Shiraz"],
                "correct_index": 0
            }
        }]
    )

    # Story with a CountDown widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "CountDown",
            "position": {
                "point_position": {"x": 0.5, "y": 0.5},
                "width": 0.6,
                "height": 0.2,
                "rotation": 0.0
            },
            "count_down": {
                "content": "My birthday!",
                "timestamp": 1794034607,
                "is_remind_on": True
            }
        }]
    )

    # Story with a Question widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "Question",
            "position": {
                "point_position": {"x": 0.5, "y": 0.5},
                "width": 0.6,
                "height": 0.2,
                "rotation": 0.0
            },
            "question": {"content": "Any questions?"}
        }]
    )

    # Story with an EmojiSlider widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "EmojiSlider",
            "position": {
                "point_position": {"x": 0.5, "y": 0.5},
                "width": 0.6,
                "height": 0.2,
                "rotation": 0.0
            },
            "emoji_slider": {
                "content": "How beautiful is this?",
                "emoji_char": "❤️",
                "theme": {
                    "background_color": {"red": 255, "green": 255, "blue": 255, "alpha": 255},
                    "text_color": {"red": 0, "green": 0, "blue": 0, "alpha": 255},
                    "seekbar_background_color": {"red": 200, "green": 200, "blue": 200, "alpha": 255},
                    "seekbar_progress_color": {"red": 255, "green": 0, "blue": 0, "alpha": 255},
                    "seekbar_type": "Simple"
                }
            }
        }]
    )

    # Story with a PostToStory widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "PostToStory",
            "position": {
                "point_position": {"x": 0.5, "y": 0.5},
                "width": 0.6,
                "height": 0.6,
                "rotation": 0.0
            },
            "post_to_story": {
                "post_id": "6aee1d58ca7c95c82981e983",
                "post_creator_id": "67f65de73b77504d03749be2",
                "post_profile_id": "67f65de73b77504d03749be2"
            }
        }]
    )

    # Story with a StoryToStory widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "StoryToStory",
            "position": {
                "point_position": {"x": 0.5, "y": 0.5},
                "width": 0.6,
                "height": 0.6,
                "rotation": 0.0
            },
            "story_to_story": {
                "story_id": "6aeecbaff1089881816c7142",
                "story_creator_id": "6a807217b59333f89d394d36",
                "story_profile_id": "6a807217b59333f89d394d36"
            }
        }]
    )

    # Story with an AddYours widget
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[{
            "type": "AddYours",
            "position": {
                "point_position": {"x": 0.5, "y": 0.5},
                "width": 0.6,
                "height": 0.3,
                "rotation": 0.0
            },
            "add_yours": {
                "content": "Send your photo!",
                "main_story_data": {
                    "story_id": "6aeecbaff1089881816c7142",
                    "story_profile_id": "6a807217b59333f89d394d36"
                }
            }
        }]
    )

    # Story with multiple widgets
    await client.add_story(
        file="photo.jpg",
        my_profile="MAXRubikaTest",
        widget_story_list=[
            {
                "type": "Poll",
                "position": {
                    "point_position": {"x": 0.5, "y": 0.3},
                    "width": 0.6,
                    "height": 0.2,
                    "rotation": 0.0
                },
                "poll": {
                    "content": "Do you agree?",
                    "choices_list": ["Yes", "No"]
                }
            },
            {
                "type": "Hashtag",
                "position": {
                    "point_position": {"x": 0.5, "y": 0.7},
                    "width": 0.4,
                    "height": 0.1,
                    "rotation": 0.0
                },
                "hashtag": {"hashtag": "darkob"}
            }
        ]
    )

### add_usage_time

```python
add_usage_time(self: 'darkob.Rubino', usage_time_list: List[Dict[str, Any]], my_profile: Optional[str]=None)
```

Register usage time analytics.

Parameters:
    usage_time_list (List[Dict[str, Any]]): List of usage time entries. Each entry must contain 'page' (exactly one of 'Feed', 'Profile', 'Story', 'Live', 'Explore', 'Search' — case-sensitive) and 'duration' (any value). Optional 'extra_data' may contain 'post_data_id' (dict with 'post_id' and 'post_profile_id'), 'profile_id' (str), and 'live_id' (str).
    my_profile (str, optional): The profile that reports usage. Defaults to self.profile_id.

Returns:
    The response data.

Examples:
    # Single page usage
    await client.add_usage_time(
        usage_time_list=[
            {"page": "Feed", "duration": 3000}
        ],
        my_profile="MAXRubikaTest"
    )

    # Feed with post data
    await client.add_usage_time(
        usage_time_list=[
            {
                "page": "Feed",
                "duration": 3000,
                "extra_data": {
                    "post_data_id": {
                        "post_id": "6aee295d805bf66cedd0c202",
                        "post_profile_id": "6a807217b59333f89d394d36"
                    }
                }
            }
        ],
        my_profile="MAXRubikaTest"
    )

    # Profile view
    await client.add_usage_time(
        usage_time_list=[
            {
                "page": "Profile",
                "duration": 10000,
                "extra_data": {"profile_id": "6a807217b59333f89d394d36"}
            }
        ],
        my_profile="MAXRubikaTest"
    )

    # Live view
    await client.add_usage_time(
        usage_time_list=[
            {
                "page": "Live",
                "duration": 20000,
                "extra_data": {"live_id": "live_123"}
            }
        ],
        my_profile="MAXRubikaTest"
    )

    # Multiple entries
    await client.add_usage_time(
        usage_time_list=[
            {"page": "Feed", "duration": 3000},
            {"page": "Explore", "duration": 8000},
            {"page": "Search", "duration": 4000}
        ],
        my_profile="MAXRubikaTest"
    )

### block_profile

```python
block_profile(self: 'darkob.Rubino', target_profile: str, post_track_id: Optional[str]=None, profile_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Block a profile.

Parameters:
    target_profile (str): The profile ID or username to block.
    post_track_id (str, optional): The post track ID. Only used in API version 1.
    profile_track_id (str, optional): The profile track ID. Only used in API version 1.
    my_profile (str, optional): The profile that blocks. Defaults to self.profile_id.

Returns:
    The response data.

### create_page

```python
create_page(self: 'darkob.Rubino', name: str, username: str, profile_status: Literal['Public', 'Private']='Public', profile_type: Optional[Literal['Business', 'Personal', 'Creator']]=None, bio: Optional[str]=None, email: Optional[str]=None, phone: Optional[str]=None, website: Optional[str]=None, avatar_file: Optional[str]=None, avatar_thumbnail: Optional[str]=None)
```

Create a new page (profile).

Parameters:
    name (str): The display name of the page.
    username (str): The username for the page.
    profile_status (Literal['Public', 'Private']): The page visibility. Case-insensitive. Default is 'Public'.
    profile_type (Literal['Business', 'Personal', 'Creator'], optional): The page type. Case-insensitive.
    bio (str, optional): The page bio.
    email (str, optional): The email contact.
    phone (str, optional): The phone contact.
    website (str, optional): The website contact.
    avatar_file (str, optional): Local path to the avatar main image. If 'avatar_thumbnail' is not provided, the main file is uploaded again as the thumbnail.
    avatar_thumbnail (str, optional): Local path to the avatar thumbnail image.

Returns:
    The response data.

Examples:
    # Minimal page
    await client.create_page(
        name="My Page",
        username="mypage"
    )

    # Private business page with bio
    await client.create_page(
        name="My Business",
        username="mybusiness",
        profile_status="Private",
        profile_type="Business",
        bio="We sell stuff"
    )

    # Page with contacts
    await client.create_page(
        name="My Store",
        username="mystore",
        profile_type="Business",
        email="info@example.com",
        phone="+989123456789",
        website="https://example.com"
    )

    # Page with avatar (thumbnail auto-uploaded from main if omitted)
    await client.create_page(
        name="My Page",
        username="mypage",
        avatar_file="avatar.jpg"
    )

    # Page with explicit avatar thumbnail
    await client.create_page(
        name="My Page",
        username="mypage",
        avatar_file="avatar.jpg",
        avatar_thumbnail="avatar_thumb.jpg"
    )

### delete_page

```python
delete_page(self: 'darkob.Rubino', target_profile: str, my_profile: Optional[str]=None)
```

Delete a page (profile).

Parameters:
    target_profile (str): The profile ID or username of the page to delete.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### delete_page_avatar

```python
delete_page_avatar(self: 'darkob.Rubino', my_profile: Optional[str]=None)
```

Delete the avatar of a page (profile).

Parameters:
    my_profile (str, optional): The profile whose avatar is deleted. Defaults to self.profile_id.

Returns:
    The response data.

### delete_post

```python
delete_post(self: 'darkob.Rubino', target_profile: Optional[str]=None, post: Optional[str]=None, post_ids: Optional[List[Dict]]=None, my_profile: Optional[str]=None)
```

Delete one or more posts.

Parameters:
    target_profile (str, optional): The profile ID or username that owns the post. Use together with 'post'.
    post (str, optional): The post link or post ID. Use together with 'target_profile'.
    post_ids (List[Dict], optional): List of post identifiers for batch delete. Each item must contain 'post' (link or ID) and 'target_profile' (profile ID or username). Cannot be used together with 'post' or 'target_profile'.
    my_profile (str, optional): The profile that deletes. Defaults to self.profile_id.

Returns:
    The response data.

### delete_post_comment

```python
delete_post_comment(self: 'darkob.Rubino', post: str, comment_id: str, post_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Delete a comment on a post.

Parameters:
    post (str): The post link or post ID.
    comment_id (str): The ID of the comment.
    post_track_id (str, optional): The post track ID. Defaults to None.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### delete_story

```python
delete_story(self: 'darkob.Rubino', story_id: str, my_profile: Optional[str]=None)
```

Delete a story.

Parameters:
    story_id (str): The ID of the story to delete.
    my_profile (str, optional): The profile that deletes. Defaults to self.profile_id.

Returns:
    The response data.

### deny_message_owner

```python
deny_message_owner(self: 'darkob.Rubino', target_profile: str, my_profile: Optional[str]=None)
```

Deny a message request from a profile.

Parameters:
    target_profile (str): The profile ID or username that sent the message request.
    my_profile (str, optional): The profile that denies. Defaults to self.profile_id.

Returns:
    The response data.

### deny_profile_admin

```python
deny_profile_admin(self: 'darkob.Rubino', target_profile: str, my_profile: Optional[str]=None)
```

Deny a profile admin invitation.

Parameters:
    target_profile (str): The profile ID or username of the page that sent the admin invitation.
    my_profile (str, optional): The profile that denies the invitation. Defaults to self.profile_id.

Returns:
    The response data.

### download_post

```python
download_post(self: 'darkob.Rubino', post: str, target_profile: Optional[str]=None, save_as: bool=True, file_name: Optional[str]=None, my_profile: Optional[str]=None)
```

Download all media files of a post.

Parameters:
    post (str): The post link or post ID.
    target_profile (str, optional): The profile ID or username that owns the post. Required when 'post' is a post ID.
    save_as (bool, optional): If True, save files to disk; if False, return raw bytes. Default is True.
    file_name (str, optional): Base name for saved files (without extension). If not provided, the current date and time are used.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    Contains 'files' (list of saved paths if save_as=True, otherwise list of dicts with 'file_name' and 'content').

### download_story

```python
download_story(self: 'darkob.Rubino', target_profile: str, save_as: bool=True, file_name: Optional[str]=None, my_profile: Optional[str]=None)
```

Download all stories of a profile.

Parameters:
    target_profile (str): The profile ID or username that owns the stories.
    save_as (bool, optional): If True, save files to disk; if False, return raw bytes. Default is True.
    file_name (str, optional): Base name for saved files (without extension). If not provided, the current date and time are used.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    Data: Contains 'files' (list of saved paths if save_as=True, otherwise list of dicts with 'file_name' and 'content').

### follow_page

```python
follow_page(self: 'darkob.Rubino', target_profile: str, post_track_id: Optional[str]=None, profile_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Follow a page (profile).

Parameters:
    target_profile (str): The profile ID or username to follow.
    post_track_id (str, optional): The post track ID. Only used in API version 1.
    profile_track_id (str, optional): The profile track ID. Only used in API version 1.
    my_profile (str, optional): The profile that follows. Defaults to self.profile_id.

Returns:
    The response data.

### get_blocked_profiles

```python
get_blocked_profiles(self: 'darkob.Rubino', start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get the list of blocked profiles.

Parameters:
    start_id (str, optional): The starting profile ID for pagination. Defaults to None.
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data.

### get_boost_url

```python
get_boost_url(self: 'darkob.Rubino', target_profile: str, post_id: str, my_profile: Optional[str]=None)
```

Get the boost URL for a post.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post_id (str): The ID of the post to boost.
    my_profile (str, optional): The profile that performs the boost. Defaults to self.profile_id.

Returns:
    The response data.

### get_events

```python
get_events(self: 'darkob.Rubino', filter: Optional[Literal['FollowRequest', 'PostConfirm', 'ProfileConfirm']]=None, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get profile events.

Parameters:
    filter (Literal['FollowRequest', 'PostConfirm', 'ProfileConfirm'], optional): The event filter. Case-insensitive. Defaults to None (all events).
    start_id (str, optional): The starting event ID for pagination. Defaults to None.
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data.

### get_explore_post_topics

```python
get_explore_post_topics(self: 'darkob.Rubino', my_profile: Optional[str]=None)
```

Get explore post topics.

Parameters:
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The topics data.

### get_explore_posts

```python
get_explore_posts(self: 'darkob.Rubino', topic_id: Optional[str]=None, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get posts from the Explore feed.

Parameters:
    topic_id (str, optional): The topic ID to filter posts by. Defaults to None (all topics).
    start_id (str, optional): The starting post ID for pagination. Defaults to None.
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data.

### get_feed_data

```python
get_feed_data(self: 'darkob.Rubino', limit: Optional[int]=None, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get feed posts.

Parameters:
    limit (int, optional): The maximum number of posts to return. Defaults to None (server default).
    start_id (str, optional): The starting post ID for pagination. Defaults to None.
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data.

### get_follow_requests

```python
get_follow_requests(self: 'darkob.Rubino', start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get pending follow requests.

Parameters:
    start_id (str, optional): The starting event ID for pagination. Defaults to None.
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data.

### get_info_by_username

```python
get_info_by_username(self: 'darkob.Rubino', username: str)
```

Get a page (user or channel) by its username.

Parameters:
    username (str): The username to check.

Returns:
    The result of the API call.

### get_me

```python
get_me(self: 'darkob.Rubino', my_profile: Optional[str]=None)
```

Get profile information.

Parameters:
    my_profile (str, optional): The profile ID or username.
        Defaults to self.profile_id.

Returns:
    The profile data.

### get_metrics_config

```python
get_metrics_config(self: 'darkob.Rubino', my_profile: Optional[str]=None)
```

Get the metrics/tracking configuration.

Parameters:
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data containing 'enable_tracking' and 'chances' (with 'loading_file_chance' and 'uploading_file_chance').

### get_my_close_friends

```python
get_my_close_friends(self: 'darkob.Rubino', search_text: Optional[str]=None, limit: Optional[int]=None, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get the list of close friends.

Parameters:
    search_text (str, optional): Search text for filtering close friends. Defaults to None.
    limit (int, optional): The maximum number of close friends to return. Defaults to None (server default).
    start_id (str, optional): The starting profile ID for pagination. Defaults to None.
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data.

### get_my_profile_id

```python
get_my_profile_id(self: 'darkob.Rubino')
```

Get the current user's profile ID.

Returns:
    str: The user's profile ID.

### get_my_profile_settings

```python
get_my_profile_settings(self: 'darkob.Rubino', my_profile: Optional[str]=None)
```

Get the settings of a profile.

Parameters:
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data.

### get_post_by_link

```python
get_post_by_link(self: 'darkob.Rubino', link: str, my_profile: Optional[str]=None)
```

Get a post by its link.

Parameters:
    link (str): The link of the post.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The post data.

### get_post_comment_likes

```python
get_post_comment_likes(self: 'darkob.Rubino', post: str, comment_id: str, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get the list of users who liked a post comment.

Parameters:
    post (str): The post link or post ID.
    comment_id (str): The ID of the comment.
    start_id (str, optional): The starting user ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### get_post_comments

```python
get_post_comments(self: 'darkob.Rubino', target_profile: str, post: str, type: Literal['Main', 'Reply']='Main', parent_id: Optional[str]=None, start_id: Optional[str]=None, comment_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get comments of a post.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post (str): The post link or post ID.
    type (Literal['Main', 'Reply']): The comment type. Case-insensitive. Default is 'Main'.
    parent_id (str, optional): The parent comment ID (used with 'Reply'). Defaults to None.
    start_id (str, optional): The starting comment ID for pagination. Defaults to None.
    comment_id (str, optional): A specific comment ID (used with 'Reply'). Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### get_post_id

```python
get_post_id(self: 'darkob.Rubino', post: str, my_profile: Optional[str]=None)
```

Get post ID from a share link or post ID.

Parameters:
    post (str): The share link or post ID.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The post ID string.

### get_post_likes

```python
get_post_likes(self: 'darkob.Rubino', target_profile: str, post_id: str, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get the list of users who liked a post.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post_id (str): The ID of the post.
    start_id (str, optional): The starting user ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### get_post_link

```python
get_post_link(self: 'darkob.Rubino', target_profile: str, post_id: str, my_profile: Optional[str]=None)
```

Get the share link of a post.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post_id (str): The ID of the post.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### get_posts_by_hashtag

```python
get_posts_by_hashtag(self: 'darkob.Rubino', hashtag: str, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get posts by hashtag.

Parameters:
    hashtag (str): The hashtag name.
    start_id (str, optional): The starting post ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### get_posts_by_ids

```python
get_posts_by_ids(self: 'darkob.Rubino', target_profile: Optional[str]=None, post: Optional[str]=None, post_ids: Optional[List[Dict]]=None, my_profile: Optional[str]=None)
```

Get one or more posts by their IDs.

Parameters:
    target_profile (str, optional): The profile ID or username that owns the post. Use together with 'post'.
    post (str, optional): The post link or post ID. Use together with 'target_profile'.
    post_ids (List[Dict], optional): List of post identifiers for batch retrieval. Each item must contain 'post' (link or ID) and 'target_profile' (profile ID or username). Cannot be used together with 'post' or 'target_profile'.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

Examples:
    # Get a single post by ID
    await client.get_posts_by_ids(
        target_profile="Online_User",
        post="6ae61abdfc4eff521f9f0448"
    )

    # Get multiple posts
    await client.get_posts_by_ids(
        post_ids=[
            {"post": "6ae61abdfc4eff521f9f0448", "target_profile": "Online_User"},
            {"post": "6aee295d805bf66cedd0c202", "target_profile": "MAXRubikaTest"}
        ]
    )

### get_profile_admins

```python
get_profile_admins(self: 'darkob.Rubino', my_profile: Optional[str]=None)
```

Get the list of admins of a profile (page).

Parameters:
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data.

### get_profile_followers

```python
get_profile_followers(self: 'darkob.Rubino', target_profile: str, search_text: Optional[str]=None, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get the followers list of a profile.

Parameters:
    target_profile (str): The profile ID or username to query.
    search_text (str, optional): Search text for filtering. Defaults to None.
    start_id (str, optional): The starting user ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### get_profile_followings

```python
get_profile_followings(self: 'darkob.Rubino', target_profile: str, search_text: Optional[str]=None, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get the following list of a profile.

Parameters:
    target_profile (str): The profile ID or username to query.
    search_text (str, optional): Search text for filtering. Defaults to None.
    start_id (str, optional): The starting user ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### get_profile_id

```python
get_profile_id(self: 'darkob.Rubino', username: str)
```

Get profile ID by username or profile ID.

Parameters:
    username (str): The username, profile ID, or 'me'.

Returns:
    The profile ID string.

### get_profile_info

```python
get_profile_info(self: 'darkob.Rubino', target_profile: str, my_profile: Optional[str]=None)
```

Get detailed profile information.

Parameters:
    target_profile (str): The profile ID or username.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The profile information data.

### get_profile_posts

```python
get_profile_posts(self: 'darkob.Rubino', target_profile: str, post_type: Literal['IGTV', 'Reels', 'Tagged', 'All']='All', limit: Optional[int]=None, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get the posts of a profile.

Parameters:
    target_profile (str): The profile ID or username to query.
    post_type (Literal['IGTV', 'Reels', 'Tagged', 'All']): The post type filter. Case-insensitive. Default is 'All'.
    limit (int, optional): The maximum number of posts to return. Defaults to None (server default).
    start_id (str, optional): The starting post ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### get_profile_stories

```python
get_profile_stories(self: 'darkob.Rubino', target_profile: str, story_ids: Optional[Union[str, List[str]]]=None, my_profile: Optional[str]=None)
```

Get stories of a profile.

Parameters:
    target_profile (str): The profile ID or username that owns the stories.
    story_ids (Union[str, List[str]], optional): A single story ID or a list of story IDs to fetch specific stories. If not provided, all stories are returned. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The stories data.

### get_related_posts

```python
get_related_posts(self: 'darkob.Rubino', location: Literal['Explore', 'SuggestedPost', 'ShowPost'], post_id: Optional[str]=None, target_profile: Optional[str]=None, track_id: Optional[str]=None, limit: Optional[int]=None, start_id: Optional[str]=None, post_position: Optional[dict]=None, my_profile: Optional[str]=None)
```

Get posts related to a given post.

Parameters:
    location (Literal['Explore', 'SuggestedPost', 'ShowPost']): The context where related posts are shown. Case-insensitive.
    post_id (str, optional): The ID of the reference post. Defaults to None.
    target_profile (str, optional): The profile ID or username that owns the post. Defaults to None.
    track_id (str, optional): A tracking ID. Defaults to None.
    limit (int, optional): The maximum number of posts to return. Defaults to None (server default).
    start_id (str, optional): The starting post ID for pagination. Defaults to None.
    post_position (dict, optional): The position of the post in the grid, with 'row' (int) and 'column' (int). Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

Examples:
    # Explore related posts
    await client.get_related_posts(
        location="Explore",
        limit=10,
        my_profile="MAXRubikaTest"
    )

    # Suggested posts after viewing a post
    await client.get_related_posts(
        location="SuggestedPost",
        post_id="6ae61abdfc4eff521f9f0448",
        target_profile="Online_User",
        limit=10,
        my_profile="MAXRubikaTest"
    )

    # Related posts shown on a post page
    await client.get_related_posts(
        location="ShowPost",
        post_id="6ae61abdfc4eff521f9f0448",
        target_profile="Online_User",
        track_id='{"l": "SharePost"}',
        my_profile="MAXRubikaTest"
    )

    # With post position in the grid
    await client.get_related_posts(
        location="Explore",
        post_id="6ae61abdfc4eff521f9f0448",
        target_profile="Online_User",
        post_position={"row": 1, "column": 2},
        my_profile="MAXRubikaTest"
    )

### get_saved_posts

```python
get_saved_posts(self: 'darkob.Rubino', start_id: Optional[str]=None, bookmark_collection_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get the list of bookmarked (saved) posts.

Parameters:
    start_id (str, optional): The starting post ID for pagination. Defaults to None.
    bookmark_collection_id (str, optional): The bookmark collection ID to filter by. Defaults to None.
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data.

### get_setting_admin_permissions

```python
get_setting_admin_permissions(self: 'darkob.Rubino', my_profile: Optional[str]=None)
```

Get the admin permission settings of a profile.

Parameters:
    my_profile (str, optional): The profile to query. Defaults to self.profile_id.

Returns:
    The response data.

### get_story_viewers

```python
get_story_viewers(self: 'darkob.Rubino', story_id: str, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get the viewers of a story.

Parameters:
    story_id (str): The ID of the story.
    start_id (str, optional): The starting viewer ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### get_suggested_profiles

```python
get_suggested_profiles(self: 'darkob.Rubino', target_profile: str, usage: str='Similar', start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Get suggested profiles.

Parameters:
    target_profile (str): The reference profile ID or username for similarity.
    usage (str, optional): The suggestion usage type. Default is 'Similar'.
    start_id (str, optional): The starting profile ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### hide_post_comment

```python
hide_post_comment(self: 'darkob.Rubino', post: str, comment_id: str, post_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Hide a comment on a post.

Parameters:
    post (str): The post link or post ID.
    comment_id (str): The ID of the comment.
    post_track_id (str, optional): The post track ID. Defaults to None.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### like_post

```python
like_post(self: 'darkob.Rubino', target_profile: Optional[str]=None, post: Optional[str]=None, post_ids: Optional[List[Dict]]=None, my_profile: Optional[str]=None)
```

Like one or more posts.

Parameters:
    target_profile (str, optional): The profile ID or username that owns the post. Use together with 'post'.
    post (str, optional): The post link or post ID. Use together with 'target_profile'.
    post_ids (List[Dict], optional): List of post identifiers for batch like. Each item must contain 'post' (link or ID) and 'target_profile' (profile ID or username). Cannot be used together with 'post' or 'target_profile'.
    my_profile (str, optional): The profile that likes. Defaults to self.profile_id.

Returns:
    The response data.

### like_post_comment

```python
like_post_comment(self: 'darkob.Rubino', post: str, comment_id: str, post_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Like a comment on a post.

Parameters:
    post (str): The post link or post ID.
    comment_id (str): The ID of the comment.
    post_track_id (str, optional): The post track ID. Defaults to None.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### not_interested_profile

```python
not_interested_profile(self: 'darkob.Rubino', target_profile: str, track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Mark a profile as "not interested".

Parameters:
    target_profile (str): The profile ID or username to mark as not interested.
    track_id (str, optional): A tracking ID. Defaults to None.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### pin_post_comment

```python
pin_post_comment(self: 'darkob.Rubino', post: str, comment_id: str, post_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Pin a comment on a post.

Parameters:
    post (str): The post link or post ID.
    comment_id (str): The ID of the comment.
    post_track_id (str, optional): The post track ID. Defaults to None.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### post_collaborator_action

```python
post_collaborator_action(self: 'darkob.Rubino', target_profile: str, post: str, action_type: Literal['Accept', 'Deny', 'Remove'], my_profile: Optional[str]=None)
```

Accept, deny, or remove a collaborator from a post.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post (str): The post link or post ID.
    action_type (Literal['Accept', 'Deny', 'Remove']): The collaboration action. Case-insensitive.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### profile_created_at

```python
profile_created_at(self: 'darkob.Rubino', target_profile: str)
```

Get the creation date of a profile.

Parameters:
    target_profile (str): The profile ID or username.

Returns:
    Creation date with details.

### reject_follow_request

```python
reject_follow_request(self: 'darkob.Rubino', target_profile: str, post_track_id: Optional[str]=None, profile_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Reject a follow request.

Parameters:
    target_profile (str): The profile ID or username that sent the follow request.
    post_track_id (str, optional): The post track ID. Only used in API version 1.
    profile_track_id (str, optional): The profile track ID. Only used in API version 1.
    my_profile (str, optional): The profile that rejects. Defaults to self.profile_id.

Returns:
    The response data.

### remove_follower

```python
remove_follower(self: 'darkob.Rubino', target_profile: str, post_track_id: Optional[str]=None, profile_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Remove a follower from a profile.

Parameters:
    target_profile (str): The profile ID or username of the follower to remove.
    post_track_id (str, optional): The post track ID. Defaults to None.
    profile_track_id (str, optional): The profile track ID. Defaults to None.
    my_profile (str, optional): The profile that removes the follower. Defaults to self.profile_id.

Returns:
    The response data.

### remove_message_owner

```python
remove_message_owner(self: 'darkob.Rubino', target_profile: str, my_profile: Optional[str]=None)
```

Remove message access for a profile.

Parameters:
    target_profile (str): The profile ID or username whose message access will be removed.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### remove_profile_admin

```python
remove_profile_admin(self: 'darkob.Rubino', target_profile: str, my_profile: Optional[str]=None)
```

Remove an admin from a profile.

Parameters:
    target_profile (str): The profile ID or username of the admin to remove.
    my_profile (str, optional): The profile that removes the admin. Defaults to self.profile_id.

Returns:
    The response data.

### report_comment

```python
report_comment(self: 'darkob.Rubino', target_profile: str, post: str, comment_id: str, reason: int=2, my_profile: Optional[str]=None)
```

Report a comment.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post (str): The post link or post ID that contains the comment.
    comment_id (str): The ID of the comment.
    reason (int): Report reason code. Defaults to 2.
    my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

Returns:
    The response data.

### report_hashtag

```python
report_hashtag(self: 'darkob.Rubino', target_profile: str, reason: int=2, my_profile: Optional[str]=None)
```

Report a hashtag.

Parameters:
    target_profile (str): The profile ID or username of the hashtag.
    reason (int): Report reason code. Defaults to 2.
    my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

Returns:
    The response data.

### report_live

```python
report_live(self: 'darkob.Rubino', target_profile: str, live_id: str, reason: int=2, my_profile: Optional[str]=None)
```

Report a live stream.

Parameters:
    target_profile (str): The profile ID or username that owns the live.
    live_id (str): The ID of the live stream to report.
    reason (int): Report reason code. Defaults to 2.
    my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

Returns:
    The response data.

### report_post

```python
report_post(self: 'darkob.Rubino', target_profile: str, post: str, reason: int=2, my_profile: Optional[str]=None)
```

Report a post.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post (str): The post link or post ID.
    reason (int): Report reason code. Defaults to 2.
    my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

Returns:
    The response data.

### report_profile

```python
report_profile(self: 'darkob.Rubino', target_profile: str, reason: int=2, my_profile: Optional[str]=None)
```

Report a profile.

Parameters:
    target_profile (str): The profile ID or username to report.
    reason (int): Report reason code. Defaults to 2.
    my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

Returns:
    The response data.

### report_story

```python
report_story(self: 'darkob.Rubino', target_profile: str, story_id: str, reason: int=2, my_profile: Optional[str]=None)
```

Report a story.

Parameters:
    target_profile (str): The profile ID or username that owns the story.
    story_id (str): The ID of the story.
    reason (int): Report reason code. Defaults to 2.
    my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

Returns:
    The response data.

### request

```python
request(self: 'darkob.Rubino', method: str, input: Optional[dict]=None)
```

Send a request to the Rubino API.

Parameters:
    method (str): The API method name to call.
    input (dict, optional): The input data to send with the request.
        In api_version=1, 'profile_id' in input is used internally
        and NOT sent to the API inside input.

Returns:
    The parsed response data on success.

### request_send_file

```python
request_send_file(self: 'darkob.Rubino', file_name: str, file_size: int, file_type: Literal['Picture', 'Video']='Picture', mime: Optional[str]=None, my_profile: Optional[str]=None)
```

Request an upload session from Rubino servers.

Parameters:
    file_name (str): The name of the file to be uploaded.
    file_size (int): Total file size in bytes.
    file_type (Literal["Picture", "Video"]): Either 'Picture' or 'Video'. Case-insensitive. Accepts 'Picture', 'Image', 'Photo' for Picture and 'Video', 'Clip' for Video. Defaults to 'Picture'.
    mime (str, optional): MIME type of the file. Defaults based on file_type ('jpg' for Picture, 'mp4' for Video). Only used in api_version=1.
    my_profile (str, optional): The profile that uploads. Defaults to self.profile_id.

Returns:
    A dict containing upload endpoint, file ID, and access hash.

Raises:
    InvalidInput: If file_type is invalid.

### save_post

```python
save_post(self: 'darkob.Rubino', target_profile: Optional[str]=None, post: Optional[str]=None, post_ids: Optional[List[Dict]]=None, bookmark_collection_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Bookmark (save) one or more posts.

Parameters:
    target_profile (str, optional): The profile ID or username that owns the post. Use together with 'post'.
    post (str, optional): The post link or post ID. Use together with 'target_profile'.
    post_ids (List[Dict], optional): List of post identifiers for batch save. Each item must contain 'post' (link or ID) and 'target_profile' (profile ID or username). Cannot be used together with 'post' or 'target_profile'.
    bookmark_collection_id (str, optional): The bookmark collection ID. Defaults to None.
    my_profile (str, optional): The profile that bookmarks. Defaults to self.profile_id.

Returns:
    The response data.

### search_hashtag

```python
search_hashtag(self: 'darkob.Rubino', search_text: str, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Search for hashtags.

Parameters:
    search_text (str): The search text (hashtag name without '#').
    start_id (str, optional): The starting hashtag ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### search_location

```python
search_location(self: 'darkob.Rubino', usage: Literal['Search', 'AddPost']='Search', search_text: Optional[str]=None, latitude: Optional[float]=None, longitude: Optional[float]=None, start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Search for locations.

Parameters:
    usage (Literal['Search', 'AddPost']): The search usage context. Case-sensitive.
    search_text (str, optional): The search text for the location. Required when 'usage' is 'Search'. Defaults to None.
    latitude (float, optional): The latitude for location bias. Required when 'usage' is 'AddPost'. Defaults to None.
    longitude (float, optional): The longitude for location bias. Required when 'usage' is 'AddPost'. Defaults to None.
    start_id (str, optional): The starting location ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### search_post

```python
search_post(self: 'darkob.Rubino', search_text: Optional[str]=None, search_key: Optional[str]=None, usage: Literal['Search', 'Hashtag', 'Reels', 'Location']='Search', start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Search for posts.

Parameters:
    search_text (str, optional): The search text. Required for 'Search', 'Hashtag', and 'Reels'. Defaults to None.
    search_key (str, optional): The location ID. Required for 'Location'. Defaults to None.
    usage (Literal['Search', 'Hashtag', 'Reels', 'Location']): The search usage context. Case-insensitive. Default is 'Search'.
    start_id (str, optional): The starting post ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### search_profile

```python
search_profile(self: 'darkob.Rubino', search_text: str, usage: Literal['Search', 'AddCloseFriend', 'AddTag', 'AddCollaborator', 'AddMention', 'AddBrandPartner', 'AddAdmin', 'MessageReceiver']='Search', start_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Search for profiles.

Parameters:
    search_text (str): The search text (username or name).
    usage (Literal['Search', 'AddCloseFriend', 'AddTag', 'AddCollaborator', 'AddMention', 'AddBrandPartner', 'AddAdmin', 'MessageReceiver']): The search usage context. Case-insensitive. Default is 'Search'.
    start_id (str, optional): The starting profile ID for pagination. Defaults to None.
    my_profile (str, optional): The profile that requests. Defaults to self.profile_id.

Returns:
    The response data.

### set_close_friends

```python
set_close_friends(self: 'darkob.Rubino', target_profiles: Union[str, List[str]], my_profile: Optional[str]=None)
```

Add profiles to close friends.

Parameters:
    target_profiles (Union[str, List[str]]): A profile ID/username or a list of profile IDs/usernames to add as close friends.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

Examples:
    # Add a single close friend
    await client.set_close_friends(
        target_profiles="Online_User",
        my_profile="MAXRubikaTest"
    )

    # Add multiple close friends
    await client.set_close_friends(
        target_profiles=["Online_User", "PythonChannel"],
        my_profile="MAXRubikaTest"
    )

### set_page_avatar

```python
set_page_avatar(self: 'darkob.Rubino', avatar_file: str, avatar_thumbnail: Optional[str]=None, my_profile: Optional[str]=None)
```

Set or update the avatar of a page (profile).

Parameters:
    avatar_file (str): Local path to the new avatar main image.
    avatar_thumbnail (str, optional): Local path to the new avatar thumbnail image. If not provided, the main file is uploaded again as the thumbnail.
    my_profile (str, optional): The profile to update. Defaults to self.profile_id.

Returns:
    The response data.

Examples:
    # Set avatar (thumbnail auto-uploaded from main)
    await client.set_page_avatar(
        avatar_file="avatar.jpg",
        my_profile="MAXRubikaTest"
    )

    # Set avatar with explicit thumbnail
    await client.set_page_avatar(
        avatar_file="avatar.jpg",
        avatar_thumbnail="avatar_thumb.jpg",
        my_profile="MAXRubikaTest"
    )

### set_post_feedback

```python
set_post_feedback(self: 'darkob.Rubino', target_profile: str, post: str, action: Literal['Interested', 'NotInterested']='Interested', track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Set feedback (interested/not interested) for a post.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post (str): The post link or post ID.
    action (Literal['Interested', 'NotInterested']): The feedback action. Case-insensitive. Default is 'Interested'.
    track_id (str, optional): A tracking ID. Defaults to None.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### set_profile_admin

```python
set_profile_admin(self: 'darkob.Rubino', target_profile: str, access: Union[str, List[str]], my_profile: Optional[str]=None)
```

Set admin access for a profile.

Parameters:
    target_profile (str): The profile ID or username of the admin.
    access (Union[str, List[str]]): A single access permission or a list of them. Pass 'All' (case-insensitive) to grant all permissions.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### set_profile_setting

```python
set_profile_setting(self: 'darkob.Rubino', story_allow_reply: Optional[str]=None, story_save_to_gallery: Optional[bool]=None, story_save_to_archive: Optional[bool]=None, post_save_to_gallery: Optional[bool]=None, allow_tag: Optional[str]=None, message_allowed: Optional[str]=None, hide_comment_count: Optional[bool]=None, hide_like_count: Optional[bool]=None, hide_share_count: Optional[bool]=None, message_receiver_profile_id: Optional[str]=None, show_avatar_full_size: Optional[bool]=None, muted_notif: Optional[bool]=None, my_profile: Optional[str]=None)
```

Update profile settings.

Parameters:
    story_allow_reply (str, optional): Who can reply to stories.
    story_save_to_gallery (bool, optional): Save stories to gallery.
    story_save_to_archive (bool, optional): Save stories to archive.
    post_save_to_gallery (bool, optional): Save posts to gallery.
    allow_tag (str, optional): Who can tag the profile.
    message_allowed (str, optional): Who can send messages.
    hide_comment_count (bool, optional): Hide comment count.
    hide_like_count (bool, optional): Hide like count.
    hide_share_count (bool, optional): Hide share count.
    message_receiver_profile_id (str, optional): The profile that receives messages.
    show_avatar_full_size (bool, optional): Show the avatar in full size.
    muted_notif (bool, optional): Mute notifications.
    my_profile (str, optional): The profile to update. Defaults to self.profile_id.

Returns:
    The response data.

### set_profile_status

```python
set_profile_status(self: 'darkob.Rubino', profile_status: Literal['Public', 'Private'], my_profile: Optional[str]=None)
```

Set the visibility status of a page (profile).

Parameters:
    profile_status (Literal['Public', 'Private']): The new visibility. Case-insensitive.
    my_profile (str, optional): The profile to update. Defaults to self.profile_id.

Returns:
    The response data.

### set_profile_type

```python
set_profile_type(self: 'darkob.Rubino', profile_type: Literal['Business', 'Personal', 'Creator'], my_profile: Optional[str]=None)
```

Set the type of a page (profile).

Parameters:
    profile_type (Literal['Business', 'Personal', 'Creator']): The new page type. Case-insensitive.
    my_profile (str, optional): The profile to update. Defaults to self.profile_id.

Returns:
    The response data.

### track_client_metrics

```python
track_client_metrics(self: 'darkob.Rubino', network: Literal['WiFi', '2G', '3G', '4G', '5G', 'Offline'], metrics: List[Dict], my_profile: Optional[str]=None)
```

Track client metrics for analytics.

Parameters:
    network (Literal['WiFi', '2G', '3G', '4G', '5G', 'Offline']): The current network type. Case-insensitive.
    metrics (List[Dict]): List of metric entries. Each entry must contain 'type' ('LoadingFile' or 'UploadingFile') and the corresponding data ('loading_file_data' for LoadingFile, 'uploading_file_data' for UploadingFile).
    my_profile (str, optional): The profile that reports. Defaults to self.profile_id.

Returns:
    The response data.

Examples:
    # Upload metrics for a successful image upload
    await client.track_client_metrics(
        network="WiFi",
        metrics=[
            {
                "type": "UploadingFile",
                "uploading_file_data": {
                    "status": "Success",
                    "media_type": "Image",
                    "file_size_bytes": 123456,
                    "upload_ms": 1500,
                    "convert_ms": 200,
                    "publish_ms": 300,
                    "total_ms": 2000,
                    "attempts_count": 1,
                    "media_count": 1,
                    "video_count": 0,
                    "is_foreground": True,
                    "is_streaming_upload": False,
                    "stalled": False
                }
            }
        ],
        my_profile="MAXRubikaTest"
    )

    # Upload metrics for a failed video upload
    await client.track_client_metrics(
        network="4G",
        metrics=[
            {
                "type": "UploadingFile",
                "uploading_file_data": {
                    "status": "Failed",
                    "media_type": "Video",
                    "file_size_bytes": 5242880,
                    "upload_ms": 12000,
                    "total_ms": 15000,
                    "attempts_count": 3,
                    "media_count": 1,
                    "video_count": 1,
                    "video_duration_ms": 30000,
                    "is_foreground": True,
                    "stalled": True,
                    "stalled_stage": "UploadingFile",
                    "failed_stage": "UploadingFile",
                    "error_type": "NetworkError",
                    "error_detail": "Connection timed out"
                }
            }
        ],
        my_profile="MAXRubikaTest"
    )

    # Loading metrics for a video viewed in feed
    await client.track_client_metrics(
        network="WiFi",
        metrics=[
            {
                "type": "LoadingFile",
                "loading_file_data": {
                    "view_type": "Reels",
                    "downloaded_bytes": 1048576,
                    "loading_count": 1,
                    "reached_first_frame": True,
                    "startup_ms": 500,
                    "startup_buffering_ms": 200,
                    "rebuffer_ms": 100,
                    "watch_ms": 8000
                }
            }
        ],
        my_profile="MAXRubikaTest"
    )

    # Multiple metrics in one request
    await client.track_client_metrics(
        network="WiFi",
        metrics=[
            {
                "type": "UploadingFile",
                "uploading_file_data": {
                    "status": "Success",
                    "media_type": "Image",
                    "file_size_bytes": 200000,
                    "upload_ms": 1000,
                    "total_ms": 1500,
                    "attempts_count": 1
                }
            },
            {
                "type": "LoadingFile",
                "loading_file_data": {
                    "view_type": "Simple",
                    "downloaded_bytes": 500000,
                    "reached_first_frame": True,
                    "startup_ms": 300,
                    "watch_ms": 4000
                }
            }
        ],
        my_profile="MAXRubikaTest"
    )

### unblock_profile

```python
unblock_profile(self: 'darkob.Rubino', target_profile: str, post_track_id: Optional[str]=None, profile_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Unblock a profile.

Parameters:
    target_profile (str): The profile ID or username to unblock.
    post_track_id (str, optional): The post track ID. Only used in API version 1.
    profile_track_id (str, optional): The profile track ID. Only used in API version 1.
    my_profile (str, optional): The profile that unblocks. Defaults to self.profile_id.

Returns:
    The response data.

### unfollow_page

```python
unfollow_page(self: 'darkob.Rubino', target_profile: str, post_track_id: Optional[str]=None, profile_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Unfollow a page (profile).

Parameters:
    target_profile (str): The profile ID or username to unfollow.
    post_track_id (str, optional): The post track ID. Only used in API version 1.
    profile_track_id (str, optional): The profile track ID. Only used in API version 1.
    my_profile (str, optional): The profile that unfollows. Defaults to self.profile_id.

Returns:
    The response data.

### unhide_post_comment

```python
unhide_post_comment(self: 'darkob.Rubino', post: str, comment_id: str, post_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Unhide a comment on a post.

Parameters:
    post (str): The post link or post ID.
    comment_id (str): The ID of the comment.
    post_track_id (str, optional): The post track ID. Defaults to None.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### unlike_post

```python
unlike_post(self: 'darkob.Rubino', target_profile: Optional[str]=None, post: Optional[str]=None, post_ids: Optional[List[Dict]]=None, my_profile: Optional[str]=None)
```

Unlike one or more posts.

Parameters:
    target_profile (str, optional): The profile ID or username that owns the post. Use together with 'post'.
    post (str, optional): The post link or post ID. Use together with 'target_profile'.
    post_ids (List[Dict], optional): List of post identifiers for batch unlike. Each item must contain 'post' (link or ID) and 'target_profile' (profile ID or username). Cannot be used together with 'post' or 'target_profile'.
    my_profile (str, optional): The profile that unlikes. Defaults to self.profile_id.

Returns:
    The response data.

### unlike_post_comment

```python
unlike_post_comment(self: 'darkob.Rubino', post: str, comment_id: str, post_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Unlike a comment on a post.

Parameters:
    post (str): The post link or post ID.
    comment_id (str): The ID of the comment.
    post_track_id (str, optional): The post track ID. Defaults to None.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### unpin_post_comment

```python
unpin_post_comment(self: 'darkob.Rubino', post: str, comment_id: str, post_track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Unpin a comment from a post.

Parameters:
    post (str): The post link or post ID.
    comment_id (str): The ID of the comment.
    post_track_id (str, optional): The post track ID. Defaults to None.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### unsave_post

```python
unsave_post(self: 'darkob.Rubino', target_profile: Optional[str]=None, post: Optional[str]=None, post_ids: Optional[List[Dict]]=None, my_profile: Optional[str]=None)
```

Remove a bookmark from one or more posts.

Parameters:
    target_profile (str, optional): The profile ID or username that owns the post. Use together with 'post'.
    post (str, optional): The post link or post ID. Use together with 'target_profile'.
    post_ids (List[Dict], optional): List of post identifiers for batch unsave. Each item must contain 'post' (link or ID) and 'target_profile' (profile ID or username). Cannot be used together with 'post' or 'target_profile'.
    my_profile (str, optional): The profile that removes the bookmark. Defaults to self.profile_id.

Returns:
    The response data.

### unset_close_friends

```python
unset_close_friends(self: 'darkob.Rubino', target_profiles: Union[str, List[str]], my_profile: Optional[str]=None)
```

Remove profiles from close friends.

Parameters:
    target_profiles (Union[str, List[str]]): A profile ID/username or a list of profile IDs/usernames to remove from close friends.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

Examples:
    # Remove a single close friend
    await client.unset_close_friends(
        target_profiles="u0abc123def",
        my_profile="MAXRubikaTest"
    )

    # Remove multiple close friends
    await client.unset_close_friends(
        target_profiles=["u0abc123def", "u0xyz789ghi"],
        my_profile="MAXRubikaTest"
    )

### unset_profile_admin

```python
unset_profile_admin(self: 'darkob.Rubino', target_profile: str, my_profile: Optional[str]=None)
```

Unset (remove) all admin access for a profile.

Parameters:
    target_profile (str): The profile ID or username of the admin.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### update_page

```python
update_page(self: 'darkob.Rubino', name: Optional[str]=None, username: Optional[str]=None, profile_status: Optional[Literal['Public', 'Private']]=None, profile_type: Optional[Literal['Business', 'Personal', 'Creator']]=None, bio: Optional[str]=None, email: Optional[str]=None, phone: Optional[str]=None, website: Optional[str]=None, avatar_file: Optional[str]=None, avatar_thumbnail: Optional[str]=None, delete_avatar: bool=False, my_profile: Optional[str]=None)
```

Update a page (profile).

Only the fields that are provided (not None) will be updated. Contact fields are merged: providing an empty string removes that contact type, while other existing contacts are preserved.

Parameters:
    name (str, optional): The new display name.
    username (str, optional): The new username.
    profile_status (Literal['Public', 'Private'], optional): The new visibility. Case-insensitive.
    profile_type (Literal['Business', 'Personal', 'Creator'], optional): The new page type. Case-insensitive.
    bio (str, optional): The new bio.
    email (str, optional): The new email contact. If empty string, removes the email contact.
    phone (str, optional): The new phone contact. If empty string, removes the phone contact.
    website (str, optional): The new website contact. If empty string, removes the website contact.
    avatar_file (str, optional): Local path to the new avatar main image. If 'avatar_thumbnail' is not provided, the main file is uploaded again as the thumbnail. Cannot be used together with 'delete_avatar'.
    avatar_thumbnail (str, optional): Local path to the new avatar thumbnail image.
    delete_avatar (bool, optional): If True, removes the current avatar. Cannot be used together with 'avatar_file'. Default is False.
    my_profile (str, optional): The profile to update. Defaults to self.profile_id.

Returns:
    The response data.

Examples:
    # Update name only
    await client.update_page(name="New Name")

    # Update bio and status
    await client.update_page(
        bio="New bio",
        profile_status="Private"
    )

    # Update contacts individually
    await client.update_page(
        email="info@example.com",
        phone="9986",
        website="https://example.com"
    )

    # Remove a single contact
    await client.update_page(email="")

    # Update avatar (thumbnail auto-uploaded from main if omitted)
    await client.update_page(
        avatar_file="new_avatar.jpg"
    )

    # Update avatar with explicit thumbnail
    await client.update_page(
        avatar_file="new_avatar.jpg",
        avatar_thumbnail="new_avatar_thumb.jpg"
    )

    # Delete the current avatar
    await client.update_page(delete_avatar=True)

### update_post

```python
update_post(self: 'darkob.Rubino', post: str, caption: Optional[str]=None, location_id: Optional[str]=None, update_post_file_list: Optional[List[Dict]]=None, hide_comment_count: Optional[bool]=None, hide_like_count: Optional[bool]=None, show_only_close_friend: Optional[bool]=None, hide_share_count: Optional[bool]=None, collaborators: Optional[List[str]]=None, my_profile: Optional[str]=None)
```

Update a post.

Parameters:
    post (str): The post link or post ID.
    caption (str, optional): The new caption.
    location_id (str, optional): The new location ID.
    update_post_file_list (List[Dict], optional): List of file updates. Each item must contain 'file_index' (int) and may contain 'alt_text', 'tag_list', 'product_list'.
    hide_comment_count (bool, optional): Hide the comment count.
    hide_like_count (bool, optional): Hide the like count.
    show_only_close_friend (bool, optional): Show only to close friends.
    hide_share_count (bool, optional): Hide the share count.
    collaborators (List[str], optional): List of collaborator profile IDs or usernames.
    my_profile (str, optional): The profile that performs the action. Defaults to self.profile_id.

Returns:
    The response data.

### update_post_share_count

```python
update_post_share_count(self: 'darkob.Rubino', target_profile: str, post: str, target_object_type: Literal['User', 'Channel', 'Group', 'Service', 'Bot']='Channel', target_object_id: Optional[str]=None, type: str='Message', track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Update the share count of a post.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post (str): The post link or post ID.
    target_object_type (Literal['User', 'Channel', 'Group', 'Service', 'Bot']): The type of the destination object. Case-insensitive.
    target_object_id (str, optional): The ID of the destination (chat/channel/group). Defaults to None.
    type (str, optional): The share type. Default is 'Message'.
    track_id (str, optional): A tracking ID. Defaults to None.
    my_profile (str, optional): The profile that shares. Defaults to self.profile_id.

Returns:
    The response data.

### upload_file

```python
upload_file(self: 'darkob.Rubino', file: str, file_type: Literal['Picture', 'Video']='Picture', mime: Optional[str]=None, my_profile: Optional[str]=None)
```

Upload a local file or bytes to Rubino.

Parameters:
    file (str | bytes): Local path or raw bytes of the file.
    file_type (Literal["Picture", "Video"]): Either 'Picture' or 'Video'.
        Case-insensitive. Defaults to 'Picture'.
    mime (str, optional): MIME type. Defaults based on file_type
        ('jpg' for Picture, 'mp4' for Video).
    my_profile (str, optional): The profile that uploads. Defaults to self.profile_id.

Returns:
    Data: Upload result containing file_id, hash_file_request, server_url, and hash_file_receive.

### view_feed_data

```python
view_feed_data(self: 'darkob.Rubino', target_profile: Optional[str]=None, post: Optional[str]=None, post_ids: Optional[List[Dict]]=None, my_profile: Optional[str]=None)
```

Register views for feed posts.

Parameters:
    target_profile (str, optional): The profile ID or username that owns the post. Use together with 'post'.
    post (str, optional): The post link or post ID. Use together with 'target_profile'.
    post_ids (List[Dict], optional): List of post identifiers for batch view. Each item must contain 'post' (link or ID) and 'target_profile' (profile ID or username). Cannot be used together with 'post' or 'target_profile'.
    my_profile (str, optional): The profile that views. Defaults to self.profile_id.

Returns:
    The response data.

### view_post

```python
view_post(self: 'darkob.Rubino', target_profile: str, post: str, view_duration: int=5, file_list_index: int=0, play_duration: Optional[int]=None, track_id: Optional[str]=None, my_profile: Optional[str]=None)
```

Register a view for a post.

Parameters:
    target_profile (str): The profile ID or username that owns the post.
    post (str): The post link or post ID.
    view_duration (int, optional): View duration in seconds. Only used in api_version=1. Default is 5.
    file_list_index (int, optional): Index of the file in the post's file list. Only used in api_version=1. Default is 0.
    play_duration (int, optional): Play duration in seconds. Only used in api_version=1.
    track_id (str, optional): Tracking ID for the view. Only used in api_version=1.
    my_profile (str, optional): The profile that views the post. Defaults to self.profile_id.

Returns:
    The response data.

### view_story

```python
view_story(self: 'darkob.Rubino', target_profile: str, story_id: Union[str, List[str]], my_profile: Optional[str]=None)
```

Mark stories as viewed.

Parameters:
    target_profile (str): The profile ID or username that owns the stories.
    story_id (str | list): A story ID or list of story IDs.
    my_profile (str, optional): The profile that views. Defaults to self.profile_id.

Returns:
    The response data.
