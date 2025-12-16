"""
Scene registry for mini arcade core.
Allows registering and creating scenes by string IDs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Protocol

if TYPE_CHECKING:
    from mini_arcade_core.game import Game
    from mini_arcade_core.scene import Scene


class SceneFactory(Protocol):
    """
    Protocol for scene factory callables.
    """

    def __call__(self, game: "Game") -> "Scene": ...


@dataclass
class SceneRegistry:
    """
    Registry for scene factories, allowing registration and creation of scenes by string IDs.
    """

    _factories: Dict[str, SceneFactory]

    def register(self, scene_id: str, factory: SceneFactory) -> None:
        """
        Register a scene factory under a given scene ID.

        :param scene_id: The string ID for the scene.
        :type scene_id: str

        :param factory: A callable that creates a Scene instance.
        :type factory: SceneFactory
        """
        self._factories[scene_id] = factory

    def create(self, scene_id: str, game: "Game") -> "Scene":
        """
        Create a scene instance using the registered factory for the given scene ID.

        :param scene_id: The string ID of the scene to create.
        :type scene_id: str

        :param game: The Game instance to pass to the scene factory.
        :type game: Game

        :return: A new Scene instance.
        :rtype: Scene

        :raises KeyError: If no factory is registered for the given scene ID.
        """
        try:
            return self._factories[scene_id](game)
        except KeyError as e:
            raise KeyError(f"Unknown scene_id={scene_id!r}") from e
