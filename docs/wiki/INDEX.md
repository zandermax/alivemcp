# ALiveMCP Wiki

This repository-hosted wiki documents the ALiveMCP tool surface and maps each tool to the Ableton Live API operations it performs. The source files live in `docs/wiki/` so they render on GitHub and are usable with Fossil.

Generated: 2026-05-13

## Quick links

- Tools inventory: [TOOLS_INDEX](TOOLS_INDEX.md)
- Template: [tool template](templates/tool.md)

---

## Taxonomy

Tools are organized along two axes: **operation type** and **domain object**.

| Symbol | Operation type | Meaning |
|--------|---------------|---------|
| 📖 | **Read** | Query or inspect state — non-mutating |
| ✏️ | **Write** | Create, set, modify — mutating |
| ⚠️ | **Destructive write** | Delete, clear, flatten, remove — irreversible without undo |
| ▶️ | **Transport** | Playback, recording, and timing control |
| 🖥️ | **View** | UI focus, panel visibility, window management |
| 🔀 | **Compound** | Spans multiple domains or combines read + write atomically |

Within each operation type, tools are grouped by domain: **Session**, **Tracks**, **Clips**, **MIDI**, **Devices**, **Automation**, **Mixing**, **Scenes**, **Arrangement**, **M4L**.

> **Duplicate note:** `add_notes`, `get_clip_notes`, and `remove_notes` appear in both Clips and MIDI sections with different paths; canonical paths are used below.

---

## 📖 Read

### Session

- [get_session_info](tools/session/get_session_info.md)
- [get_current_time](tools/session/get_current_time.md)
- [get_metronome_volume](tools/session/get_metronome_volume.md)
- [get_session_automation_record](tools/session/get_session_automation_record.md)
- [get_session_record](tools/session/get_session_record.md)
- [get_arrangement_overdub](tools/properties/get_arrangement_overdub.md)
- [get_signature_numerator](tools/properties/get_signature_numerator.md)
- [get_signature_denominator](tools/properties/get_signature_denominator.md)
- [get_loop_enabled](tools/arrangement/get_loop_enabled.md)
- [get_can_jump_to_next_cue](tools/arrangement/get_can_jump_to_next_cue.md)
- [get_can_jump_to_prev_cue](tools/arrangement/get_can_jump_to_prev_cue.md)
- [get_build_id](tools/properties/get_build_id.md)
- [get_variant](tools/properties/get_variant.md)
- [get_application_version](tools/properties/get_application_version.md)
- [get_project_root_folder](tools/arrangement/get_project_root_folder.md)

### Tracks

- [get_track_info](tools/tracks/get_track_info.md)
- [get_track_index_by_name](tools/tracks/get_track_index_by_name.md)
- [get_track_color](tools/tracks/get_track_color.md)
- [get_track_annotation](tools/tracks/get_track_annotation.md)
- [get_track_delay](tools/tracks/get_track_delay.md)
- [get_track_is_foldable](tools/properties/get_track_is_foldable.md)
- [get_track_is_frozen](tools/properties/get_track_is_frozen.md)
- [get_track_is_grouped](tools/tracks/get_track_is_grouped.md)
- [get_track_chain_summary](tools/tracks/get_track_chain_summary.md)
- [get_track_available_input_routing_types](tools/tracks/get_track_available_input_routing_types.md)
- [get_track_available_output_routing_types](tools/tracks/get_track_available_output_routing_types.md)
- [get_track_input_routing_type](tools/tracks/get_track_input_routing_type.md)
- [get_track_output_routing](tools/tracks/get_track_output_routing.md)

### Clips

- [get_clip_info](tools/clips/get_clip_info.md)
- [get_clip_notes](tools/clips/get_clip_notes.md)
- [get_clip_annotation](tools/clips/get_clip_annotation.md)
- [get_clip_color](tools/clips/get_clip_color.md)
- [get_clip_fade_in](tools/clips/get_clip_fade_in.md)
- [get_clip_fade_out](tools/clips/get_clip_fade_out.md)
- [get_clip_ram_mode](tools/clips/get_clip_ram_mode.md)
- [get_clip_follow_action](tools/clips/get_clip_follow_action.md)
- [get_clip_start_time](tools/properties/get_clip_start_time.md)
- [get_arrangement_clips](tools/arrangement/get_arrangement_clips.md)
- [get_locators](tools/arrangement/get_locators.md)
- [get_take_lanes](tools/arrangement/get_take_lanes.md)
- [get_take_lane_name](tools/arrangement/get_take_lane_name.md)
- [get_clips_in_take_lane](tools/arrangement/get_clips_in_take_lane.md)

### MIDI

- [get_clip_notes](tools/midi/get_clip_notes.md) *(see also: Clips)*
- [get_notes_extended](tools/midi/get_notes_extended.md)

### Devices

