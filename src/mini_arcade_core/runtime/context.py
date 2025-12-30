from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mini_arcade_core.commands import CommandQueue
    from mini_arcade_core.game import Game, GameConfig, GameSettings
    from mini_arcade_core.runtime.services import RuntimeServices


@dataclass(frozen=True)
class RuntimeContext:
    services: RuntimeServices
    config: GameConfig
    settings: GameSettings
    commands: CommandQueue | None = None

    @staticmethod
    def from_game(game_entity: Game) -> "RuntimeContext":
        return RuntimeContext(
            services=game_entity.services,
            config=game_entity.config,
            settings=game_entity.settings,
        )
