# RubikaTV API reference

Rubika TV/VOD: media discovery, playback, lists and reactions.

> Generated from the installed package by `scripts/generate_docs_assets.py`. Every signature below is real; do not hand-edit this file.

**28 public methods.**

## Method index

- **tv** (28): [`add_wish_media`](#add-wish-media), [`dislike_media`](#dislike-media), [`follow_media`](#follow-media), [`get_cast_details`](#get-cast-details), [`get_cast_medias`](#get-cast-medias), [`get_custom_menu_items`](#get-custom-menu-items), [`get_list_items`](#get-list-items), [`get_listing`](#get-listing), [`get_me`](#get-me), [`get_media`](#get-media), [`get_media_by_link`](#get-media-by-link), [`get_media_related`](#get-media-related), [`get_next_episode`](#get-next-episode), [`get_next_media_info`](#get-next-media-info), [`get_play_info`](#get-play-info), [`get_play_suggested_episode`](#get-play-suggested-episode), [`get_property_types`](#get-property-types), [`get_season_episodes`](#get-season-episodes), [`get_wish_list`](#get-wish-list), [`like_media`](#like-media), [`remove_wish_list_media`](#remove-wish-list-media), [`request`](#request), [`search_movie`](#search-movie), [`set_current_play_time`](#set-current-play-time), [`set_session_play_duration`](#set-session-play-duration), [`undo_like_or_dislike_media`](#undo-like-or-dislike-media), [`unfollow_media`](#unfollow-media), [`view_commercial`](#view-commercial)

## tv

### add_wish_media

```python
add_wish_media(self: 'darkob.RubikaTV', media_id: str, track_id: Optional[str]=None)
```

Add a media to the wishlist.

Parameters:
    media_id (str): Identifier of the media.
    track_id (str, optional): Optional tracking identifier.

Returns:
    The API output.

### dislike_media

```python
dislike_media(self: 'darkob.RubikaTV', media_id: str, track_id: Optional[str]=None)
```

Dislike a media.

Parameters:
    media_id (str): Identifier of the media.
    track_id (str, optional): Optional tracking identifier.

Returns:
    The API output.

### follow_media

```python
follow_media(self: 'darkob.RubikaTV', media_id: str, track_id: Optional[str]=None)
```

Follow a media.

Parameters:
    media_id (str): Identifier of the media.
    track_id (str, optional): Optional tracking identifier.

Returns:
    The API output.

### get_cast_details

```python
get_cast_details(self: 'darkob.RubikaTV', cast_id: str)
```

Retrieve details of a cast member.

Parameters:
    cast_id (str): Identifier of the cast member.

Returns:
    The API output.

### get_cast_medias

```python
get_cast_medias(self: 'darkob.RubikaTV', cast_id: str, start_id: Optional[str]=None)
```

Retrieve media associated with a cast member.

Parameters:
    cast_id (str): Identifier of the cast member.
    start_id (str, optional): Optional starting item ID for pagination.

Returns:
    The API output.

### get_custom_menu_items

```python
get_custom_menu_items(self: 'darkob.RubikaTV')
```

Retrieve custom menu items.

Returns:
    The API output.

### get_list_items

```python
get_list_items(self: 'darkob.RubikaTV', list_id: str, type: Literal['Media', 'LinkItem', 'Cast']='Media', is_channel: Optional[bool]=None, start_id: Optional[str]=None)
```

Retrieve items from a VOD list.

Parameters:
    list_id (str): Identifier of the list.
    type (str): Type of items: "Media", "LinkItem", or "Cast". Case-insensitive.
    is_channel (bool, optional): Optional channel filter.
    start_id (str, optional): Starting item ID for pagination.

Returns:
    The API output.

### get_listing

```python
get_listing(self: 'darkob.RubikaTV', listing_id: str='home')
```

Retrieve a listing (e.g., home page sections).

Parameters:
    listing_id (str): Identifier of the listing (default: "home").

Returns:
    The API output.

### get_me

```python
get_me(self: 'darkob.RubikaTV')
```

Retrieve the current VOD account information.

Returns:
    The API output.

### get_media

```python
get_media(self: 'darkob.RubikaTV', media_id: str, track_id: Optional[str]=None)
```

Retrieve media details by its ID.

Parameters:
    media_id (str): Identifier of the media.
    track_id (str, optional): Optional tracking identifier (session hash string).

Returns:
    The API output.

### get_media_by_link

```python
get_media_by_link(self: 'darkob.RubikaTV', link: str, track_id: Optional[str]=None)
```

Retrieve media details by its share link.

Parameters:
    link (str): Share link (e.g., "https://rubika.ir/vod/294119").
    track_id (str, optional): Optional tracking identifier (session hash string).

Returns:
    The API output.

### get_media_related

```python
get_media_related(self: 'darkob.RubikaTV', media_id: str, section_type: Optional[Literal['PageRelated', 'EndOfStream']]=None, start_id: Optional[str]=None)
```

Retrieve media related to a specific media.

Parameters:
    media_id (str): Identifier of the media.
    section_type (str, optional): Optional section type. One of: "PageRelated", "EndOfStream".
    start_id (str, optional): Optional starting item ID for pagination.

Returns:
    The API output.

### get_next_episode

```python
get_next_episode(self: 'darkob.RubikaTV', episode_id: str)
```

Retrieve the next episode after the given episode.

Parameters:
    episode_id (str): Identifier of the current episode.

Returns:
    The API output.

### get_next_media_info

```python
get_next_media_info(self: 'darkob.RubikaTV', media_id: str, track_id: Optional[str]=None)
```

Retrieve the next media info after the given media.

Parameters:
    media_id (str): Identifier of the media.
    track_id (str, optional): Optional tracking identifier (session hash string).

Returns:
    The API output.

### get_play_info

```python
get_play_info(self: 'darkob.RubikaTV', media_id: str, type: Literal['Main', 'Trailer']='Trailer', version: int=1, track_id: Optional[str]=None)
```

Retrieve playback information for a specific media.

Parameters:
    media_id (str): Identifier of the media.
    type (str): Type of content ("Main" or "Trailer"). Case-insensitive.
    version (int): Version number.
    track_id (str, optional): Optional tracking identifier (session hash string).

Returns:
    The API output.

### get_play_suggested_episode

```python
get_play_suggested_episode(self: 'darkob.RubikaTV', series_id: str, track_id: Optional[str]=None)
```

Retrieve the suggested next episode for a series.

Parameters:
    series_id (str): Identifier of the series.
    track_id (str, optional): Optional tracking identifier (session hash string).

Returns:
    The API output.

### get_property_types

```python
get_property_types(self: 'darkob.RubikaTV')
```

Retrieve available property types.

Returns:
    The API output.

### get_season_episodes

```python
get_season_episodes(self: 'darkob.RubikaTV', season_id: str, series_id: str, section_type: Optional[Literal['MediaInfo', 'Player']]=None, track_id: Optional[str]=None)
```

Retrieve episodes of a season.

Parameters:
    season_id (str): Identifier of the season.
    series_id (str): Identifier of the series.
    section_type (str, optional): Optional section type: "MediaInfo" or "Player". Case-insensitive.
    track_id (str, optional): Optional tracking identifier.

Returns:
    The API output.

### get_wish_list

```python
get_wish_list(self: 'darkob.RubikaTV', start_id: Optional[str]=None)
```

Retrieve the wishlist items.

Parameters:
    start_id (str, optional): Optional starting item ID for pagination.

Returns:
    The API output.

### like_media

```python
like_media(self: 'darkob.RubikaTV', media_id: str, track_id: Optional[str]=None)
```

Like a media.

Parameters:
    media_id (str): Identifier of the media.
    track_id (str, optional): Optional tracking identifier.

Returns:
    The API output.

### remove_wish_list_media

```python
remove_wish_list_media(self: 'darkob.RubikaTV', media_id: str, track_id: Optional[str]=None)
```

Remove a media from the wishlist.

Parameters:
    media_id (str): Identifier of the media.
    track_id (str, optional): Optional tracking identifier.

Returns:
    The API output.

### request

```python
request(self: 'darkob.RubikaTV', method: str, input: Optional[Dict[str, Any]]=None)
```

Send a normal HTTP request to the Rubika VOD/TV API.

Parameters:
    method (str): Remote API method name.
    input (dict): Method-specific input parameters.

Returns:
    The API output (wrapped in Data by default).

### search_movie

```python
search_movie(self: 'darkob.RubikaTV', search_text: str, start_id: Optional[str]=None)
```

Search for movies by text.

Parameters:
    search_text (str): Search text.
    start_id (str, optional): Optional starting item ID for pagination.

Returns:
    The API output.

### set_current_play_time

```python
set_current_play_time(self: 'darkob.RubikaTV', media_id: str, play_time: int)
```

Set the current play time for a media.

Parameters:
    media_id (str): Identifier of the media.
    play_time (int): Current play time in seconds

Returns:
    The API output.

### set_session_play_duration

```python
set_session_play_duration(self: 'darkob.RubikaTV', session_id: str, play_duration: int=0)
```

Set the total play duration for a session.

Parameters:
    session_id (str): Identifier of the session.
    play_duration (int): Total play duration in seconds.

Returns:
    The API output.

### undo_like_or_dislike_media

```python
undo_like_or_dislike_media(self: 'darkob.RubikaTV', media_id: str, track_id: Optional[str]=None)
```

Undo like or dislike on a media.

Parameters:
    media_id (str): Identifier of the media.
    track_id (str, optional): Optional tracking identifier.

Returns:
    The API output.

### unfollow_media

```python
unfollow_media(self: 'darkob.RubikaTV', media_id: str, track_id: Optional[str]=None)
```

Unfollow a media.

Parameters:
    media_id (str): Identifier of the media.
    track_id (str, optional): Optional tracking identifier.

Returns:
    The API output.

### view_commercial

```python
view_commercial(self: 'darkob.RubikaTV', view_type: Literal['Full', 'Half', 'Skip']='Full')
```

Register a commercial view event.

Parameters:
    view_type (str): Type of view ("Full", "Half", or "Skip"). Case-insensitive.

Returns:
    The API output.
