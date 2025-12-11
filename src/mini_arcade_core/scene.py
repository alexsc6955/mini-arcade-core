"""
Base class for game scenes (states/screens).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, List

from mini_arcade_core.backend import Backend
from mini_arcade_core.entity import Entity
from mini_arcade_core.geometry2d import Size2D

from .game import Game

OverlayFunc = Callable[[Backend], None]


class Scene(ABC):
    """Base class for game scenes (states/screens)."""

    def __init__(self, game: Game):
        """
        :param game: Reference to the main Game object.
        :type game: Game
        """
        self.game = game
        self.entities: List[Entity] = []
        self.size: Size2D = Size2D(game.config.width, game.config.height)
        # overlays drawn on top of the scene
        self._overlays: List[OverlayFunc] = []

    def add_entity(self, *entities: Entity) -> None:
        """Register one or more entities in this scene."""
        self.entities.extend(entities)

    def remove_entity(self, entity: Entity) -> None:
        """Unregister a single entity, if present."""
        if entity in self.entities:
            self.entities.remove(entity)

    def clear_entities(self) -> None:
        """Remove all entities from the scene."""
        self.entities.clear()

    def update_entities(self, dt: float) -> None:
        """Default update loop for all entities."""
        for ent in self.entities:
            ent.update(dt)

    def draw_entities(self, surface: Backend) -> None:
        """Default draw loop for all entities."""
        for ent in self.entities:
            ent.draw(surface)

    def add_overlay(self, overlay: OverlayFunc) -> None:
        """
        Register an overlay (drawn every frame, after entities).

        :param overlay: A callable that takes a Backend and draws on it.
        :type overlay: OverlayFunc
        """
        self._overlays.append(overlay)

    def remove_overlay(self, overlay: OverlayFunc) -> None:
        """
        Unregister a previously added overlay.

        :param overlay: The overlay to remove.
        :type overlay: OverlayFunc
        """
        if overlay in self._overlays:
            self._overlays.remove(overlay)

    def clear_overlays(self) -> None:
        """Clear all registered overlays."""
        self._overlays.clear()

    def draw_overlays(self, surface: Backend) -> None:
        """
        Call all overlays. Scenes should call this at the end of draw().

        :param surface: The backend surface to draw on.
        :type surface: Backend
        """
        for overlay in self._overlays:
            overlay(surface)

    @abstractmethod
    def on_enter(self):
        """Called when the scene becomes active."""

    @abstractmethod
    def on_exit(self):
        """Called when the scene is replaced."""

    @abstractmethod
    def handle_event(self, event: object):
        """
        Handle input / events (e.g. pygame.Event).

        :param event: The event to handle.
        :type event: object
        """

    @abstractmethod
    def update(self, dt: float):
        """
        Update game logic. ``dt`` is the delta time in seconds.

        :param dt: Time delta in seconds.
        :type dt: float
        """

    @abstractmethod
    def draw(self, surface: object):
        """
        Render to the main surface.

        :param surface: The backend surface to draw on.
        :type surface: object
        """
