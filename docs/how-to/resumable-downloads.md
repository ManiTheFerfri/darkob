# Resumable downloads

Download a large file so that an interrupted transfer continues where it stopped instead of starting over.

## What "resume" means in darkob

The Bot API surface (`darkob.Bot`) resumes. There is no sidecar file and
no state to persist: **the partial file on disk is the state**. On the next
call darkob reads its size, asks for the remaining bytes with an HTTP
`Range` header, and appends.

The Messenger surface (`darkob.Messenger` / `darkob.Shad`) does **not**
resume; see [the Messenger equivalent](#the-messenger-equivalent) at the
end of this page.

## Download a file to disk

`event.file_id` comes from the incoming message, so a full round trip is:

```python title="bot.py"
from pathlib import Path

from darkob import Bot

bot = Bot(token="YOUR_BOT_TOKEN")
DOWNLOADS = Path.home() / "downloads"

@bot.on_new_message()
async def save_document(bot, event):
    if not event.file_id:
        return

    result = await bot.download_file(
        event.file_id,
        name="report",            # becomes report.pdf, report.zip, ...
        path=str(DOWNLOADS),      # must be absolute
        save_as=True,
        resume=True,              # the default
    )
    await event.reply(f"Saved {result['file_path']} ({result['size']})")
```

Calling the handler again after a network drop, a process restart or a
`Network` exception re-issues the same download and writes only the missing
tail. Keep `name` and `path` identical between attempts — that is how the
second call finds the first call's bytes.

## The parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `file_id` | required | File id from the update |
| `name` | `None` | Base name, **without** extension; the extension comes from the server's `Content-Type` |
| `path` | `None` | Absolute directory. A relative path raises `InvalidInput` |
| `save_as` | `False` | `True` streams to disk; `False` returns bytes and ignores `name`, `path` and `resume` |
| `as_base64` | `False` | Return a base64 string instead of bytes (only when `save_as=False`) |
| `callback` | `None` | `callback(written, total, percent)` — see below |
| `resume` | `True` | Continue a partial file instead of overwriting it |

`resume` is only consulted when `save_as=True`. With `save_as=False` the
whole body is read into memory through a separate retrying path, and no
file is involved.

!!! note "The extension is not yours to choose"
    darkob sends a `HEAD` request first, maps the response
    `Content-Type` to an extension (`.json` for JSON, `.bin` when unknown)
    and appends it to `name`. Passing `"report.pdf"` therefore produces
    `report.pdf.zip` if the server says the body is a ZIP. Pass the base
    name only.

## How resume state is kept

`Bot.download_file(..., save_as=True)` delegates to an internal
`_download_to_path(url, full_path, resume=..., callback=...)` that does
four things:

1. `existing = os.path.getsize(full_path)` when resume is on and the file
   exists, else `0`.
2. `Range: bytes=<existing>-` when `existing` is non-zero.
3. `416 Range Not Satisfiable` means there is nothing left: the call
   returns `existing` and writes nothing.
4. A `200` answer to a ranged request means the server ignored the range
   and is sending the whole file again. darkob then sets `existing = 0`
   and opens the file with `"wb"`, because appending would corrupt it.

The body is streamed in 256 KiB blocks and handed to the progress callback
as it arrives. The file handle is opened in `"ab"` when resuming and
`"wb"` otherwise.

```text
attempt 1: 0 → 6.0 MB of 10.0 MB   (connection drops)
attempt 2: Range: bytes=6291456-
           server: 206 Partial Content, 3.9 MB
           file now: 10.0 MB
```

!!! warning "Signals to watch for"
    - A resumed file is assumed to be a **prefix** of the same remote
      file. If the remote file changed, the result is corrupt — delete
      the partial file and download again.
    - `resume=False` overwrites from byte zero, which is what you want
      when you have no way to tell whether the local tail is trustworthy.

## Reporting progress

The callback receives three arguments and may be a plain function or a
coroutine:

```python
def progress(written, total, percent):
    print(f"{written}/{total} bytes ({percent:.1f}%)")


await bot.download_file(
    event.file_id,
    name="video",
    path=str(DOWNLOADS),
    save_as=True,
    callback=progress,
)
```

`written` counts bytes on disk including the resumed prefix, and `total`
is the full file size, so the percentage stays meaningful across a resume.
With `save_as=False` the callback fires once with
`(len(data), len(data), 100.0)` after the body is read.

If no `path` is given, darkob saves into the current working directory —
or into `~/Downloads` when the working directory looks like a Visual
Studio Code session. Pass `path` explicitly unless that heuristic suits
you.

## The Messenger equivalent

`darkob.Messenger.download_file` is a different method with a different
signature, and it restarts from byte zero on every call:

| Parameter | Default | Meaning |
| --- | --- | --- |
| `file_inline` | `None` | The message's `file_inline` object; `dc_id`, `file_id`, `access_hash` and `size` are read from it |
| `dc_id`, `file_id`, `access_hash`, `size` | `None` | Or supply all four yourself |
| `chunk` | `131072` | Bytes per ranged request |
| `callback` | `None` | `callback(total_size, downloaded_size)` — two arguments, not three |
| `gather` | `False` | Fetch all chunks concurrently instead of one at a time |
| `save_as` | `None` | Directory, or `True` for the current directory; `None` returns bytes |
| `file_name` | `None` | Overrides the name from `file_inline` |
| `as_base64` | `False` | Return a base64 string |

```python
data = await client.download_file(event.file_inline, save_as=True, file_name="clip")
```

It requires an authenticated client (`start()` first), otherwise it raises
`NoConnection`. Save the bytes yourself if you need resumability on this
surface.

!!! warning "`gather=True` can lose a chunk"
    A chunk that still fails after `max_retries` comes back empty, and the
    parallel path joins whatever it received. Prefer the default
    sequential path for anything whose integrity matters, and verify the
    size afterwards.

## See also

- [All Bot API methods](../api/bot.md)
- [Errors](../guides/errors.md)
- [Reliability](../explanation/reliability.md)
- [First bot](../tutorials/first-bot.md)
- [Bot vs Messenger vs Shad](../explanation/bot-vs-messenger-vs-shad.md)
