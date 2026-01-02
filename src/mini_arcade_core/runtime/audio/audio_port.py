"""
Service interfaces for runtime components.
"""

from __future__ import annotations


class AudioPort:
    """Interface for audio playback operations."""

    def play(self, sound_id: str):
        """
        Play the specified sound.

        :param sound_id: Identifier of the sound to play.
        :type sound_id: str
        """
