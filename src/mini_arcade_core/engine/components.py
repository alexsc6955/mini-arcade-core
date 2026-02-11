from dataclasses import dataclass
from typing import Optional

from mini_arcade_core.engine.animation import Animation


@dataclass
class Renderable:
    texture: Optional[int] = None
    visible: bool = True


@dataclass
class Animated:
    anim: Optional["Animation"] = None
    texture: Optional[int] = None


@dataclass
class Alive:
    alive: bool = True


@dataclass
class TTL:
    ttl: float
    alive: bool = True

    def step(self, dt: float) -> None:
        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False
