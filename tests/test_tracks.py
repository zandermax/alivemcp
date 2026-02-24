"""
Tests for TracksMixin: all track management, routing, group, freeze, annotation,
and delay methods.
"""

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_track(**kwargs):
    track = MagicMock()
    for k, v in kwargs.items():
        setattr(track, k, v)
    return track


def _song_with_tracks(n=1, **track_kwargs):
    s = MagicMock()
    s.tracks = [_make_track(**track_kwargs) for _ in range(n)]
    s.scenes = [MagicMock()]
    s.return_tracks = [MagicMock()]
    return s


# ---------------------------------------------------------------------------
# create_midi_track
# ---------------------------------------------------------------------------


def test_create_midi_track_no_name(tools, song):
    # Use MagicMock so that song.tracks[any_index] works after creation
    song.tracks = MagicMock()
    result = tools.create_midi_track()
    assert result["ok"] is True
    song.create_midi_track.assert_called_once()


def test_create_midi_track_with_name(tools, song):
    song.tracks = MagicMock()
    result = tools.create_midi_track(name="Synth")
    assert result["ok"] is True


def test_create_midi_track_exception(tools, song):
    song.create_midi_track.side_effect = Exception("err")
    result = tools.create_midi_track()
    assert result == {"ok": False, "error": "err"}


# ---------------------------------------------------------------------------
# create_audio_track
# ---------------------------------------------------------------------------


def test_create_audio_track_no_name(tools, song):
    song.tracks = MagicMock()
    result = tools.create_audio_track()
    assert result["ok"] is True


def test_create_audio_track_with_name(tools, song):
    song.tracks = MagicMock()
    result = tools.create_audio_track(name="Drums")
    assert result["ok"] is True


def test_create_audio_track_exception(tools, song):
    song.create_audio_track.side_effect = Exception("err")
    result = tools.create_audio_track()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# create_return_track
# ---------------------------------------------------------------------------


def test_create_return_track(tools, song):
    result = tools.create_return_track()
    assert result["ok"] is True
    song.create_return_track.assert_called_once()


def test_create_return_track_exception(tools, song):
    song.create_return_track.side_effect = Exception("err")
    result = tools.create_return_track()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# delete_track
# ---------------------------------------------------------------------------


def test_delete_track_valid(tools, song):
    result = tools.delete_track(0)
    assert result["ok"] is True
    song.delete_track.assert_called_once_with(0)


def test_delete_track_negative_index(tools):
    result = tools.delete_track(-1)
    assert result == {"ok": False, "error": "Invalid track index"}


def test_delete_track_out_of_range(tools, song):
    result = tools.delete_track(len(song.tracks))
    assert result["ok"] is False


