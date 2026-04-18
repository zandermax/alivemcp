"""Tests for Live 12 application info tools: build id, variant, message box,
and application version."""

import sys
from unittest.mock import patch

import pytest

import ALiveMCP_Remote.tools.m4l_and_live12 as m4l_module


@pytest.fixture
def live_in_m4l():
    from unittest.mock import MagicMock

    fresh_live = MagicMock()
    with patch.dict(sys.modules, {"Live": fresh_live}):
        with patch.object(m4l_module, "Live", fresh_live, create=True):
            yield fresh_live


# ---------------------------------------------------------------------------
# get_build_id
# ---------------------------------------------------------------------------


def test_get_build_id_with_attr(tools, live_in_m4l):
    live_in_m4l.Application.get_application.return_value.get_build_id.return_value = "12345"
    result = tools.get_build_id()
    assert result["ok"] is True
    assert result["build_id"] == "12345"


def test_get_build_id_without_attr(tools, live_in_m4l):
    del live_in_m4l.Application.get_application.return_value.get_build_id
    result = tools.get_build_id()
    assert result["ok"] is False


def test_get_build_id_exception(tools, live_in_m4l):
    live_in_m4l.Application.get_application.side_effect = Exception("err")
    result = tools.get_build_id()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_variant
# ---------------------------------------------------------------------------


def test_get_variant_with_attr(tools, live_in_m4l):
    live_in_m4l.Application.get_application.return_value.get_variant.return_value = "Suite"
    result = tools.get_variant()
    assert result["ok"] is True
    assert result["variant"] == "Suite"


def test_get_variant_without_attr(tools, live_in_m4l):
    del live_in_m4l.Application.get_application.return_value.get_variant
    result = tools.get_variant()
    assert result["ok"] is False


def test_get_variant_exception(tools, live_in_m4l):
    live_in_m4l.Application.get_application.side_effect = Exception("err")
    result = tools.get_variant()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# show_message_box
# ---------------------------------------------------------------------------


def test_show_message_box_with_attr(tools, live_in_m4l):
    live_in_m4l.Application.get_application.return_value.show_message.return_value = 0
    result = tools.show_message_box("Hello")
    assert result["ok"] is True
    assert result["button_pressed"] == 0


def test_show_message_box_result_none(tools, live_in_m4l):
    live_in_m4l.Application.get_application.return_value.show_message.return_value = None
    result = tools.show_message_box("Hello")
    assert result["ok"] is True
    assert result["button_pressed"] == 0


def test_show_message_box_without_attr(tools, live_in_m4l):
    del live_in_m4l.Application.get_application.return_value.show_message
    result = tools.show_message_box("Hello")
    assert result["ok"] is False


def test_show_message_box_exception(tools, live_in_m4l):
    live_in_m4l.Application.get_application.side_effect = Exception("err")
    result = tools.show_message_box("Hello")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_application_version
# ---------------------------------------------------------------------------


def test_get_application_version_basic(tools, live_in_m4l):
    app = live_in_m4l.Application.get_application.return_value
    app.get_major_version.return_value = 11
    app.get_minor_version.return_value = 3
    app.get_bugfix_version.return_value = 2
    del app.get_build_id
    del app.get_variant
    result = tools.get_application_version()
    assert result["ok"] is True
    assert result["major_version"] == 11


def test_get_application_version_with_build_and_variant(tools, live_in_m4l):
    app = live_in_m4l.Application.get_application.return_value
    app.get_major_version.return_value = 12
    app.get_minor_version.return_value = 0
    app.get_bugfix_version.return_value = 0
    app.get_build_id.return_value = "99"
    app.get_variant.return_value = "Suite"
    result = tools.get_application_version()
    assert result["ok"] is True
    assert result["build_id"] == "99"
    assert result["variant"] == "Suite"


def test_get_application_version_exception(tools, live_in_m4l):
    live_in_m4l.Application.get_application.side_effect = Exception("err")
    result = tools.get_application_version()
    assert result["ok"] is False
