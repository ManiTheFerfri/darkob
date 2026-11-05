"""Tests for the Data wrapper: attribute/item access and recursive lookup."""

from __future__ import annotations

import pytest

from darkob.data import Data


def test_attribute_access():
    data = Data({"status": "OK", "count": 3})

    assert data.status == "OK"
    assert data.count == 3


def test_item_access():
    data = Data({"status": "OK"})

    assert data["status"] == "OK"


def test_missing_attribute_lists_available_keys():
    data = Data({"status": "OK", "count": 1})

    with pytest.raises(AttributeError) as excinfo:
        _ = data.missing

    message = str(excinfo.value)
    assert "missing" in message
    assert "status" in message


def test_missing_key_raises_keyerror():
    with pytest.raises(KeyError):
        _ = Data({"a": 1})["b"]


def test_nested_dicts_become_data_objects():
    data = Data({"message": {"text": "hi"}})

    assert isinstance(data["message"], Data)
    assert data["message"]["text"] == "hi"


def test_find_keys_searches_nested_structures():
    data = Data({"result": {"inner": [{"target": "found"}]}})

    assert data.find_keys("target") == "found"


def test_find_keys_returns_default_when_absent():
    data = Data({"a": 1})

    assert data.find_keys("nope", default="fallback") == "fallback"


def test_len_and_contains():
    data = Data({"a": 1, "b": 2})

    assert len(data) == 2
    assert "a" in data
    assert "z" not in data


def test_iteration_yields_keys_for_dicts():
    assert sorted(Data({"b": 1, "a": 2})) == ["a", "b"]


def test_iteration_converts_list_items():
    data = Data([{"a": 1}])

    first = next(iter(data))
    assert isinstance(first, Data)
    assert first["a"] == 1


def test_set_and_delete_item():
    data = Data({"a": 1})
    data["b"] = 2
    assert data["b"] == 2

    del data["b"]
    assert "b" not in data


def test_list_indexing():
    data = Data([{"a": 1}, {"a": 2}])

    assert data[0]["a"] == 1


def test_jsonify_roundtrip():
    import json

    payload = {"a": 1, "b": [{"c": 2}]}
    data = Data(payload)

    assert json.loads(data.jsonify()) == payload


def test_repr_is_informative():
    assert "Data" in repr(Data({"a": 1}))
