"""Tests for the protocol snapshot tracker."""

from __future__ import annotations

from types import SimpleNamespace

from darkob.protocol import ProtocolSnapshot, ProtocolTracker


def make_connection(api_url="https://api.example/", wss_url="wss://ws.example"):
    return SimpleNamespace(
        api_url=api_url,
        wss_url=wss_url,
        api_priority=["1", "2"],
    )


def make_client(platform="PWA", app_version="2.5.8"):
    return SimpleNamespace(
        DEFAULT_PLATFORM={"platform": platform, "app_version": app_version}
    )


def test_snapshot_captures_the_layout():
    snapshot = ProtocolSnapshot.capture(make_connection(), make_client())

    assert snapshot.api_url == "https://api.example/"
    assert snapshot.wss_url == "wss://ws.example"
    assert snapshot.api_codes == ["1", "2"]
    assert snapshot.platform == "PWA"
    assert snapshot.app_version == "2.5.8"


def test_first_record_reports_no_changes(tmp_path):
    tracker = ProtocolTracker(path=str(tmp_path / "protocol.json"))

    assert tracker.record(make_connection(), make_client()) == []


def test_second_record_reports_drift(tmp_path):
    tracker = ProtocolTracker(path=str(tmp_path / "protocol.json"))
    tracker.record(make_connection(), make_client())

    changes = tracker.record(
        make_connection(api_url="https://api2.example/", wss_url="wss://ws2.example"),
        make_client(),
    )

    assert any("api_url" in change for change in changes)
    assert any("wss_url" in change for change in changes)


def test_record_reports_a_version_bump(tmp_path):
    tracker = ProtocolTracker(path=str(tmp_path / "protocol.json"))
    tracker.record(make_connection(), make_client(app_version="2.5.8"))

    changes = tracker.record(
        make_connection(), make_client(app_version="2.6.0")
    )

    assert changes == ["app_version: '2.5.8' -> '2.6.0'"]


def test_snapshot_survives_reopening(tmp_path):
    path = str(tmp_path / "protocol.json")
    ProtocolTracker(path=path).record(make_connection(), make_client())

    reopened = ProtocolTracker(path=path)

    assert reopened.previous is not None
    assert reopened.previous.api_url == "https://api.example/"


def test_no_changes_between_identical_records(tmp_path):
    tracker = ProtocolTracker(path=str(tmp_path / "protocol.json"))
    tracker.record(make_connection(), make_client())

    assert tracker.record(make_connection(), make_client()) == []


def test_corrupt_snapshot_file_is_ignored(tmp_path):
    path = tmp_path / "protocol.json"
    path.write_text("not json", encoding="utf-8")

    tracker = ProtocolTracker(path=str(path))

    assert tracker.previous is None


def test_tracker_without_a_path_still_diffs_in_memory():
    tracker = ProtocolTracker()
    tracker.record(make_connection(), make_client())

    changes = tracker.record(make_connection(api_url="https://other/"), make_client())

    assert changes


def test_api_code_changes_are_reported():
    tracker = ProtocolTracker()
    tracker.record(make_connection(), make_client())

    connection = make_connection()
    connection.api_priority = ["2", "1"]

    changes = tracker.record(connection, make_client())

    assert any("api_codes" in change for change in changes)