- [get_track_devices](tools/devices/get_track_devices.md)
- [get_device_parameters](tools/devices/get_device_parameters.md)
- [get_device_parameter_by_name](tools/devices/get_device_parameter_by_name.md)
- [get_device_presets](tools/devices/get_device_presets.md)
- [get_device_chains](tools/devices/get_device_chains.md)
- [get_chain_devices](tools/devices/get_chain_devices.md)
- [get_device_class_name](tools/devices/get_device_class_name.md)
- [get_device_type](tools/devices/get_device_type.md)
- [get_rack_contents](tools/devices/get_rack_contents.md)
- [get_track_device_params](tools/tracks/get_track_device_params.md)
- [browse_devices](tools/arrangement/browse_devices.md)
- [browse_plugins](tools/arrangement/browse_plugins.md)
- [get_browser_items](tools/arrangement/get_browser_items.md)

### Automation

- [get_clip_automation_envelope](tools/automation/get_clip_automation_envelope.md)
- [get_automation_envelope_values](tools/automation/get_automation_envelope_values.md)

### Mixing

- [get_track_sends](tools/mixing/get_track_sends.md)
- [get_master_track_info](tools/mixing/get_master_track_info.md)
- [get_master_devices](tools/mixing/get_master_devices.md)
- [get_master_device_params](tools/mixing/get_master_device_params.md)
- [get_master_device_param_info](tools/mixing/get_master_device_param_info.md)
- [get_master_chain_summary](tools/mixing/get_master_chain_summary.md)
- [get_return_track_count](tools/mixing/get_return_track_count.md)
- [get_return_track_info](tools/mixing/get_return_track_info.md)
- [get_crossfader_assignment](tools/mixing/get_crossfader_assignment.md)
- [get_crossfader_position](tools/mixing/get_crossfader_position.md)
- [get_groove_amount](tools/mixing/get_groove_amount.md)
- [get_groove_pool_grooves](tools/mixing/get_groove_pool_grooves.md)

### Scenes

- [get_scene_info](tools/scenes/get_scene_info.md)
- [get_scene_color](tools/scenes/get_scene_color.md)
- [get_scene_is_empty](tools/properties/get_scene_is_empty.md)
- [get_scene_tempo](tools/properties/get_scene_tempo.md)

### Max for Live (M4L)

- [is_max_device](tools/m4l/is_max_device.md)
- [get_m4l_devices](tools/m4l/get_m4l_devices.md)
- [get_m4l_param_by_name](tools/m4l/get_m4l_param_by_name.md)
- [get_cv_tools_devices](tools/m4l/get_cv_tools_devices.md)

---

## ✏️ Write

### Session

- [set_tempo](tools/session/set_tempo.md)
- [set_time_signature](tools/session/set_time_signature.md)
- [set_loop_start](tools/session/set_loop_start.md)
- [set_loop_length](tools/session/set_loop_length.md)
- [set_loop_enabled](tools/arrangement/set_loop_enabled.md)
- [set_metronome](tools/session/set_metronome.md)
- [set_metronome_volume](tools/session/set_metronome_volume.md)
- [set_record_mode](tools/properties/set_record_mode.md)
- [set_arrangement_overdub](tools/session/set_arrangement_overdub.md)
- [set_session_automation_record](tools/session/set_session_automation_record.md)
- [set_session_record](tools/session/set_session_record.md)
- [set_back_to_arranger](tools/session/set_back_to_arranger.md)
- [set_punch_in](tools/session/set_punch_in.md)
- [set_punch_out](tools/session/set_punch_out.md)
- [re_enable_automation](tools/session/re_enable_automation.md)
- [undo](tools/session/undo.md)
- [redo](tools/session/redo.md)

### Tracks

- [create_midi_track](tools/tracks/create_midi_track.md)
- [create_audio_track](tools/tracks/create_audio_track.md)
- [create_return_track](tools/tracks/create_return_track.md)
- [create_group_track](tools/tracks/create_group_track.md)
- [duplicate_track](tools/tracks/duplicate_track.md)
- [rename_track](tools/tracks/rename_track.md)
- [set_track_volume](tools/tracks/set_track_volume.md)
- [set_track_pan](tools/tracks/set_track_pan.md)
- [set_track_color](tools/tracks/set_track_color.md)
- [set_track_annotation](tools/tracks/set_track_annotation.md)
- [set_track_delay](tools/tracks/set_track_delay.md)
- [set_track_fold_state](tools/tracks/set_track_fold_state.md)
- [set_track_input_routing](tools/tracks/set_track_input_routing.md)
- [set_track_output_routing](tools/tracks/set_track_output_routing.md)
- [set_track_input_sub_routing](tools/tracks/set_track_input_sub_routing.md)
- [set_track_output_sub_routing](tools/tracks/set_track_output_sub_routing.md)
- [set_track_current_monitoring_state](tools/tracks/set_track_current_monitoring_state.md)
- [set_track_device_param](tools/tracks/set_track_device_param.md)
- [set_track_device_param_by_name](tools/tracks/set_track_device_param_by_name.md)
- [arm_track](tools/tracks/arm_track.md)
- [solo_track](tools/tracks/solo_track.md)
- [mute_track](tools/tracks/mute_track.md)
- [group_tracks](tools/tracks/group_tracks.md)
- [ungroup_track](tools/tracks/ungroup_track.md)
- [freeze_track](tools/tracks/freeze_track.md)
- [unfreeze_track](tools/tracks/unfreeze_track.md)

