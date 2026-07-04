import time
import pyautogui
from PySide6.QtCore import QThread, Signal


class CalibrationWorker(QThread):
    """
    Worker thread untuk capture koordinat tanpa freeze UI.
    """
    
    progress = Signal(int)  # Emit countdown: 5, 4, 3, 2, 1
    finished = Signal(tuple)  # Emit (x, y)
    error = Signal(str)  # Emit error message

    def __init__(self, config, logger, key):
        super().__init__()
        self.config = config
        self.logger = logger
        self.key = key
        self.running = True

    def run(self):
        try:
            delay = self.config.get_float("countdown_delay", 1)

            # ==========================
            # COUNTDOWN (Non-blocking)
            # ==========================

            for i in range(5, 0, -1):
                if not self.running:
                    self.error.emit("Capture dibatalkan.")
                    return

                self.progress.emit(i)
                
                self.logger.info(f"Capture {self.key} : {i}")
                
                time.sleep(delay)

            # ==========================
            # GET POSITION
            # ==========================

            x, y = pyautogui.position()

            self.logger.info(f"Mouse Position : ({x}, {y})")

            # ==========================
            # SAVE CONFIG
            # ==========================

            self.config.set_position(self.key, [x, y])

            self.logger.info(
                f"Calibration saved : {self.key} -> ({x}, {y})"
            )

            self.finished.emit((x, y))

        except Exception as e:
            self.logger.exception(e)
            self.error.emit(str(e))

    def stop(self):
        """Stop capture process."""
        self.running = False


class CalibrationTool:

    def __init__(self, config, logger):

        self.config = config
        self.logger = logger
        self.worker_thread = None

    # =====================================================
    # CAPTURE POSITION (ASYNC)
    # =====================================================

    def capture_async(
        self,
        key,
        progress_callback=None,
        finished_callback=None,
        error_callback=None,
        status_callback=None
    ):
        """
        Capture posisi mouse secara async (tidak freeze UI).

        Parameters
        ----------
        key : str
            Nama koordinat.

        progress_callback : callable(int), optional
            Callback countdown (5..1)

        finished_callback : callable(tuple), optional
            Callback ketika selesai dengan (x, y)

        error_callback : callable(str), optional
            Callback ketika error

        status_callback : callable(str), optional
            Callback status proses.
        """

        self.logger.info(f"Calibration start : {key}")

        if status_callback:
            status_callback(f"Capture '{key}' dimulai dalam 5 detik...")

        # Create worker thread
        self.worker_thread = CalibrationWorker(
            self.config,
            self.logger,
            key
        )

        # Connect signals
        if progress_callback:
            self.worker_thread.progress.connect(progress_callback)

        if finished_callback:
            self.worker_thread.finished.connect(
                lambda pos: self._on_finished(
                    key,
                    pos,
                    finished_callback,
                    status_callback
                )
            )

        if error_callback:
            self.worker_thread.error.connect(error_callback)

        # Start worker thread
        self.worker_thread.start()

    def _on_finished(self, key, pos, callback, status_callback):
        """Callback ketika capture selesai."""
        if status_callback:
            status_callback(f"Capture '{key}' selesai.")
        
        if callback:
            callback(pos)

        self.worker_thread = None

    def stop_capture(self):
        """Stop capture yang sedang berjalan."""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.worker_thread.wait()
            self.worker_thread = None

    # =====================================================
    # CAPTURE POSITION (SYNC - Legacy)
    # =====================================================

    def capture(
        self,
        key,
        progress_callback=None,
        status_callback=None
    ):
        """
        Capture posisi mouse secara synchronous (blocking).
        
        DEPRECATED: Gunakan capture_async() untuk menghindari UI freeze.

        Parameters
        ----------
        key : str
            Nama koordinat.

        progress_callback : callable(int), optional
            Callback countdown (5..1)

        status_callback : callable(str), optional
            Callback status proses.
        """

        self.logger.info(f"Calibration start : {key}")

        if status_callback:
            status_callback(f"Capture '{key}' dimulai.")

        delay = self.config.get_float(
            "countdown_delay",
            1
        )

        # ==========================
        # COUNTDOWN
        # ==========================

        for i in range(5, 0, -1):

            if progress_callback:
                progress_callback(i)

            self.logger.info(
                f"Capture {key} : {i}"
            )

            time.sleep(delay)

        # ==========================
        # GET POSITION
        # ==========================

        x, y = pyautogui.position()

        self.logger.info(
            f"Mouse Position : ({x}, {y})"
        )

        # ==========================
        # SAVE CONFIG
        # ==========================

        self.config.set_position(
            key,
            [x, y]
        )

        self.logger.info(
            f"Calibration saved : {key} -> ({x}, {y})"
        )

        if status_callback:
            status_callback(
                f"Capture '{key}' selesai."
            )

        return x, y
