"""
Clip quantization tools.

Single responsibility: MIDI clip quantization (grid and pitch).
"""


class ClipsQuantizeMixin:
    # ========================================================================
    # CLIP QUANTIZATION
    # ========================================================================

    def quantize_clip(self, track_index, clip_index, quantize_to):
        """Quantize MIDI clip to grid

        See Also:
            Wiki: docs/wiki/tools/quantize_clip.md"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, "quantize"):
                clip.quantize(float(quantize_to), 1.0)
                return {"ok": True, "message": "Clip quantized", "quantize_to": quantize_to}
            else:
                return {"ok": False, "error": "Clip does not support quantization"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def quantize_clip_pitch(self, track_index, clip_index, pitch=60):
        """Quantize MIDI clip pitch

        See Also:
            Wiki: docs/wiki/tools/quantize_clip_pitch.md"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, "quantize_pitch"):
                clip.quantize_pitch(int(pitch), int(pitch), 1.0)
                return {"ok": True, "message": "Clip pitch quantized", "pitch": pitch}
            else:
                return {"ok": False, "error": "Clip does not support pitch quantization"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
