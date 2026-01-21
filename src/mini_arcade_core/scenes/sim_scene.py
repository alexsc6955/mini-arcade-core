from __future__ import annotations

from typing import Protocol, runtime_checkable

from mini_arcade_core.engine.render.packet import RenderPacket
from mini_arcade_core.runtime.input_frame import InputFrame


@runtime_checkable
class SimScene(Protocol):
    def on_enter(self) -> None: ...
    def on_exit(self) -> None: ...
    def tick(self, input_frame: InputFrame, dt: float) -> None: ...
    def build_render_packet(self) -> RenderPacket: ...
