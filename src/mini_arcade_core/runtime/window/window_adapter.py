"""
Module providing runtime adapters for window and scene management.
"""

from __future__ import annotations

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.viewport import (
    Viewport,
    ViewportMode,
    ViewportState,
)
from mini_arcade_core.runtime.window.window_port import WindowPort
from mini_arcade_core.utils import logger


class WindowAdapter(WindowPort):
    """
    Manages multiple game windows (not implemented).
    """

    def __init__(self, backend: Backend):
        self.backend = backend

        self.backend.init()
        self._initialized = True
        self._viewport = Viewport(
            backend.window.width,
            backend.window.height,
            mode=ViewportMode.FIT,
        )

        # Cached current window size
        self.size = (backend.window.width, backend.window.height)
        self._viewport.resize(backend.window.width, backend.window.height)

    def set_virtual_resolution(self, width: int, height: int):
        self._viewport.set_virtual_resolution(int(width), int(height))
        # re-apply using current window size
        w, h = self.size
        self._viewport.resize(w, h)

    def set_viewport_mode(self, mode: ViewportMode):
        self._viewport.set_mode(mode)

    def get_viewport(self) -> ViewportState:
        return self._viewport.state

    def screen_to_virtual(self, x: float, y: float) -> tuple[float, float]:
        return self._viewport.screen_to_virtual(x, y)

    def set_title(self, title):
        self.backend.window.set_title(title)

    def set_clear_color(self, r, g, b):
        self.backend.render.set_clear_color(r, g, b)

    def on_window_resized(self, width: int, height: int):
        logger.debug(f"Window resized event: {width}x{height}")
        width = int(width)
        height = int(height)

        # Update cached size, but DO NOT call backend.resize_window here.
        self.size = (width, height)
        self.backend.window.width = width
        self.backend.window.height = height

        self._viewport.resize(width, height)

    def get_virtual_size(self) -> tuple[int, int]:
        s = self.get_viewport()
        return (s.virtual_w, s.virtual_h)
