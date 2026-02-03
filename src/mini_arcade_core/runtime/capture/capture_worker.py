"""
Capture worker thread for saving screenshots.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from queue import Empty, Queue
from threading import Event, Thread
from typing import Callable, Optional

from PIL import Image

from mini_arcade_core.utils import logger


@dataclass(frozen=True)
class CaptureJob:
    """
    Job representing a screenshot to be saved.

    :ivar job_id (str): Unique identifier for the capture job.
    :ivar out_path (Path): Destination path for the saved screenshot.
    :ivar bmp_path (Path): Temporary path of the bitmap image to be saved.
    """

    job_id: str
    out_path: Path
    bmp_path: Path  # <-- file-based now


@dataclass(frozen=True)
class CaptureResult:
    """
    Result of a completed capture job.

    :ivar job_id (str): Unique identifier for the capture job.
    :ivar out_path (Path): Destination path where the screenshot was saved.
    :ivar ok (bool): Whether the capture was successful.
    :ivar error (Optional[str]): Error message if the capture failed.
    """

    job_id: str
    out_path: Path
    ok: bool
    error: str | None = None


@dataclass
class WorkerConfig:
    """
    Configuration options for the CaptureWorker.

    :ivar queue_size (int): Maximum number of jobs to queue.
    :ivar on_done (Optional[Callable[[CaptureResult], None]]):
        Optional callback invoked when a job is done.
    :ivar name (str): Name of the worker thread.
    :ivar daemon (bool): Whether the thread is a daemon thread.
    :ivar delete_temp (bool): Whether to delete temporary bitmap files after saving.
    """

    queue_size: int = 64
    on_done: Optional[Callable[[CaptureResult], None]] = None
    name: str = "capture-worker"
    daemon: bool = True
    delete_temp: bool = True


class CaptureWorker:
    """Capture worker thread for saving screenshots asynchronously."""

    def __init__(
        self,
        worker_config: WorkerConfig | None = None,
    ):
        """
        :param queue_size: Maximum number of jobs to queue.
        :type queue_size: int
        :param on_done: Optional callback invoked when a job is done.
        :type on_done: Optional[Callable[[CaptureResult], None]]
        :param name: Name of the worker thread.
        :type name: str
        :param daemon: Whether the thread is a daemon thread.
        :type daemon: bool
        :param delete_temp: Whether to delete temporary bitmap files after saving.
        :type delete_temp: bool
        """
        if worker_config is None:
            worker_config = WorkerConfig()
        self._q: Queue[CaptureJob] = Queue(maxsize=worker_config.queue_size)
        self._stop = Event()
        self._thread = Thread(
            target=self._run,
            name=worker_config.name,
            daemon=worker_config.daemon,
        )
        self._on_done = worker_config.on_done
        self._delete_temp = worker_config.delete_temp

    def start(self):
        """Start the capture worker thread."""
        if self._thread.is_alive():
            return
        self._stop.clear()
        self._thread.start()

    def stop(self):
        """Stop the capture worker thread."""
        self._stop.set()
        if self._thread.is_alive():
            self._thread.join(timeout=2.0)

    def enqueue(self, job: CaptureJob) -> bool:
        """
        Enqueue a capture job.

        :param job: CaptureJob to enqueue.
        :type job: CaptureJob
        :return: True if the job was enqueued successfully, False otherwise.
        :rtype: bool
        """
        if self._stop.is_set():
            return False
        try:
            self._q.put_nowait(job)
            return True
        # Justification: Queue.put_nowait can raise a broad exception
        # pylint: disable=broad-exception-caught
        except Exception:
            return False
        # pylint: enable=broad-exception-caught

    def _run(self):
        while not self._stop.is_set():
            try:
                job = self._q.get(timeout=0.1)
            except Empty:
                continue

            try:
                job.out_path.parent.mkdir(parents=True, exist_ok=True)

                img = Image.open(str(job.bmp_path))
                img.save(str(job.out_path))

                if self._delete_temp:
                    try:
                        job.bmp_path.unlink(missing_ok=True)
                    except Exception:  # pylint: disable=broad-exception-caught
                        logger.warning(
                            f"Failed to delete temp bmp: {job.bmp_path}"
                        )

                res = CaptureResult(
                    job_id=job.job_id, out_path=job.out_path, ok=True
                )

            except Exception as exc:  # pylint: disable=broad-exception-caught
                logger.exception("CaptureWorker failed to save screenshot")
                res = CaptureResult(
                    job_id=job.job_id,
                    out_path=job.out_path,
                    ok=False,
                    error=str(exc),
                )

            if self._on_done:
                try:
                    self._on_done(res)
                except Exception:  # pylint: disable=broad-exception-caught
                    logger.warning("CaptureWorker on_done callback failed")

            self._q.task_done()
