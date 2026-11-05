"""TLS verification must default to on, for both the Bot and Messenger surfaces."""

from __future__ import annotations

import pytest

from darkob import Bot, Messenger

from conftest import VALID_TOKEN


def test_bot_verifies_ssl_by_default():
    assert Bot(token=VALID_TOKEN, show_welcome=False).verify_ssl is True


def test_bot_can_opt_out():
    assert Bot(token=VALID_TOKEN, show_welcome=False, verify_ssl=False).verify_ssl is False


def test_messenger_verifies_ssl_by_default():
    messenger = Messenger(auth="a" * 32, api_version=5, show_welcome=False)
    assert messenger.verify_ssl is True


def test_messenger_can_opt_out():
    messenger = Messenger(
        auth="a" * 32, api_version=5, verify_ssl=False, show_welcome=False
    )
    assert messenger.verify_ssl is False


def test_messenger_rejects_non_boolean_verify_ssl():
    with pytest.raises(ValueError):
        Messenger(
            auth="a" * 32, api_version=5, verify_ssl="no", show_welcome=False
        )
