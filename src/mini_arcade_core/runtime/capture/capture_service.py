"""
Capture service managing screenshots and replays.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from mini_arcade_core.backend import Backend
from mini_arcade_core.runtime.capture.capture_service_protocol import (
    CaptureServicePort,
)
from mini_arcade_core.runtime.capture.capture_settings import CaptureSettings
from mini_arcade_core.runtime.capture.replay import (
    ReplayPlayer,
    ReplayRecorder,
    ReplayRecorderConfig,
)
from mini_arcade_core.runtime.capture.replay_format import ReplayHeader
from mini_arcade_core.runtime.capture.screenshot_capturer import (
    ScreenshotCapturer,
)
from mini_arcade_core.runtime.input_frame import InputFrame


class CaptureService(CaptureServicePort):
    """
    Owns:
        - screenshots (delegated)
        - replay recording (InputFrame stream)
        - replay playback (feeds InputFrames)
        - (later) video recording
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        backend: Backend,
        *,
        screenshots: Optional[ScreenshotCapturer] = None,
        replay_recorder: Optional[ReplayRecorder] = None,
        replay_player: Optional[ReplayPlayer] = None,
        settings: Optional[CaptureSettings] = None,
    ):
        self.backend = backend
        self.settings = settings or CaptureSettings()

        self.screenshots = screenshots or ScreenshotCapturer(backend)
        self.replay_recorder = replay_recorder or ReplayRecorder()
        self.replay_player = replay_player or ReplayPlayer()

    # -------- screenshots --------
    def screenshot(self, label: str | None = None) -> str:
        return self.screenshots.screenshot(label)

    def screenshot_sim(
        self, run_id: str, frame_index: int, label: str = "frame"
    ) -> str:
        return self.screenshots.screenshot_sim(run_id, frame_index, label)

    # -------- replays --------
    @property
    def replay_playing(self) -> bool:
        return self.replay_player.active

    @property
    def replay_recording(self) -> bool:
        return self.replay_recorder.active

    def start_replay_record(
        self,
        *,
        filename: str,
        header: ReplayHeader,
    ) -> None:
        path = Path(self.settings.replays_dir) / filename
        self.replay_recorder.start(
            ReplayRecorderConfig(path=path, header=header)
        )

    def stop_replay_record(self) -> None:
        self.replay_recorder.stop()

    def record_input(self, frame: InputFrame) -> None:
        self.replay_recorder.record(frame)

    def start_replay_play(self, filename: str) -> ReplayHeader:
        path = Path(self.settings.replays_dir) / filename
        return self.replay_player.start(path)

    def stop_replay_play(self) -> None:
        self.replay_player.stop()

    def next_replay_input(self) -> InputFrame:
        return self.replay_player.next()
