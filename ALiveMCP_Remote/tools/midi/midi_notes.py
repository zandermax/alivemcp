"""
MIDI notes aggregator module.

Composes smaller mixins to keep file sizes under the limit.
"""

from .midi_notes_operations import MidiNotesOperationsMixin
from .midi_notes_queries import MidiNotesQueriesMixin
from .midi_notes_selection import MidiNotesSelectionMixin


class MidiNotesMixin(MidiNotesOperationsMixin, MidiNotesSelectionMixin, MidiNotesQueriesMixin):
    """Aggregator combining MIDI notes operations, selection, and queries."""

    pass
