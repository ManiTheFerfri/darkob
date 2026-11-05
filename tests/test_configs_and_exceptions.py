"""Platform configuration invariants and exception hierarchy guarantees."""

from __future__ import annotations

import pytest

import darkob.client.exceptions as client_exceptions
from darkob.bot import exceptions as bot_exceptions
from darkob.client.core.configs import (
    DEFAULT_PLATFORM,
    PLATFORM_NAME_TO_KEY,
    PLATFORMS,
    RUBIKA_PLATFORM_ALIASES,
    RUBIKA_PLATFORM_NAMES,
    SHAD_PLATFORM_NAMES,
    USER_AGENT,
    VALID_PLATFORMS,
)


# ---------------------------------------------------------------------------
# Platform configuration
# ---------------------------------------------------------------------------


def test_platform_configs_have_required_keys():
    required = {"platform", "get_dcs_url", "storage_prefix"}

    for name, config in PLATFORMS.items():
        missing = required - set(config)
        assert not missing, f"{name} is missing {missing}"


def test_every_platform_url_is_https():
    for name, config in PLATFORMS.items():
        assert config["get_dcs_url"].startswith("https://"), name


def test_valid_platforms_matches_the_table():
    assert VALID_PLATFORMS == list(PLATFORMS.keys())


def test_platform_name_lookup_is_consistent():
    known_platforms = set(PLATFORMS[key]["platform"] for key in PLATFORMS)

    for platform_name, key in PLATFORM_NAME_TO_KEY.items():
        assert key in PLATFORMS, f"{platform_name} maps to unknown key {key}"
        # Alias names (RubX, RubiKids, Rubino) intentionally share the
        # Android config, so only require that the platform value is valid.
        assert PLATFORMS[key]["platform"] in known_platforms


def test_platform_name_sets_cover_the_table():
    names = set(RUBIKA_PLATFORM_NAMES) | set(SHAD_PLATFORM_NAMES)
    assert names == set(PLATFORM_NAME_TO_KEY)


def test_aliases_point_at_real_platforms():
    for alias, name in {**RUBIKA_PLATFORM_ALIASES, **{}}.items():
        assert name in PLATFORM_NAME_TO_KEY, alias


def test_default_platform_is_complete():
    for key in ("app_name", "app_version", "platform", "package", "lang_code"):
        assert DEFAULT_PLATFORM.get(key), key


def test_user_agent_looks_like_a_user_agent():
    assert "Mozilla" in USER_AGENT
    assert len(USER_AGENT) > 30


# ---------------------------------------------------------------------------
# Bot exceptions
# ---------------------------------------------------------------------------


def test_bot_exceptions_share_a_base():
    for name in (
        "Network",
        "Timeout",
        "BadGateway",
        "InvalidResponse",
        "JSONDecode",
        "ServerError",
        "InvalidInput",
        "InvalidAccess",
        "TooRequests",
        "TokenError",
    ):
        cls = getattr(bot_exceptions, name)
        assert issubclass(cls, bot_exceptions.APIException), name


def test_api_exception_is_an_exception():
    assert issubclass(bot_exceptions.APIException, Exception)


# ---------------------------------------------------------------------------
# Client exceptions
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "status,expected",
    [
        ("INVALID_INPUT", client_exceptions.InvalidInput),
        ("INVALID_AUTH", client_exceptions.InvalidAccess),
        ("TOO_REQUESTS", client_exceptions.TooRequests),
        ("SERVER_ERROR", client_exceptions.ServerError),
        ("NOT_REGISTERED", client_exceptions.NotRegistered),
    ],
)
def test_status_lookup_maps_to_typed_exceptions(status, expected):
    assert client_exceptions.get(status) is expected


def test_unknown_status_falls_back_to_client_error():
    assert client_exceptions.get("SOMETHING_NEW") is client_exceptions.ClientError


def test_validation_errors_are_grouped():
    for name in (
        "TimeoutError",
        "ApiVersionError",
        "PlatformError",
        "AuthError",
        "MaxRetriesError",
        "ProxyError",
        "SessionError",
    ):
        cls = getattr(client_exceptions, name)
        assert issubclass(cls, client_exceptions.ValidationError), name


def test_request_errors_are_grouped():
    for name in (
        "InvalidInput",
        "InvalidAccess",
        "TooRequests",
        "ServerError",
        "NotRegistered",
        "CodeIsExpired",
        "UsernameExist",
    ):
        cls = getattr(client_exceptions, name)
        assert issubclass(cls, client_exceptions.RequestError), name


def test_raise_exception_raises_the_mapped_type():
    with pytest.raises(client_exceptions.TooRequests):
        client_exceptions.raise_exception("TOO_REQUESTS", {"status": "TOO_REQUESTS"})
