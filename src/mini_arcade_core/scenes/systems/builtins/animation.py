from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable, Protocol


class HasAnimSprite(Protocol):
    anim: object | None  # Animation
    texture: int | None


@dataclass
class AnimationTickSystem:
    name: str = "common_anim_tick"
    order: int = 0
    get_entities: Callable[[object], Iterable[HasAnimSprite]] = lambda _w: ()

    def step(self, ctx):
        for e in self.get_entities(ctx.world):
            alive = getattr(e, "alive", True)
            if not alive:
                continue
            anim = getattr(e, "anim", None)
            if not anim:
                continue
            anim.update(ctx.dt)
            e.texture = anim.current_frame