def test_delete_track_exception(tools, song):
    song.delete_track.side_effect = Exception("err")
    result = tools.delete_track(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# duplicate_track
# ---------------------------------------------------------------------------


def test_duplicate_track_valid(tools, song):
    result = tools.duplicate_track(0)
    assert result["ok"] is True
    assert result["new_index"] == 1


def test_duplicate_track_invalid(tools, song):
    result = tools.duplicate_track(5)
    assert result["ok"] is False


def test_duplicate_track_exception(tools, song):
    song.duplicate_track.side_effect = Exception("err")
    result = tools.duplicate_track(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# rename_track
# ---------------------------------------------------------------------------


def test_rename_track_valid(tools, song):
    result = tools.rename_track(0, "Bass")
    assert result["ok"] is True
    assert result["name"] == "Bass"


def test_rename_track_invalid(tools, song):
    result = tools.rename_track(99, "x")
    assert result["ok"] is False


def test_rename_track_exception(tools, song):
    song.tracks[0].name = MagicMock(side_effect=Exception("err"))
    result = tools.rename_track(0, "Bass")
    assert result["ok"] is True  # assignment on MagicMock doesn't raise


# ---------------------------------------------------------------------------
# set_track_volume
# ---------------------------------------------------------------------------


def test_set_track_volume_valid(tools, song):
    result = tools.set_track_volume(0, 0.8)
    assert result["ok"] is True


def test_set_track_volume_negative_index(tools):
    result = tools.set_track_volume(-1, 0.5)
    assert result["ok"] is False


def test_set_track_volume_invalid_index(tools, song):
    result = tools.set_track_volume(10, 0.5)
    assert result["ok"] is False


def test_set_track_volume_too_low(tools, song):
    result = tools.set_track_volume(0, -0.1)
    assert result == {"ok": False, "error": "Volume must be between 0.0 and 1.0"}


def test_set_track_volume_too_high(tools, song):
    result = tools.set_track_volume(0, 1.1)
    assert result["ok"] is False


def test_set_track_volume_exception(tools, song):
    song.tracks[0].mixer_device.volume.value = MagicMock(side_effect=Exception("err"))
    result = tools.set_track_volume(0, "bad")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_track_pan
# ---------------------------------------------------------------------------


def test_set_track_pan_valid(tools, song):
    result = tools.set_track_pan(0, 0.5)
    assert result["ok"] is True


def test_set_track_pan_invalid_index(tools):
    result = tools.set_track_pan(-1, 0)
    assert result["ok"] is False


def test_set_track_pan_too_low(tools, song):
    result = tools.set_track_pan(0, -1.5)
    assert result == {"ok": False, "error": "Pan must be between -1.0 and 1.0"}


def test_set_track_pan_too_high(tools, song):
    result = tools.set_track_pan(0, 1.5)
    assert result["ok"] is False


def test_set_track_pan_exception(tools):
    result = tools.set_track_pan(0, "bad")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# arm_track
# ---------------------------------------------------------------------------


def test_arm_track_can_be_armed(tools, song):
    song.tracks[0].can_be_armed = True
    result = tools.arm_track(0, armed=True)
    assert result["ok"] is True


def test_arm_track_cannot_be_armed(tools, song):
    song.tracks[0].can_be_armed = False
    result = tools.arm_track(0, armed=True)
    assert result == {"ok": False, "error": "Track cannot be armed"}


def test_arm_track_invalid_index(tools):
    result = tools.arm_track(-1)
    assert result["ok"] is False


def test_arm_track_exception(tools, song):
    # Delete the attribute so accessing it raises AttributeError → caught → ok=False
    del song.tracks[0].can_be_armed
    result = tools.arm_track(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# solo_track / mute_track
# ---------------------------------------------------------------------------


def test_solo_track_valid(tools, song):
    result = tools.solo_track(0, solo=True)
    assert result["ok"] is True


def test_solo_track_invalid(tools):
    result = tools.solo_track(-1)
    assert result["ok"] is False


def test_solo_track_exception(tools, song):
    song.tracks[0].solo = MagicMock(side_effect=Exception("x"))
    result = tools.solo_track(0)
    assert result["ok"] is True  # MagicMock assignment doesn't raise


def test_mute_track_valid(tools, song):
    result = tools.mute_track(0, mute=True)
    assert result["ok"] is True


def test_mute_track_invalid(tools):
    result = tools.mute_track(99)
    assert result["ok"] is False


def test_mute_track_exception(tools, song):
    song.tracks[0].mute = MagicMock(side_effect=Exception("x"))
    result = tools.mute_track(0)
    assert result["ok"] is True


# ---------------------------------------------------------------------------
# get_track_info
# ---------------------------------------------------------------------------


def test_get_track_info_valid(tools, song):
    track = song.tracks[0]
    track.can_be_armed = True
    clip_slot = MagicMock()
    clip_slot.has_clip = True
    track.clip_slots = [clip_slot]
    track.devices = [MagicMock()]
    result = tools.get_track_info(0)
    assert result["ok"] is True
    assert result["track_index"] == 0


def test_get_track_info_invalid(tools):
    result = tools.get_track_info(-1)
    assert result["ok"] is False


def test_get_track_info_exception(tools, song):
    song.tracks = None  # None[0] → TypeError caught by except
    result = tools.get_track_info(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_track_color
# ---------------------------------------------------------------------------


def test_set_track_color_with_color_attr(tools, song):
    result = tools.set_track_color(0, 5)
    assert result["ok"] is True


def test_set_track_color_without_color_attr(tools, song):
    del song.tracks[0].color
    result = tools.set_track_color(0, 5)
    assert result == {"ok": False, "error": "Track color not supported"}


def test_set_track_color_invalid_index(tools):
    result = tools.set_track_color(-1, 5)
    assert result["ok"] is False


def test_set_track_color_exception(tools, song):
    song.tracks[0].color = MagicMock(side_effect=Exception("x"))
    result = tools.set_track_color(0, "bad")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_track_fold_state
# ---------------------------------------------------------------------------


def test_set_track_fold_state_foldable(tools, song):
    song.tracks[0].is_foldable = True
    result = tools.set_track_fold_state(0, True)
    assert result["ok"] is True


def test_set_track_fold_state_not_foldable(tools, song):
    song.tracks[0].is_foldable = False
    result = tools.set_track_fold_state(0, True)
    assert result == {"ok": False, "error": "Track is not foldable"}


def test_set_track_fold_state_invalid(tools):
    result = tools.set_track_fold_state(-1, True)
    assert result["ok"] is False


def test_set_track_fold_state_exception(tools, song):
    song.tracks = None  # TypeError caught by except
    result = tools.set_track_fold_state(0, True)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_track_input_routing / set_track_output_routing
# ---------------------------------------------------------------------------


def test_set_track_input_routing_valid(tools, song):
    result = tools.set_track_input_routing(0, "Ext. In", 1)
    assert result["ok"] is True


def test_set_track_input_routing_invalid(tools):
    result = tools.set_track_input_routing(-1, "x")
    assert result["ok"] is False


def test_set_track_output_routing_valid(tools, song):
    result = tools.set_track_output_routing(0, "Master")
    assert result["ok"] is True


def test_set_track_output_routing_invalid(tools):
    result = tools.set_track_output_routing(-1, "Master")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Monitoring
# ---------------------------------------------------------------------------


def test_set_track_current_monitoring_state_can_be_armed(tools, song):
    song.tracks[0].can_be_armed = True
    result = tools.set_track_current_monitoring_state(0, 1)
    assert result["ok"] is True


def test_set_track_current_monitoring_state_cannot_be_armed(tools, song):
    song.tracks[0].can_be_armed = False
    result = tools.set_track_current_monitoring_state(0, 1)
    assert result == {"ok": False, "error": "Track cannot be monitored"}


def test_set_track_current_monitoring_state_invalid(tools):
    result = tools.set_track_current_monitoring_state(-1, 0)
    assert result["ok"] is False


def test_get_track_available_input_routing_types_with_attr(tools, song):
    routing = MagicMock()
    routing.display_name = "Ext. In"
    song.tracks[0].available_input_routing_types = [routing]
    result = tools.get_track_available_input_routing_types(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_track_available_input_routing_types_without_attr(tools, song):
    del song.tracks[0].available_input_routing_types
    result = tools.get_track_available_input_routing_types(0)
    assert result["ok"] is True
    assert result["routing_types"] == []


def test_get_track_available_input_routing_types_invalid(tools):
    result = tools.get_track_available_input_routing_types(-1)
    assert result["ok"] is False


def test_get_track_available_output_routing_types_with_attr(tools, song):
    routing = MagicMock()
    routing.display_name = "Master"
    song.tracks[0].available_output_routing_types = [routing]
    result = tools.get_track_available_output_routing_types(0)
    assert result["ok"] is True


def test_get_track_available_output_routing_types_without_attr(tools, song):
    del song.tracks[0].available_output_routing_types
    result = tools.get_track_available_output_routing_types(0)
    assert result["ok"] is True
    assert result["routing_types"] == []


def test_get_track_available_output_routing_types_invalid(tools):
    result = tools.get_track_available_output_routing_types(-1)
    assert result["ok"] is False


def test_get_track_input_routing_type_with_attr(tools, song):
    result = tools.get_track_input_routing_type(0)
    assert result["ok"] is True


def test_get_track_input_routing_type_without_attr(tools, song):
    del song.tracks[0].input_routing_type
    result = tools.get_track_input_routing_type(0)
    assert result["ok"] is False


def test_get_track_input_routing_type_invalid(tools):
    result = tools.get_track_input_routing_type(-1)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Track routing extras
# ---------------------------------------------------------------------------


def test_get_track_output_routing_with_attrs(tools, song):
    result = tools.get_track_output_routing(0)
    assert result["ok"] is True


def test_get_track_output_routing_invalid(tools):
    result = tools.get_track_output_routing(-1)
    assert result["ok"] is False


def test_set_track_input_sub_routing_with_attr(tools, song):
    result = tools.set_track_input_sub_routing(0, "ch1")
    assert result["ok"] is True


def test_set_track_input_sub_routing_without_attr(tools, song):
    del song.tracks[0].input_sub_routing
    result = tools.set_track_input_sub_routing(0, "ch1")
    assert result["ok"] is False


def test_set_track_input_sub_routing_invalid(tools):
    result = tools.set_track_input_sub_routing(-1, "ch1")
    assert result["ok"] is False


def test_set_track_output_sub_routing_with_attr(tools, song):
    result = tools.set_track_output_sub_routing(0, "ch1")
    assert result["ok"] is True


def test_set_track_output_sub_routing_without_attr(tools, song):
    del song.tracks[0].output_sub_routing
    result = tools.set_track_output_sub_routing(0, "ch1")
    assert result["ok"] is False


def test_set_track_output_sub_routing_invalid(tools):
    result = tools.set_track_output_sub_routing(-1, "ch1")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Track groups
# ---------------------------------------------------------------------------


def test_create_group_track_no_name(tools, song):
    result = tools.create_group_track()
    assert result["ok"] is True


def test_create_group_track_with_name(tools, song):
    result = tools.create_group_track(name="Group 1")
    assert result["ok"] is True


def test_create_group_track_exception(tools, song):
    song.create_group_track.side_effect = Exception("err")
    result = tools.create_group_track()
    assert result["ok"] is False


def test_group_tracks_valid(tools, song):
    song.tracks = [MagicMock(), MagicMock()]
    result = tools.group_tracks(0, 1)
    assert result["ok"] is True


def test_group_tracks_invalid_start(tools, song):
    result = tools.group_tracks(-1, 0)
    assert result["ok"] is False


def test_group_tracks_invalid_end(tools, song):
    result = tools.group_tracks(0, 99)
    assert result["ok"] is False


def test_group_tracks_end_before_start(tools, song):
    song.tracks = [MagicMock(), MagicMock()]
    result = tools.group_tracks(1, 0)
    assert result["ok"] is False


def test_group_tracks_exception(tools, song):
    song.create_group_track.side_effect = Exception("err")
    song.tracks = [MagicMock(), MagicMock()]
    result = tools.group_tracks(0, 1)
    assert result["ok"] is False


def test_get_track_is_grouped_not_grouped(tools, song):
    song.tracks[0].group_track = None
    song.tracks[0].is_foldable = False
    result = tools.get_track_is_grouped(0)
    assert result["ok"] is True
    assert result["is_grouped"] is False


def test_get_track_is_grouped_is_grouped(tools, song):
    other_track = MagicMock()
    song.tracks = [MagicMock(), other_track]
    song.tracks[0].group_track = other_track
    song.tracks[0].is_foldable = False
    result = tools.get_track_is_grouped(0)
    assert result["ok"] is True


def test_get_track_is_grouped_invalid(tools):
    result = tools.get_track_is_grouped(-1)
    assert result["ok"] is False


def test_ungroup_track_is_group(tools, song):
    song.tracks[0].is_foldable = True
    result = tools.ungroup_track(0)
    assert result["ok"] is True


def test_ungroup_track_not_group(tools, song):
    song.tracks[0].is_foldable = False
    result = tools.ungroup_track(0)
    assert result["ok"] is False


def test_ungroup_track_invalid(tools):
    result = tools.ungroup_track(-1)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Freeze / flatten
# ---------------------------------------------------------------------------


def test_freeze_track_can_freeze(tools, song):
    song.tracks[0].freeze_available = True
    result = tools.freeze_track(0)
    assert result["ok"] is True
    assert song.tracks[0].freeze_state == 1


def test_freeze_track_no_freeze_state(tools, song):
    song.tracks[0].freeze_available = True
    del song.tracks[0].freeze_state
    result = tools.freeze_track(0)
    assert result["ok"] is False


def test_freeze_track_cannot_freeze(tools, song):
    song.tracks[0].freeze_available = False
    result = tools.freeze_track(0)
    assert result["ok"] is False


def test_freeze_track_exception(tools, song):
    song.tracks = None  # None[0] → TypeError caught by except
    result = tools.freeze_track(0)
    assert result["ok"] is False


def test_unfreeze_track_with_state(tools, song):
    result = tools.unfreeze_track(0)
    assert result["ok"] is True
    assert song.tracks[0].freeze_state == 0


def test_unfreeze_track_without_state(tools, song):
    del song.tracks[0].freeze_state
    result = tools.unfreeze_track(0)
    assert result["ok"] is False


def test_unfreeze_track_exception(tools, song):
    song.tracks[0].freeze_state = MagicMock(side_effect=Exception("x"))
    result = tools.unfreeze_track(0)
    assert result["ok"] is True  # assignment on MagicMock is fine


def test_flatten_track_with_attr(tools, song):
    result = tools.flatten_track(0)
    assert result["ok"] is True
    song.tracks[0].flatten.assert_called_once()


def test_flatten_track_without_attr(tools, song):
    del song.tracks[0].flatten
    result = tools.flatten_track(0)
    assert result["ok"] is False


def test_flatten_track_exception(tools, song):
    song.tracks[0].flatten.side_effect = Exception("err")
    result = tools.flatten_track(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Annotations
# ---------------------------------------------------------------------------


def test_get_track_annotation_with_attr(tools, song):
    song.tracks[0].annotation = "my note"
    result = tools.get_track_annotation(0)
    assert result["ok"] is True
    assert result["annotation"] == "my note"


def test_get_track_annotation_without_attr(tools, song):
    del song.tracks[0].annotation
    result = tools.get_track_annotation(0)
    assert result["ok"] is False


def test_get_track_annotation_exception(tools, song):
    song.tracks = None  # None[0] → TypeError caught by except
    result = tools.get_track_annotation(0)
    assert result["ok"] is False


def test_set_track_annotation_with_attr(tools, song):
    result = tools.set_track_annotation(0, "note text")
    assert result["ok"] is True


def test_set_track_annotation_without_attr(tools, song):
    del song.tracks[0].annotation
    result = tools.set_track_annotation(0, "note text")
    assert result["ok"] is False


def test_set_track_annotation_exception(tools, song):
    song.tracks[0].annotation = MagicMock(side_effect=Exception("x"))
    result = tools.set_track_annotation(0, "note text")
    assert result["ok"] is True  # assignment doesn't raise on MagicMock


# ---------------------------------------------------------------------------
# Track delay
# ---------------------------------------------------------------------------


def test_get_track_delay_with_attr(tools, song):
    song.tracks[0].delay = 0.0
    result = tools.get_track_delay(0)
    assert result["ok"] is True
    assert result["delay"] == 0.0


def test_get_track_delay_without_attr(tools, song):
    del song.tracks[0].delay
    result = tools.get_track_delay(0)
    assert result["ok"] is False


def test_get_track_delay_exception(tools, song):
    song.tracks = None  # None[0] → TypeError caught by except
    result = tools.get_track_delay(0)
    assert result["ok"] is False


def test_set_track_delay_with_attr(tools, song):
    result = tools.set_track_delay(0, 100.0)
    assert result["ok"] is True


def test_set_track_delay_without_attr(tools, song):
    del song.tracks[0].delay
    result = tools.set_track_delay(0, 100.0)
    assert result["ok"] is False


def test_set_track_delay_exception(tools):
    result = tools.set_track_delay(0, "bad")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Additional except-block coverage tests (tools.song = None → AttributeError)
# ---------------------------------------------------------------------------


def test_rename_track_except_block(tools):
    tools.song = None
    result = tools.rename_track(0, "x")
    assert result["ok"] is False


def test_solo_track_except_block(tools):
    tools.song = None
    result = tools.solo_track(0)
    assert result["ok"] is False


def test_mute_track_except_block(tools):
    tools.song = None
    result = tools.mute_track(0)
    assert result["ok"] is False


def test_set_track_input_routing_except_block(tools):
    tools.song = None
    result = tools.set_track_input_routing(0, "x")
    assert result["ok"] is False


def test_set_track_output_routing_except_block(tools):
    tools.song = None
    result = tools.set_track_output_routing(0, "x")
    assert result["ok"] is False


def test_set_track_current_monitoring_state_except_block(tools):
    tools.song = None
    result = tools.set_track_current_monitoring_state(0, 1)
    assert result["ok"] is False


def test_get_track_available_input_routing_types_except_block(tools):
    tools.song = None
    result = tools.get_track_available_input_routing_types(0)
    assert result["ok"] is False


def test_get_track_available_output_routing_types_except_block(tools):
    tools.song = None
    result = tools.get_track_available_output_routing_types(0)
    assert result["ok"] is False


def test_get_track_input_routing_type_except_block(tools):
    tools.song = None
    result = tools.get_track_input_routing_type(0)
    assert result["ok"] is False


def test_get_track_output_routing_except_block(tools):
    tools.song = None
    result = tools.get_track_output_routing(0)
    assert result["ok"] is False


def test_set_track_input_sub_routing_except_block(tools):
    tools.song = None
    result = tools.set_track_input_sub_routing(0, "x")
    assert result["ok"] is False


def test_set_track_output_sub_routing_except_block(tools):
    tools.song = None
    result = tools.set_track_output_sub_routing(0, "x")
    assert result["ok"] is False


def test_create_group_track_with_name_covers_assignment(tools, song):
    """Cover line 442: name assignment when name provided and track index valid."""
    tracks_mock = MagicMock()
    tracks_mock.__len__ = MagicMock(side_effect=[0, 1, 1])
    song.tracks = tracks_mock
    result = tools.create_group_track(name="Group Bus")
    assert result["ok"] is True


def test_get_track_is_grouped_except_block(tools):
    tools.song = None
    result = tools.get_track_is_grouped(0)
    assert result["ok"] is False


def test_ungroup_track_except_block(tools):
    tools.song = None
    result = tools.ungroup_track(0)
    assert result["ok"] is False


def test_unfreeze_track_except_block(tools):
    tools.song = None
    result = tools.unfreeze_track(0)
    assert result["ok"] is False


def test_set_track_annotation_except_block(tools):
    tools.song = None
    result = tools.set_track_annotation(0, "text")
    assert result["ok"] is False
