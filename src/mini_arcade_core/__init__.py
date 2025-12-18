"""
Entry point for the mini_arcade_core package.
Provides access to core classes and a convenience function to run a game.

mini_arcade_core/
|-- __init__.py # main entry point
|-- game.py # core game loop and management
|-- entity.py # base entity classes
|-- backend/ # backend abstraction layer
|   |-- __init__.py
|   |-- backend.py # abstract Backend class
|   |-- events.py # event definitions
|   |-- types.py # common types like Color
|-- keymaps/ # key mapping utilities
|   |-- __init__.py
|   |-- keys.py # key definitions and keymaps
|   |-- sdl.py # SDL keycode mappings
|-- scenes/ # scene management
|   |-- __init__.py
|   |-- autoreg.py # automatic scene registration
|   |-- registry.py # SceneRegistry class
|   |-- scene.py # base Scene class
|-- two_d/ # 2D utilities and types
|   |-- __init__.py
|   |-- boundaries2d.py # boundary behaviors
|   |-- collision2d.py # collision detection
|   |-- geometry2d.py # geometric types like Position2D, Size2D
|   |-- kinematics2d.py # kinematic data structures
|   |-- physics2d.py # physics-related types like Velocity2D
|-- ui/ # user interface components
|   |-- __init__.py
|   |-- menu.py # menu components
"""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError, version

from mini_arcade_core.backend import Backend, Event, EventType
from mini_arcade_core.entity import Entity, KinematicEntity, SpriteEntity
from mini_arcade_core.game import Game, GameConfig
from mini_arcade_core.keymaps.keys import Key, keymap
from mini_arcade_core.scenes import Scene, SceneRegistry, register_scene
from mini_arcade_core.two_d import (
    Bounds2D,
    KinematicData,
    Position2D,
    RectCollider,
    RectKinematic,
    RectSprite,
    Size2D,
    Velocity2D,
    VerticalBounce,
    VerticalWrap,
)

logger = logging.getLogger(__name__)


def run_game(
    initial_scene_cls: type[Scene],
    config: GameConfig | None = None,
    registry: SceneRegistry | None = None,
):
    """
    Convenience helper to bootstrap and run a game with a single scene.

    :param initial_scene_cls: The Scene subclass to instantiate as the initial scene.
    :type initial_scene_cls: type[Scene]

    :param config: Optional GameConfig to customize game settings.
    :type config: GameConfig | None

    :param registry: Optional SceneRegistry for scene management.
    :type registry: SceneRegistry | None

    :raises ValueError: If the provided config does not have a valid Backend.
    """
    cfg = config or GameConfig()
    if config.backend is None:
        raise ValueError(
            "GameConfig.backend must be set to a Backend instance"
        )
    game = Game(cfg, registry=registry)
    scene = initial_scene_cls(game)
    game.run(scene)


__all__ = [
    "Game",
    "GameConfig",
    "Scene",
    "Entity",
    "SpriteEntity",
    "run_game",
    "Backend",
    "Event",
    "EventType",
    "Velocity2D",
    "Position2D",
    "Size2D",
    "KinematicEntity",
    "KinematicData",
    "RectCollider",
    "VerticalBounce",
    "Bounds2D",
    "VerticalWrap",
    "RectSprite",
    "RectKinematic",
    "Key",
    "keymap",
    "SceneRegistry",
    "register_scene",
]

PACKAGE_NAME = "mini-arcade-core"  # or whatever is in your pyproject.toml


def get_version() -> str:
    """
    Return the installed package version.

    This is a thin helper around importlib.metadata.version so games can do:

        from mini_arcade_core import get_version
        print(get_version())

    :return: The version string of the installed package.
    :rtype: str

    :raises PackageNotFoundError: If the package is not installed.
    """
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:  # if running from source / editable
        logger.warning(
            f"Package '{PACKAGE_NAME}' not found. Returning default version '0.0.0'."
        )
        return "0.0.0"


__version__ = get_version()
__version__ = get_version()
__version__ = get_version()
__version__ = get_version()
