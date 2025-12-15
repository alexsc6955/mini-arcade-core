from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from mini_arcade_core.backend import Backend, Color, Event, EventType

MenuAction = Callable[[], None]


@dataclass(frozen=True)
class MenuItem:
    label: str
    on_select: MenuAction


@dataclass
class MenuStyle:
    normal: Color = (220, 220, 220)
    selected: Color = (255, 255, 0)
    line_height: int = 28


class Menu:
    def __init__(
        self,
        items: Sequence[MenuItem],
        *,
        x: int = 40,
        y: int = 40,
        style: MenuStyle | None = None,
    ):
        self.items = list(items)
        self.x = x
        self.y = y
        self.style = style or MenuStyle()
        self.selected_index = 0

    def move_up(self):
        if self.items:
            self.selected_index = (self.selected_index - 1) % len(self.items)

    def move_down(self):
        if self.items:
            self.selected_index = (self.selected_index + 1) % len(self.items)

    def select(self):
        if self.items:
            self.items[self.selected_index].on_select()

    def handle_event(
        self,
        event: Event,
        *,
        up_key: int,
        down_key: int,
        select_key: int,
    ):
        if event.type != EventType.KEYDOWN or event.key is None:
            return
        if event.key == up_key:
            self.move_up()
        elif event.key == down_key:
            self.move_down()
        elif event.key == select_key:
            self.select()

    def draw(self, surface: Backend):
        for i, item in enumerate(self.items):
            color = (
                self.style.selected
                if i == self.selected_index
                else self.style.normal
            )
            surface.draw_text(
                self.x,
                self.y + i * self.style.line_height,
                item.label,
                color=color,
            )
