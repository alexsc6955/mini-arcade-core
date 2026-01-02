"""
Service interfaces for runtime components.
"""

from __future__ import annotations

from mini_arcade_core.backend import Backend


class CapturePort:
    """Interface for frame capture operations."""

    backend: Backend

    def screenshot(self, label: str | None = None) -> str:
        """
        Capture the current frame.

        :param label: Optional label for the screenshot file.
        :type label: str | None

        :return: Screenshot file path.
        :rtype: str
        """

    def screenshot_bytes(self) -> bytes | None:
        """
        Capture the current frame and return it as bytes.

        :return: Screenshot data as bytes.
        :rtype: bytes | None
        """
