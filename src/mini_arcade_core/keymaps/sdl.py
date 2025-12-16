"""
SDL keymap for mini arcade core.
Maps SDL keycodes to mini arcade core Key enums.
"""

from __future__ import annotations

from mini_arcade_core.keys import Key

# SDL keycodes you need (minimal set)
SDLK_ESCAPE = 27
SDLK_RETURN = 13
SDLK_SPACE = 32
SDLK_TAB = 9
SDLK_BACKSPACE = 8

SDLK_UP = 1073741906
SDLK_DOWN = 1073741905
SDLK_LEFT = 1073741904
SDLK_RIGHT = 1073741903

F1 = 1073741882
F2 = 1073741883
F3 = 1073741884
F4 = 1073741885
F5 = 1073741886
F6 = 1073741887
F7 = 1073741888
F8 = 1073741889
F9 = 1073741890
F10 = 1073741891
F11 = 1073741892
F12 = 1073741893

SDL_KEYCODE_TO_KEY: dict[int, Key] = {
    # Letters
    ord("a"): Key.A,
    ord("b"): Key.B,
    ord("c"): Key.C,
    ord("d"): Key.D,
    ord("e"): Key.E,
    ord("f"): Key.F,
    ord("g"): Key.G,
    ord("h"): Key.H,
    ord("i"): Key.I,
    ord("j"): Key.J,
    ord("k"): Key.K,
    ord("l"): Key.L,
    ord("m"): Key.M,
    ord("n"): Key.N,
    ord("o"): Key.O,
    ord("p"): Key.P,
    ord("q"): Key.Q,
    ord("r"): Key.R,
    ord("s"): Key.S,
    ord("t"): Key.T,
    ord("u"): Key.U,
    ord("v"): Key.V,
    ord("w"): Key.W,
    ord("x"): Key.X,
    ord("y"): Key.Y,
    ord("z"): Key.Z,
    # Arrows
    SDLK_UP: Key.UP,
    SDLK_DOWN: Key.DOWN,
    SDLK_LEFT: Key.LEFT,
    SDLK_RIGHT: Key.RIGHT,
    # Common
    SDLK_ESCAPE: Key.ESCAPE,
    SDLK_SPACE: Key.SPACE,
    SDLK_RETURN: Key.ENTER,
    SDLK_TAB: Key.TAB,
    SDLK_BACKSPACE: Key.BACKSPACE,
    # Numbers
    ord("0"): Key.NUM_0,
    ord("1"): Key.NUM_1,
    ord("2"): Key.NUM_2,
    ord("3"): Key.NUM_3,
    ord("4"): Key.NUM_4,
    ord("5"): Key.NUM_5,
    ord("6"): Key.NUM_6,
    ord("7"): Key.NUM_7,
    ord("8"): Key.NUM_8,
    ord("9"): Key.NUM_9,
    # Function keys
    F1: Key.F1,
    F2: Key.F2,
    F3: Key.F3,
    F4: Key.F4,
    F5: Key.F5,
    F6: Key.F6,
    F7: Key.F7,
    F8: Key.F8,
    F9: Key.F9,
    F10: Key.F10,
    F11: Key.F11,
    F12: Key.F12,
}
