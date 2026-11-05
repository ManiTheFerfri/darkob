# Installation

## Requirements

- Python **3.9 – 3.14**
- Linux, macOS or Windows

## Install

```bash
pip install darkob
```

Optional extras, needed only for specific media features:

```bash
pip install "darkob[opencv]"     # video thumbnails via OpenCV
pip install "darkob[movie]"      # video thumbnails via MoviePy
pip install "darkob[pillow]"     # image thumbnails via Pillow
pip install "darkob[aiortc]"     # voice chats
pip install "darkob[pro]"        # everything above
```

## Verify

```bash
python -c "import darkob; print(darkob.__version__)"
```

Importing darkob performs no network I/O and prints nothing unless you
ask it to.

## Development install

```bash
git clone https://github.com/ManiTheFerfri/darkob.git
cd darkob
pip install -e ".[dev]"

pytest                 # 121 tests, no network required
ruff check .           # lint
pytest --cov=darkob    # coverage
```

## The banner

`Bot(...)` and `Messenger(...)` print a one-time welcome banner. Disable
it when it would pollute logs:

```python
bot = Bot(token="...", show_welcome=False)
```

## Checking for updates

Never automatic. Call it yourself if you want a notice:

```python
import darkob
darkob.check_for_updates()   # returns the new version string, or None
```
