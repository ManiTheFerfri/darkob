"""Tests for the Retry policy."""

from __future__ import annotations

import random

import pytest

from darkob.retry import Retry


def test_defaults_are_sane():
    retry = Retry()

    assert retry.attempts == 3
    assert retry.backoff == 1.0
    assert retry.jitter == 0.5


@pytest.mark.parametrize(
    "kwargs",
    [
        {"attempts": 0},
        {"attempts": -1},
        {"backoff": -1},
        {"jitter": -0.1},
        {"jitter": 1.1},
        {"max_delay": 0},
    ],
)
def test_invalid_values_are_rejected(kwargs):
    with pytest.raises(ValueError):
        Retry(**kwargs)


def test_base_delay_grows_linearly_without_jitter():
    retry = Retry(backoff=1.0, jitter=0.0)

    assert retry.delay(1) == 1.0
    assert retry.delay(2) == 2.0
    assert retry.delay(3) == 3.0


def test_max_delay_caps_the_wait():
    retry = Retry(backoff=10.0, jitter=0.0, max_delay=15.0)

    assert retry.delay(5) == 15.0


def test_jitter_stays_within_the_configured_fraction():
    retry = Retry(backoff=10.0, jitter=0.5, max_delay=100.0)
    rng = random.Random(1234)  # deterministic

    samples = [retry.delay(1, rng=rng) for _ in range(200)]

    assert all(5.0 <= value <= 15.0 for value in samples), (min(samples), max(samples))
    assert len(set(samples)) > 1, "jitter should vary the delay"


def test_zero_jitter_is_deterministic():
    retry = Retry(backoff=2.0, jitter=0.0)

    assert retry.delay(3) == retry.delay(3) == 6.0


def test_rate_limited_uses_its_own_backoff():
    retry = Retry(backoff=1.0, jitter=0.0, rate_limit_backoff=8.0, max_delay=100.0)

    assert retry.delay(1, rate_limited=True) == 8.0
    assert retry.delay(2, rate_limited=True) == 16.0
    assert retry.delay(1) == 1.0


def test_rate_limit_backoff_is_capped():
    retry = Retry(jitter=0.0, rate_limit_backoff=10.0, max_delay=25.0)

    assert retry.delay(9, rate_limited=True) == 25.0


def test_should_retry_respects_the_budget():
    retry = Retry(attempts=3)

    assert retry.should_retry(1) is True
    assert retry.should_retry(2) is True
    assert retry.should_retry(3) is False


def test_none_preset_never_waits():
    retry = Retry.none()

    assert retry.attempts == 1
    assert retry.delay(1) == 0.0
    assert retry.should_retry(1) is False


def test_presets_are_ordered_by_patience():
    assert Retry.aggressive().attempts > Retry.patient().attempts
    assert Retry.aggressive().backoff < Retry.patient().backoff


def test_delay_never_returns_a_negative_value():
    retry = Retry(backoff=0.0, jitter=1.0)

    assert retry.delay(5) >= 0.0
