"""
Tests for ArrangementMixin core arrangement/session operations.
"""


def test_get_project_root_folder_with_attr(tools, song):
    song.project_root_folder = "/path/to/project"
    result = tools.get_project_root_folder()
    assert result["ok"] is True
    assert result["project_root_folder"] == "/path/to/project"


def test_get_project_root_folder_none(tools, song):
    song.project_root_folder = None
    result = tools.get_project_root_folder()
    assert result["ok"] is True
    assert result["project_root_folder"] is None


def test_get_project_root_folder_without_attr(tools, song):
    del song.project_root_folder
    result = tools.get_project_root_folder()
    assert result["ok"] is False


def test_get_project_root_folder_exception(tools, song):
    tools.song = None
    result = tools.get_project_root_folder()
    assert result["ok"] is False


def test_trigger_session_record_no_length(tools, song):
    result = tools.trigger_session_record()
    assert result["ok"] is True
    song.trigger_session_record.assert_called_once_with()


def test_trigger_session_record_with_length(tools, song):
    result = tools.trigger_session_record(length=4.0)
    assert result["ok"] is True
    song.trigger_session_record.assert_called_once_with(4.0)


def test_trigger_session_record_exception(tools, song):
    song.trigger_session_record.side_effect = Exception("err")
    result = tools.trigger_session_record()
    assert result["ok"] is False


def test_get_can_jump_to_next_cue(tools, song):
    song.can_jump_to_next_cue = True
    result = tools.get_can_jump_to_next_cue()
    assert result["ok"] is True
    assert result["can_jump_to_next_cue"] is True


def test_get_can_jump_to_next_cue_exception(tools, song):
    tools.song = None
    result = tools.get_can_jump_to_next_cue()
    assert result["ok"] is False


def test_get_can_jump_to_prev_cue(tools, song):
    song.can_jump_to_prev_cue = False
    result = tools.get_can_jump_to_prev_cue()
    assert result["ok"] is True
    assert result["can_jump_to_prev_cue"] is False


def test_get_can_jump_to_prev_cue_exception(tools, song):
    tools.song = None
    result = tools.get_can_jump_to_prev_cue()
    assert result["ok"] is False


def test_jump_to_next_cue_can_jump(tools, song):
    song.can_jump_to_next_cue = True
    result = tools.jump_to_next_cue()
    assert result["ok"] is True
    song.jump_to_next_cue.assert_called_once()


def test_jump_to_next_cue_cannot_jump(tools, song):
    song.can_jump_to_next_cue = False
    result = tools.jump_to_next_cue()
    assert result == {"ok": False, "error": "Cannot jump to next cue"}


def test_jump_to_next_cue_exception(tools, song):
    song.can_jump_to_next_cue = True
    song.jump_to_next_cue.side_effect = Exception("err")
    result = tools.jump_to_next_cue()
    assert result["ok"] is False


def test_jump_to_prev_cue_can_jump(tools, song):
    song.can_jump_to_prev_cue = True
    result = tools.jump_to_prev_cue()
    assert result["ok"] is True
    song.jump_to_prev_cue.assert_called_once()


def test_jump_to_prev_cue_cannot_jump(tools, song):
    song.can_jump_to_prev_cue = False
    result = tools.jump_to_prev_cue()
    assert result == {"ok": False, "error": "Cannot jump to previous cue"}


def test_jump_to_prev_cue_exception(tools, song):
    song.can_jump_to_prev_cue = True
    song.jump_to_prev_cue.side_effect = Exception("err")
    result = tools.jump_to_prev_cue()
    assert result["ok"] is False


def test_get_arrangement_clips_with_attr(tools, song):
    clip = song.tracks[0].arrangement_clips[0]
    clip.name = "Clip 1"
    clip.start_time = 0.0
    clip.end_time = 4.0
    clip.length = 4.0
    result = tools.get_arrangement_clips(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_arrangement_clips_without_attr(tools, song):
    del song.tracks[0].arrangement_clips
    result = tools.get_arrangement_clips(0)
    assert result["ok"] is False


def test_get_arrangement_clips_exception(tools, song):
    song.tracks = None
    result = tools.get_arrangement_clips(0)
    assert result["ok"] is False


def test_duplicate_to_arrangement_with_dup_loop(tools, song):
    result = tools.duplicate_to_arrangement(0, 0)
    assert result["ok"] is True
    song.tracks[0].clip_slots[0].clip.duplicate_loop.assert_called_once()


def test_duplicate_to_arrangement_without_dup_loop(tools, song):
    del song.tracks[0].clip_slots[0].clip.duplicate_loop
    result = tools.duplicate_to_arrangement(0, 0)
    assert result["ok"] is False


def test_duplicate_to_arrangement_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.duplicate_to_arrangement(0, 0)
    assert result["ok"] is False


def test_duplicate_to_arrangement_exception(tools, song):
    song.tracks[0].clip_slots[0].clip.duplicate_loop.side_effect = Exception("err")
    result = tools.duplicate_to_arrangement(0, 0)
    assert result["ok"] is False


def test_consolidate_clip_success(tools):
    result = tools.consolidate_clip(0, 0.0, 8.0)
    assert result["ok"] is True
    assert result["start_time"] == 0.0
    assert result["end_time"] == 8.0


def test_consolidate_clip_exception(tools):
    result = tools.consolidate_clip(0, "bad", 8.0)
    assert result["ok"] is False
