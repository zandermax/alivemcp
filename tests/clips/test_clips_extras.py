"""
Tests for ClipsMixin follow action methods.
"""


def test_get_clip_follow_action_success(tools, song):
    clip = song.tracks[0].clip_slots[0].clip
    clip.follow_action_A = 1
    clip.follow_action_B = 0
    clip.follow_action_time = 4.0
    clip.follow_action_chance_A = 1.0
    clip.follow_action_chance_B = 0.0
    result = tools.get_clip_follow_action(0, 0)
    assert result["ok"] is True


def test_get_clip_follow_action_invalid_track(tools):
    result = tools.get_clip_follow_action(-1, 0)
    assert result["ok"] is False


def test_get_clip_follow_action_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_follow_action(0, 0)
    assert result["ok"] is False


def test_get_clip_follow_action_exception(tools, song):
    song.tracks = None
    result = tools.get_clip_follow_action(0, 0)
    assert result["ok"] is False


def test_set_clip_follow_action_success(tools, song):
    result = tools.set_clip_follow_action(0, 0, 3, 0, chance_A=0.8)
    assert result["ok"] is True


def test_set_clip_follow_action_invalid_track(tools):
    result = tools.set_clip_follow_action(-1, 0, 1, 0)
    assert result["ok"] is False


def test_set_clip_follow_action_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_follow_action(0, 0, 1, 0)
    assert result["ok"] is False


def test_set_clip_follow_action_exception(tools, song):
    song.tracks = None
    result = tools.set_clip_follow_action(0, 0, 1, 0)
    assert result["ok"] is False


def test_set_follow_action_time_with_attr(tools, song):
    result = tools.set_follow_action_time(0, 0, 2.0)
    assert result["ok"] is True


def test_set_follow_action_time_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.follow_action_time
    result = tools.set_follow_action_time(0, 0, 2.0)
    assert result["ok"] is False


def test_set_follow_action_time_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_follow_action_time(0, 0, 2.0)
    assert result["ok"] is False


def test_set_follow_action_time_invalid_track(tools):
    result = tools.set_follow_action_time(-1, 0, 2.0)
    assert result["ok"] is False


def test_get_clip_follow_action_invalid_clip(tools, song):
    result = tools.get_clip_follow_action(0, 99)
    assert result["ok"] is False


def test_set_clip_follow_action_invalid_clip(tools, song):
    result = tools.set_clip_follow_action(0, 99, 1, 2)
    assert result["ok"] is False


def test_set_follow_action_time_invalid_clip(tools, song):
    result = tools.set_follow_action_time(0, 99, 2.0)
    assert result["ok"] is False


def test_set_follow_action_time_except_block(tools):
    tools.song = None
    result = tools.set_follow_action_time(0, 0, 2.0)
    assert result["ok"] is False
