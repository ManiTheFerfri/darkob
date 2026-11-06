# Two stages, on purpose:
#   builder - resolves darkob[speed] and its wheels once, into a private
#             virtualenv, with pip's download cache disabled.
#   runtime - a clean python:3.12-slim that receives only that virtualenv.
#             No pip cache, no build tooling, no repository source, no token.
#
# This image installs darkob from PyPI: it is a runtime for people deploying
# their own bot, not a development environment for this repository. Pin the
# pip line below (e.g. "darkob[speed]==0.17.0") when you want a frozen runtime.

FROM python:3.12-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# The virtualenv is the single artefact carried into the runtime stage.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# "speed" is the msgspec-backed extra. Nothing local is copied: the image is
# built from the published package, so any checkout produces the same image.
RUN pip install --no-cache-dir "darkob[speed]"

FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="darkob" \
      org.opencontainers.image.description="Async Python library for the Rubika & Shad platforms" \
      org.opencontainers.image.source="https://github.com/ManiTheFerfri/darkob" \
      org.opencontainers.image.licenses="MIT"

# Container-friendly Python: unbuffered logs so output shows up immediately,
# no .pyc files written into user code that may be mounted,
# and a faulthandler traceback if the interpreter dies. HOME is set because the
# base image points it at /root, which the runtime user cannot write.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    HOME=/home/darkob \
    PATH="/opt/venv/bin:$PATH"

# Unprivileged runtime user. The uid is explicit so bind mounts and rootless
# container user-namespace mapping stay predictable.
RUN useradd --uid 10001 --user-group --create-home --shell /bin/sh darkob

# Only the virtualenv crosses stages. It stays root-owned so the process
# cannot rewrite the dependencies it is running on.
COPY --from=builder /opt/venv /opt/venv

# Mount the bot's code here at run time:  -v "$PWD":/app
WORKDIR /app
RUN chown darkob:darkob /app

USER darkob

# No token is baked into the image and none is defaulted. DARKOB_BOT_TOKEN
# must be supplied at run time from a secret store, e.g.
#   docker run --rm -e DARKOB_BOT_TOKEN=... -v "$PWD":/app darkob:latest \
#       python main.py
# Anything in ENV/ARG is readable by anyone who can pull or inspect the image,
# so never put a token (or a build ARG default) here.

# An image with no user code should explain itself instead of failing with a
# confusing ImportError for a module the user has not mounted yet.
CMD ["python", "-c", "print('darkob runtime image: no bot code is mounted in /app.'); print('Mount your bot at /app and pass DARKOB_BOT_TOKEN, e.g.'); print('  docker run --rm -e DARKOB_BOT_TOKEN=... -v \"$PWD\":/app darkob:latest python main.py')"]
