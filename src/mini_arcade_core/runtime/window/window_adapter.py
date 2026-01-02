"""
Module providing runtime adapters for window and scene management.
"""

from __future__ import annotations

from mini_arcade_core.runtime.window.window_port import WindowPort


class WindowAdapter(WindowPort):
    """
    Manages multiple game windows (not implemented).
    """

    def __init__(self, backend):
        self.backend = backend

    def set_window_size(self, width, height):
        self.size = (width, height)
        self.backend.init(width, height)

    def set_title(self, title):
        self.backend.set_window_title(title)

    def set_clear_color(self, r, g, b):
        self.backend.set_clear_color(r, g, b)
        self.backend.set_clear_color(r, g, b)