### Clips

- [create_midi_clip](tools/clips/create_midi_clip.md)
- [duplicate_clip](tools/clips/duplicate_clip.md)
- [set_clip_name](tools/clips/set_clip_name.md)
- [set_clip_annotation](tools/clips/set_clip_annotation.md)
- [set_clip_color](tools/clips/set_clip_color.md)
- [set_clip_muted](tools/clips/set_clip_muted.md)
- [set_clip_gain](tools/clips/set_clip_gain.md)
- [set_clip_pitch_coarse](tools/clips/set_clip_pitch_coarse.md)
- [set_clip_pitch_fine](tools/clips/set_clip_pitch_fine.md)
- [set_clip_looping](tools/clips/set_clip_looping.md)
- [set_clip_loop_start](tools/clips/set_clip_loop_start.md)
- [set_clip_loop_end](tools/clips/set_clip_loop_end.md)
- [set_clip_start_marker](tools/clips/set_clip_start_marker.md)
- [set_clip_end_marker](tools/clips/set_clip_end_marker.md)
- [set_clip_start_time](tools/properties/set_clip_start_time.md)
- [set_clip_fade_in](tools/clips/set_clip_fade_in.md)
- [set_clip_fade_out](tools/clips/set_clip_fade_out.md)
- [set_clip_ram_mode](tools/clips/set_clip_ram_mode.md)
- [set_clip_follow_action](tools/clips/set_clip_follow_action.md)
- [set_follow_action_time](tools/clips/set_follow_action_time.md)
- [set_clip_signature_numerator](tools/clips/set_clip_signature_numerator.md)
- [quantize_clip](tools/clips/quantize_clip.md)
- [quantize_clip_pitch](tools/clips/quantize_clip_pitch.md)
- [set_clip_groove](tools/mixing/set_clip_groove.md)
- [set_clip_groove_amount](tools/mixing/set_clip_groove_amount.md)
- [get_clip_annotation](tools/clips/get_clip_annotation.md)
- [set_clip_annotation](tools/clips/set_clip_annotation.md)
- [create_locator](tools/arrangement/create_locator.md)
- [create_take_lane](tools/arrangement/create_take_lane.md)
- [set_take_lane_name](tools/arrangement/set_take_lane_name.md)
- [create_audio_clip_in_lane](tools/arrangement/create_audio_clip_in_lane.md)
- [create_midi_clip_in_lane](tools/arrangement/create_midi_clip_in_lane.md)

### MIDI

- [add_notes](tools/clips/add_notes.md)
- [remove_notes](tools/midi/remove_notes.md) *(see also: Clips)*
- [select_all_notes](tools/midi/select_all_notes.md)
- [deselect_all_notes](tools/midi/deselect_all_notes.md)
- [replace_selected_notes](tools/midi/replace_selected_notes.md)
- [send_midi_cc](tools/midi/send_midi_cc.md)
- [send_program_change](tools/midi/send_program_change.md)

### Devices

- [add_device](tools/devices/add_device.md)
- [load_device_from_browser](tools/arrangement/load_device_from_browser.md)
- [set_device_param](tools/devices/set_device_param.md) *(possible alias — see note above)*
- [set_device_on_off](tools/devices/set_device_on_off.md)
- [set_device_parameter_by_name](tools/devices/set_device_parameter_by_name.md)

- [set_device_preset](tools/devices/set_device_preset.md)
- [randomize_device_parameters](tools/devices/randomize_device_parameters.md)
- [randomize_device](tools/devices/randomize_device.md)
- [set_chain_mute](tools/devices/set_chain_mute.md)
- [set_chain_solo](tools/devices/set_chain_solo.md)
- [set_master_device_param](tools/mixing/set_master_device_param.md)
- [set_master_device_param_by_name](tools/mixing/set_master_device_param_by_name.md)

### Automation

- [create_automation_envelope](tools/automation/create_automation_envelope.md)
- [insert_automation_step](tools/automation/insert_automation_step.md)
- [remove_automation_step](tools/automation/remove_automation_step.md)

### Mixing

