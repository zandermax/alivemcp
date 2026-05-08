"""
Tests for ClipsMixin annotation, fades, RAM, and pitch/signature edge cases.
"""


def test_get_clip_annotation_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.annotation = "hello"
    result = tools.get_clip_annotation(0, 0)
    assert result["ok"] is True
    assert result["annotation"] == "hello"


def test_get_clip_annotation_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.annotation
    result = tools.get_clip_annotation(0, 0)
    assert result["ok"] is False


def test_get_clip_annotation_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_annotation(0, 0)
    assert result["ok"] is False


def test_set_clip_annotation_with_attr(tools, song):
    result = tools.set_clip_annotation(0, 0, "note")
    assert result["ok"] is True


def test_set_clip_annotation_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.annotation
    result = tools.set_clip_annotation(0, 0, "note")
    assert result["ok"] is False


def test_set_clip_annotation_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_annotation(0, 0, "note")
    assert result["ok"] is False


def test_get_clip_fade_in_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.fade_in_time = 1.0
    result = tools.get_clip_fade_in(0, 0)
    assert result["ok"] is True
    assert result["fade_in_time"] == 1.0


def test_get_clip_fade_in_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.fade_in_time
    result = tools.get_clip_fade_in(0, 0)
    assert result["ok"] is False


def test_get_clip_fade_in_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_fade_in(0, 0)
    assert result["ok"] is False


def test_set_clip_fade_in_with_attr(tools, song):
    result = tools.set_clip_fade_in(0, 0, 0.5)
    assert result["ok"] is True


def test_set_clip_fade_in_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.fade_in_time
    result = tools.set_clip_fade_in(0, 0, 0.5)
    assert result["ok"] is False


def test_set_clip_fade_in_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_fade_in(0, 0, 0.5)
    assert result["ok"] is False


def test_get_clip_fade_out_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.fade_out_time = 2.0
    result = tools.get_clip_fade_out(0, 0)
    assert result["ok"] is True
    assert result["fade_out_time"] == 2.0


def test_get_clip_fade_out_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.fade_out_time
    result = tools.get_clip_fade_out(0, 0)
    assert result["ok"] is False


def test_get_clip_fade_out_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_fade_out(0, 0)
    assert result["ok"] is False


def test_set_clip_fade_out_with_attr(tools, song):
    result = tools.set_clip_fade_out(0, 0, 1.0)
    assert result["ok"] is True


def test_set_clip_fade_out_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.fade_out_time
    result = tools.set_clip_fade_out(0, 0, 1.0)
    assert result["ok"] is False


def test_set_clip_fade_out_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_fade_out(0, 0, 1.0)
    assert result["ok"] is False


def test_get_clip_ram_mode_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.ram_mode = True
    result = tools.get_clip_ram_mode(0, 0)
    assert result["ok"] is True
    assert result["ram_mode"] is True


def test_get_clip_ram_mode_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.ram_mode
    result = tools.get_clip_ram_mode(0, 0)
    assert result["ok"] is False


def test_get_clip_ram_mode_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_ram_mode(0, 0)
    assert result["ok"] is False


def test_set_clip_ram_mode_with_attr(tools, song):
    result = tools.set_clip_ram_mode(0, 0, True)
    assert result["ok"] is True


def test_set_clip_ram_mode_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.ram_mode
    result = tools.set_clip_ram_mode(0, 0, True)
    assert result["ok"] is False


def test_set_clip_ram_mode_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_ram_mode(0, 0, True)
    assert result["ok"] is False


def test_get_clip_annotation_except_block(tools):
    tools.song = None
    result = tools.get_clip_annotation(0, 0)
    assert result["ok"] is False


def test_set_clip_annotation_except_block(tools):
    tools.song = None
    result = tools.set_clip_annotation(0, 0, "x")
    assert result["ok"] is False


def test_get_clip_fade_in_except_block(tools):
    tools.song = None
    result = tools.get_clip_fade_in(0, 0)
    assert result["ok"] is False


def test_set_clip_fade_in_except_block(tools):
    tools.song = None
    result = tools.set_clip_fade_in(0, 0, 0.1)
    assert result["ok"] is False


def test_get_clip_fade_out_except_block(tools):
    tools.song = None
    result = tools.get_clip_fade_out(0, 0)
    assert result["ok"] is False


def test_set_clip_fade_out_except_block(tools):
    tools.song = None
    result = tools.set_clip_fade_out(0, 0, 0.1)
    assert result["ok"] is False


def test_get_clip_ram_mode_except_block(tools):
    tools.song = None
    result = tools.get_clip_ram_mode(0, 0)
    assert result["ok"] is False


def test_set_clip_ram_mode_except_block(tools):
    tools.song = None
    result = tools.set_clip_ram_mode(0, 0, True)
    assert result["ok"] is False


def test_set_clip_pitch_coarse_invalid_track(tools):
    result = tools.set_clip_pitch_coarse(-1, 0, 3)
    assert result["ok"] is False


def test_set_clip_pitch_coarse_invalid_clip(tools, song):
    result = tools.set_clip_pitch_coarse(0, 99, 3)
    assert result["ok"] is False


def test_set_clip_pitch_coarse_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_pitch_coarse(0, 0, 3)
    assert result["ok"] is False


def test_set_clip_pitch_coarse_except_block(tools):
    tools.song = None
    result = tools.set_clip_pitch_coarse(0, 0, 3)
    assert result["ok"] is False


def test_set_clip_pitch_fine_invalid_track(tools):
    result = tools.set_clip_pitch_fine(-1, 0, 50)
    assert result["ok"] is False


def test_set_clip_pitch_fine_invalid_clip(tools, song):
    result = tools.set_clip_pitch_fine(0, 99, 50)
    assert result["ok"] is False


def test_set_clip_pitch_fine_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_pitch_fine(0, 0, 50)
    assert result["ok"] is False


def test_set_clip_pitch_fine_except_block(tools):
    tools.song = None
    result = tools.set_clip_pitch_fine(0, 0, 50)
    assert result["ok"] is False


def test_set_clip_signature_numerator_invalid_track(tools):
    result = tools.set_clip_signature_numerator(-1, 0, 4)
    assert result["ok"] is False


def test_set_clip_signature_numerator_invalid_clip(tools, song):
    result = tools.set_clip_signature_numerator(0, 99, 4)
    assert result["ok"] is False


def test_set_clip_signature_numerator_except_block(tools):
    tools.song = None
    result = tools.set_clip_signature_numerator(0, 0, 4)
    assert result["ok"] is False


def test_set_clip_color_except_block(tools):
    tools.song = None
    result = tools.set_clip_color(0, 0, 5)
    assert result["ok"] is False
