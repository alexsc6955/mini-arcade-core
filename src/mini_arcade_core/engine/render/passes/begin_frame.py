"""
Begin Frame Render Pass
"""

from dataclasses import dataclass

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.context import RenderContext
from mini_arcade_core.engine.render.packet import RenderPacket


@dataclass
class BeginFramePass:
    """
    Begin Frame Render Pass.
    This pass signals the start of a new frame to the backend.
    """

    name: str = "BeginFrame"

    def run(
        self, backend: Backend, ctx: RenderContext, packets: list[RenderPacket]
    ):
        """Run the begin frame pass."""
        backend.begin_frame()
