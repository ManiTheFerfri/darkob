# RubiAI API reference

Rubika's AI assistant: chat sessions, streaming and image generation.

> Generated from the installed package by `scripts/generate_docs_assets.py`. Every signature below is real; do not hand-edit this file.

**15 public methods.**

## Method index

- **rubiai** (15): [`delete_session`](#delete-session), [`download_image`](#download-image), [`edit_session`](#edit-session), [`get_chat_history`](#get-chat-history), [`get_feedback_issues`](#get-feedback-issues), [`get_service_access`](#get-service-access), [`get_sessions`](#get-sessions), [`get_welcome`](#get-welcome), [`request`](#request), [`send_feedback`](#send-feedback), [`send_message`](#send-message), [`send_message_stream`](#send-message-stream), [`set_feedback_detail`](#set-feedback-detail), [`speech_to_text`](#speech-to-text), [`stop_session_stream`](#stop-session-stream)

## rubiai

### delete_session

```python
delete_session(self: 'darkob.RubiAI', session_id: str)
```

Delete an AI chat session.

Parameters:
    session_id (str): Identifier of the session to delete.

Returns:
    The API response.

### download_image

```python
download_image(self: 'darkob.RubiAI', task_id: str, save_as: Optional[Union['pathlib.Path', str]]=None, max_wait: int=60, interval: int=2)
```

Retrieve an AI-generated image result and optionally save it to disk.

Polls the API until the image is ready (status: Success) or fails (status: Error).

Parameters:
    task_id (str): Image generation/download task identifier.
    save_as (Path | str, optional): Destination path. If omitted, the decoded image is not saved.
    max_wait (int): Maximum seconds to wait for the image (polling).
    interval (int): Seconds between polls.

Returns:
    Parsed image download response (status: Success/Error).

### edit_session

```python
edit_session(self: 'darkob.RubiAI', session_id: str, title: Optional[str]=None, is_pinned: Optional[bool]=None)
```

Update the pin state and/or title of a session.

Parameters:
    session_id (str): Identifier of the session.
    title (str, optional): New session title. None means no update.
    is_pinned (bool, optional): New pin state. None means no update.

Returns:
    The API response.

### get_chat_history

```python
get_chat_history(self: 'darkob.RubiAI', session_id: str, all_pages: bool=True, limit: int=100, start_id: Optional[str]=None)
```

Retrieve messages from an AI session.

Parameters:
    session_id (str): Identifier of the session.
    all_pages (bool): Whether to automatically fetch all pages.
    limit (int): Maximum number of messages per request.
    start_id (str, optional): Starting message identifier for pagination.

Returns:
    The API response.

### get_feedback_issues

```python
get_feedback_issues(self: 'darkob.RubiAI')
```

Retrieve available feedback issue types.

Returns:
    Parsed feedback-issues response.

### get_service_access

```python
get_service_access(self: 'darkob.RubiAI')
```

Retrieve the current AI service access information.

Returns:
    Parsed service-access response.

### get_sessions

```python
get_sessions(self: 'darkob.RubiAI', all_pages: bool=True, limit: int=10, start_id: Optional[str]=None)
```

Retrieve AI chat sessions.

Parameters:
    all_pages (bool): Whether to automatically paginate through all sessions.
    limit (int): Maximum number of sessions requested per API call.
    start_id (str, optional): Starting session ID for pagination. Only used when all_pages is False or as the initial point.

Returns:
    The API response.

### get_welcome

```python
get_welcome(self: 'darkob.RubiAI', location: Literal['VOD', 'Home', 'Messenger', 'Social']='Messenger', location_id: str='')
```

Retrieve welcome information for a specified application location.

Parameters:
    location (str): Application location. Case-insensitive.
        Accepts: 'VOD', 'Home', 'Messenger', 'Social'.
    location_id (str): Optional identifier of the location.

Returns:
    The API response.

### request

```python
request(self: 'darkob.RubiAI', method: str, input: Optional[Dict[str, Any]]=None)
```

Send a normal HTTP request to the AI API.

Parameters:
    method (str): Remote API method name.
    input (dict): Method-specific input parameters.

Returns:
    The API output (wrapped in Data by default).

### send_feedback

```python
send_feedback(self: 'darkob.RubiAI', session_id: str, message_id: str, feedback: Literal['Like', 'Dislike', 'None'])
```

Submit feedback for an AI message.

Parameters:
    session_id (str): Identifier of the session containing the message.
    message_id (str): Identifier of the message.
    feedback (str): Feedback value: Like, Dislike, or None. Case-insensitive.

Returns:
    The API response.

### send_message

```python
send_message(self: 'darkob.RubiAI', message: str, session_id: str='', is_support: bool=False, generate_image: bool=False)
```

Send a message to the AI service and return the assembled result.

Parameters:
    message (str): Text message to send.
    session_id (str): Existing session ID to continue a conversation.
    is_support (bool): Whether the message is a support request.
    generate_image (bool): Whether to request image generation.

Returns:
    Assembled result with text_content, title, session_id, message_id.

### send_message_stream

```python
send_message_stream(self: 'darkob.RubiAI', message: str, session_id: str='', is_support: bool=False, generate_image: bool=False)
```

Send a message to the AI service and yield streamed events progressively.

Parameters:
    message (str): Text message to send.
    session_id (str): Existing session ID to continue a conversation.
    is_support (bool): Whether the message is a support request.
    generate_image (bool): Whether to request image generation.

Yields:
    Each parsed SSE event.

### set_feedback_detail

```python
set_feedback_detail(self: 'darkob.RubiAI', session_id: str, message_id: str, feedback_issue_type: str, feedback_issue_desc: Optional[str]=None)
```

Set detailed information for previously submitted feedback.

Parameters:
    session_id (str): Identifier of the session.
    message_id (str): Identifier of the message.
    feedback_issue_type (str): Feedback issue/category type (from get_feedback_issues).
    feedback_issue_desc (str, optional): Optional sub-item / description.

Returns:
    The API response.

### speech_to_text

```python
speech_to_text(self: 'darkob.RubiAI', voice_data: Union[str, bytes, 'pathlib.Path', 'io.BytesIO'])
```

Convert voice data to text using the AI speech-to-text service.

Parameters:
    voice_data (str | bytes | Path | BytesIO): Audio data as a file path, raw bytes, BytesIO, or a string containing a file path.

Returns:
    The API response.

### stop_session_stream

```python
stop_session_stream(self: 'darkob.RubiAI', session_id: str, message_id: str, feedback: Literal['Like', 'Dislike']='Like')
```

Stop an active AI session stream and submit the final feedback.

Parameters:
    session_id (str): Identifier of the session.
    message_id (str): Identifier of the streamed message.
    feedback (str): Final feedback value. Case-insensitive.
        Accepts: 'Like', 'Dislike' (and 'Good'/'Bad' as aliases).

Returns:
    The API response.

Raises:
    InvalidInput: If feedback is invalid.
