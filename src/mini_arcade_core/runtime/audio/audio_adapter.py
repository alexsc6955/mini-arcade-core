"""
Module providing runtime adapters for window and scene management.
"""

from __future__ import annotations

from mini_arcade_core.runtime.audio.audio_port import AudioPort


class NullAudioAdapter(AudioPort):
    """A no-op audio adapter."""

    def play(self, sound_id: str): ...
