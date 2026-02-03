"""
Capture settings dataclass
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CaptureSettings:
    """
    Settings for the Capture Service.

    :ivar screenshots_dir: Directory to save screenshots.
    :ivar screenshots_ext: File extension/format for screenshots.
    :ivar replays_dir: Directory to save replays.
    """

    screenshots_dir: str = "screenshots"
    screenshots_ext: str = "png"
    replays_dir: str = "replays"
