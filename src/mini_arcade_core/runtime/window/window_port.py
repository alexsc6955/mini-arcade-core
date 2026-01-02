"""
Service interfaces for runtime components.
"""

from __future__ import annotations

from mini_arcade_core.backend import Backend


class WindowPort:
    """Interface for window-related operations."""

    backend: Backend
    size: tuple[int, int]

    def set_window_size(self, width: int, height: int):
        """
        Set the size of the window.

        :param width: Width in pixels.
        :type width: int

        :param height: Height in pixels.
        :type height: int
        """

    def set_title(self, title: str):
        """
        Set the window title.

        :param title: The new title for the window.
        :type title: str
        """

    def set_clear_color(self, r: int, g: int, b: int):
        """
        Set the clear color for the window.

        :param r: Red component (0-255).
        :type r: int

        :param g: Green component (0-255).
        :type g: int

        :param b: Blue component (0-255).
        :type b: int
        """
