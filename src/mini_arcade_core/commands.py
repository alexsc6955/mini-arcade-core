"""
Command protocol for executing commands with a given context.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, List, Optional, Protocol, TypeVar

from mini_arcade_core.runtime.services import RuntimeServices
from mini_arcade_core.scenes.model import SceneModel
from mini_arcade_core.utils import deprecated

if TYPE_CHECKING:
    from mini_arcade_core.game import Game
# Justification: Generic type for context
# pylint: disable=invalid-name
TContext = TypeVar("TContext")
# pylint: enable=invalid-name


class BaseCommand(Protocol, Generic[TContext]):
    """
    Protocol for a command that can be executed with a given context.
    """

    @deprecated(
        reason="BaseCommand is deprecated, use Command protocol instead.",
        version="1.0",
        alternative="Command",
    )
    def __call__(self, context: TContext) -> None:
        """
        Execute the cheat code with the given context.

        :param context: Context object for cheat execution.
        :type context: TContext
        """
        self.execute(context)

    def execute(self, context: TContext):
        """
        Execute the command with the given context.

        :param context: Context object for command execution.
        :type context: TContext
        """


class BaseGameCommand(BaseCommand["Game"]):
    """
    Base class for commands that operate on the Game context.
    """

    def execute(self, context: "Game") -> None:
        """
        Execute the command with the given Game context.

        :param context: Game context for command execution.
        :type context: "Game"
        """
        raise NotImplementedError(
            "Execute method must be implemented by subclasses."
        )


class BaseSceneCommand(BaseCommand[SceneModel]):
    """
    Base class for commands that operate on the Scene SceneModel context within a scene.
    """

    def execute(self, context: SceneModel) -> None:
        """
        Execute the command with the given Scene Model context.

        :param context: Scene Model context for command execution.
        :type context: SceneModel
        """
        raise NotImplementedError(
            "Execute method must be implemented by subclasses."
        )


class QuitGameCommand(BaseGameCommand):
    """
    Command to quit the game.
    """

    def execute(self, context: Game) -> None:
        context.quit()


class Command(Protocol):
    """
    A command is the only allowed "write path" from input/systems into:
    - scene operations (push/pop/change/quit)
    - capture
    - global game lifecycle
    - later: world mutations (if you pass a world reference)

    For now we keep it simple: commands only need RuntimeServices.
    """

    def execute(
        self, services: RuntimeServices, world: Optional[object] = None
    ) -> None:
        """
        Execute the command with the given world and runtime services.

        :param services: Runtime services for command execution.
        :type services: RuntimeServices

        :param world: The world object (can be any type).
        :type world: object | None
        """


@dataclass
class CommandQueue:
    """
    Queue for storing and executing commands.
    """

    _items: List[Command] = field(default_factory=list)

    def push(self, cmd: Command) -> None:
        """
        Push a command onto the queue.

        :param cmd: Command to be added to the queue.
        :type cmd: Command
        """
        self._items.append(cmd)

    def drain(self) -> List[Command]:
        """
        Drain and return all commands from the queue.

        :return: List of commands that were in the queue.
        :rtype: list[Command]
        """
        items = self._items
        self._items = []
        return items


@dataclass(frozen=True)
class QuitCommand(Command):
    """Quit the game."""

    def execute(
        self, services: RuntimeServices, world: Optional[object] = None
    ) -> None:
        services.scenes.quit()


@dataclass(frozen=True)
class ScreenshotCommand(Command):
    """
    Take a screenshot.

    :ivar label (str | None): Optional label for the screenshot file.
    """

    label: str | None = None

    def execute(
        self, services: RuntimeServices, world: Optional[object] = None
    ) -> None:
        services.capture.screenshot(label=self.label, mode="manual")


@dataclass(frozen=True)
class PushSceneCommand(Command):
    """
    Push a new scene onto the scene stack.

    :ivar scene_id (str): Identifier of the scene to push.
    :ivar as_overlay (bool): Whether to push the scene as an overlay.
    """

    scene_id: str
    as_overlay: bool = False

    def execute(
        self, services: RuntimeServices, world: Optional[object] = None
    ) -> None:
        services.scenes.push(self.scene_id, as_overlay=self.as_overlay)


@dataclass(frozen=True)
class PopSceneCommand(Command):
    """Pop the current scene from the scene stack."""

    def execute(
        self, services: RuntimeServices, world: Optional[object] = None
    ) -> None:
        services.scenes.pop()


@dataclass(frozen=True)
class ChangeSceneCommand(Command):
    """
    Change the current scene to the specified scene.

    :ivar scene_id (str): Identifier of the scene to switch to.
    """

    scene_id: str

    def execute(
        self, services: RuntimeServices, world: Optional[object] = None
    ) -> None:
        services.scenes.change(self.scene_id)
