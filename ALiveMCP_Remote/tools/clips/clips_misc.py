"""
Misc clip property setters: muted, gain, pitch, signature.
"""


class ClipsMiscMixin:
    # ========================================================================
    # CLIP MISC PROPERTIES
    # ========================================================================

    def set_clip_muted(self, track_index, clip_index, muted):
        """Mute or unmute clip

        See Also:
            Wiki: docs/wiki/tools/set_clip_muted.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.muted = bool(muted)
            return {"ok": True, "muted": clip.muted}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_gain(self, track_index, clip_index, gain):
        """Set clip gain/volume

        See Also:
            Wiki: docs/wiki/tools/set_clip_gain.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, "gain"):
                clip.gain = float(gain)
                return {"ok": True, "gain": float(clip.gain)}
            else:
                return {"ok": False, "error": "Clip does not support gain"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_pitch_coarse(self, track_index, clip_index, semitones):
        """Transpose clip by semitones

        See Also:
            Wiki: docs/wiki/tools/set_clip_pitch_coarse.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, "pitch_coarse"):
                clip.pitch_coarse = int(semitones)
                return {"ok": True, "pitch_coarse": clip.pitch_coarse}
            else:
                return {"ok": False, "error": "Clip does not support pitch adjustment"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_pitch_fine(self, track_index, clip_index, cents):
        """Fine-tune clip pitch in cents

        See Also:
            Wiki: docs/wiki/tools/set_clip_pitch_fine.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if hasattr(clip, "pitch_fine"):
                clip.pitch_fine = int(cents)
                return {"ok": True, "pitch_fine": clip.pitch_fine}
            else:
                return {"ok": False, "error": "Clip does not support fine pitch adjustment"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_signature_numerator(self, track_index, clip_index, numerator):
        """Set clip time signature numerator

        See Also:
            Wiki: docs/wiki/tools/set_clip_signature_numerator.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.signature_numerator = int(numerator)
            return {"ok": True, "signature_numerator": clip.signature_numerator}
        except Exception as e:
            return {"ok": False, "error": str(e)}