- [set_track_send](tools/mixing/set_track_send.md)
- [set_master_volume](tools/mixing/set_master_volume.md)
- [set_master_pan](tools/mixing/set_master_pan.md)
- [set_return_track_volume](tools/mixing/set_return_track_volume.md)
- [set_crossfader_assignment](tools/mixing/set_crossfader_assignment.md)
- [set_groove_amount](tools/mixing/set_groove_amount.md)

### Scenes

- [create_scene](tools/scenes/create_scene.md)
- [duplicate_scene](tools/scenes/duplicate_scene.md)
- [rename_scene](tools/scenes/rename_scene.md)
- [set_scene_color](tools/scenes/set_scene_color.md)

---

## ⚠️ Destructive Write

> These operations delete or irreversibly transform data. Most can be undone via [`undo`](tools/session/undo.md) within the same session, but verify before scripting in bulk.

### Tracks

- [delete_track](tools/tracks/delete_track.md)
- [flatten_track](tools/tracks/flatten_track.md)

### Clips

- [delete_clip](tools/clips/delete_clip.md)
- [delete_locator](tools/arrangement/delete_locator.md)
- [delete_take_lane](tools/arrangement/delete_take_lane.md)

### MIDI

- [remove_notes](tools/midi/remove_notes.md)

### Devices

- [delete_device](tools/devices/delete_device.md)

### Automation

- [clear_automation_envelope](tools/automation/clear_automation_envelope.md)

### Scenes

- [delete_scene](tools/scenes/delete_scene.md)

---

## ▶️ Transport

> Controls playback, recording, navigation, and timing. These affect the Live transport state but do not modify project data.

### Playback & Recording

- [start_playback](tools/session/start_playback.md)
- [stop_playback](tools/session/stop_playback.md)
- [continue_playing](tools/session/continue_playing.md)
- [start_recording](tools/session/start_recording.md)
- [stop_recording](tools/session/stop_recording.md)
- [trigger_session_record](tools/arrangement/trigger_session_record.md)
- [tap_tempo](tools/session/tap_tempo.md)
- [nudge_up](tools/session/nudge_up.md)
- [nudge_down](tools/session/nudge_down.md)

### Clips & Scenes

- [launch_clip](tools/clips/launch_clip.md)
- [stop_clip](tools/clips/stop_clip.md)
- [stop_all_clips](tools/clips/stop_all_clips.md)
- [launch_scene](tools/scenes/launch_scene.md)

### Navigation

- [jump_to_time](tools/session/jump_to_time.md)
- [jump_by_amount](tools/arrangement/jump_by_amount.md)
- [jump_to_next_cue](tools/arrangement/jump_to_next_cue.md)
- [jump_to_prev_cue](tools/arrangement/jump_to_prev_cue.md)

---

## 🖥️ View

> Affects what is visible or focused in the Live UI. No audio or project data is modified.

- [show_clip_view](tools/arrangement/show_clip_view.md)
- [show_arrangement_view](tools/arrangement/show_arrangement_view.md)
- [focus_track](tools/arrangement/focus_track.md)
- [scroll_view_to_time](tools/arrangement/scroll_view_to_time.md)
- [show_plugin_window](tools/devices/show_plugin_window.md)
- [hide_plugin_window](tools/devices/hide_plugin_window.md)
- [show_message_box](tools/properties/show_message_box.md)

---

## 🔀 Compound

> These operations span multiple domains or combine read + write in a single atomic step. Use with care in scripted pipelines — they may have side effects across clip, track, and arrangement state simultaneously.

- [capture_midi](tools/session/capture_midi.md) — captures MIDI played since last transport event into a new clip
- [consolidate_clip](tools/arrangement/consolidate_clip.md) — renders a region of the arrangement into a new audio clip
- [duplicate_to_arrangement](tools/arrangement/duplicate_to_arrangement.md) — copies a session clip into the arrangement view at the current playhead
- [flatten_track](tools/tracks/flatten_track.md) — renders a track's device chain to audio in place *(also listed under ⚠️ Destructive)*
- [quantize_clip](tools/clips/quantize_clip.md) — reads note data and writes it back time-corrected *(also listed under ✏️ Write › Clips)*
- [quantize_clip_pitch](tools/clips/quantize_clip_pitch.md) — reads pitch data and writes it back corrected *(also listed under ✏️ Write › Clips)*
- [randomize_device](tools/devices/randomize_device.md) — reads current param ranges and writes randomized values
- [randomize_device_parameters](tools/devices/randomize_device_parameters.md) — as above, scoped to a parameter subset

---

## How to contribute

1. Add or update a page under `docs/wiki/tools/<domain>/` using [tool template](templates/tool.md).
2. Commit and open a PR; include Live version notes if behavior depends on Live 11 vs Live 12.

## Fossil/GitHub compatibility

Keep content in the `docs/wiki/` tree (plain Markdown). Avoid GitHub-only wiki features.
