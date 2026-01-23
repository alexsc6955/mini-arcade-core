from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from mini_arcade_core.utils import logger


class ViewportMode(str, Enum):
    FIT = "fit"  # letterbox
    FILL = "fill"  # crop


@dataclass(frozen=True)
class ViewportState:
    virtual_w: int
    virtual_h: int

    window_w: int
    window_h: int

    mode: ViewportMode
    scale: float

    # viewport rect in screen pixels where the virtual canvas lands
    # (can be larger than window in FILL mode -> offsets can be negative)
    viewport_w: int
    viewport_h: int
    offset_x: int
    offset_y: int


class Viewport:
    def __init__(
        self,
        virtual_w: int,
        virtual_h: int,
        mode: ViewportMode = ViewportMode.FIT,
    ):
        self._virtual_w = int(virtual_w)
        self._virtual_h = int(virtual_h)
        self._mode = mode
        self._state: ViewportState | None = None

    def set_virtual_resolution(self, w: int, h: int):
        self._virtual_w = int(w)
        self._virtual_h = int(h)
        if self._state:
            self.resize(self._state.window_w, self._state.window_h)

    def set_mode(self, mode: ViewportMode):
        self._mode = mode
        if self._state:
            self.resize(self._state.window_w, self._state.window_h)

    def resize(self, window_w: int, window_h: int):
        window_w = int(window_w)
        window_h = int(window_h)

        sx = window_w / self._virtual_w
        sy = window_h / self._virtual_h
        scale = min(sx, sy) if self._mode == ViewportMode.FIT else max(sx, sy)

        vw = int(round(self._virtual_w * scale))
        vh = int(round(self._virtual_h * scale))
        ox = int(round((window_w - vw) / 2))
        oy = int(round((window_h - vh) / 2))

        self._state = ViewportState(
            virtual_w=self._virtual_w,
            virtual_h=self._virtual_h,
            window_w=window_w,
            window_h=window_h,
            mode=self._mode,
            scale=float(scale),
            viewport_w=vw,
            viewport_h=vh,
            offset_x=ox,
            offset_y=oy,
        )
        logger.debug(
            f"Viewport resized: window=({window_w}x{window_h}), "
            f"virtual=({self._virtual_w}x{self._virtual_h}), "
            f"mode={self._mode}, scale={scale:.3f}, "
            f"viewport=({vw}x{vh})@({ox},{oy})"
        )

    @property
    def state(self) -> ViewportState:
        if self._state is None:
            raise RuntimeError(
                "Viewport not initialized. Call resize(window_w, window_h)."
            )
        return self._state

    def screen_to_virtual(self, x: float, y: float) -> tuple[float, float]:
        s = self.state
        return ((x - s.offset_x) / s.scale, (y - s.offset_y) / s.scale)

    def virtual_to_screen(self, x: float, y: float) -> tuple[float, float]:
        s = self.state
        return (s.offset_x + x * s.scale, s.offset_y + y * s.scale)
