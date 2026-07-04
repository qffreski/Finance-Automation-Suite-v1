from pathlib import Path
import os
import json
import copy

from config.performance_detector import PerformanceDetector


class ConfigManager:

    def __init__(self, logger=None):

        self.logger = logger
        self.base_dir = Path(os.getenv("APPDATA")) / "Finance Automation Suite"
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.pdf_dir = self.base_dir / "pdf"
        self.pdf_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = self.base_dir / "config.json"

        # =====================================================
        # PERFORMANCE DETECTION
        # =====================================================

        self.detector = PerformanceDetector(logger=logger)
        self.performance_profile = self.detector.detect_profile()

        # =====================================================
        # DEFAULT CONFIG (WITH OPTIMIZATION)
        # =====================================================

        optimized = self.detector.get_optimized_config()

        self.default = {

            # ============================================
            # PROFILE
            # ============================================

            "performance_profile": self.performance_profile,
            "timing_multiplier": optimized["multiplier"],

            # ============================================
            # AUTOMATION
            # ============================================

            "click_delay": optimized["click_delay"],
            "typing_speed": optimized["typing_speed"],
            "upload_speed": optimized["upload_speed"],
            "retry": optimized["retry"],

            # ============================================
            # GLOBAL DELAY
            # ============================================

            "move_duration": optimized["move_duration"],
            "typing_delay": optimized["typing_delay"],
            "dialog_delay": optimized["dialog_delay"],
            "search_delay": optimized["search_delay"],
            "attachment_delay": optimized["attachment_delay"],
            "save_delay": optimized["save_delay"],
            "countdown_delay": optimized["countdown_delay"],

            # ============================================
            # PDF
            # ============================================

            "pdf_dir": str(self.pdf_dir),

            # ============================================
            # CALIBRATION
            # ============================================

            "positions": {}
        }

        self.data = self.load()

    # =====================================================
    # LOAD
    # =====================================================

    def load(self):

        if not self.config_file.exists():

            self.data = copy.deepcopy(self.default)
            self.save()

            return self.data

        try:

            with open(
                self.config_file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

        except Exception:

            data = {}

        merged = copy.deepcopy(self.default)
        merged.update(data)

        self.data = merged

        return self.data

    # =====================================================
    # SAVE
    # =====================================================

    def save(self):

        with open(
            self.config_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.data,
                f,
                indent=4
            )

    # =====================================================
    # BASIC GET
    # =====================================================

    def get(self, key, default=None):

        return self.data.get(key, default)

    # =====================================================
    # SAFE GET
    # =====================================================

    def get_int(self, key, default=0):

        try:
            return int(self.data.get(key, default))
        except Exception:
            return default

    def get_float(self, key, default=0.0):

        try:
            return float(self.data.get(key, default))
        except Exception:
            return default

    def get_str(self, key, default=""):

        try:
            return str(self.data.get(key, default))
        except Exception:
            return default

    def get_bool(self, key, default=False):

        value = self.data.get(key, default)

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            return value.lower() in (
                "true",
                "1",
                "yes",
                "y"
            )

        return bool(value)

    # =====================================================
    # PDF PATH
    # =====================================================

    def resolve_pdf(self, file_path):

        path = Path(file_path)

        if path.is_absolute():
            return path

        return Path(
            self.get_str("pdf_dir")
        ) / path.name

    # =====================================================
    # POSITION
    # =====================================================

    def get_position(self, key):

        pos = self.data.get(
            "positions",
            {}
        ).get(key)

        if pos is None:
            raise KeyError(
                f"Coordinate '{key}' belum dikalibrasi."
            )

        if isinstance(pos, (list, tuple)):

            return (
                int(pos[0]),
                int(pos[1])
            )

        if isinstance(pos, dict):

            return (
                int(pos["x"]),
                int(pos["y"])
            )

        raise ValueError(
            f"Format posisi tidak valid : {pos}"
        )

    def set_position(self, key, position):

        if isinstance(position, dict):

            position = [
                position["x"],
                position["y"]
            ]

        self.data.setdefault(
            "positions",
            {}
        )

        self.data["positions"][key] = [
            int(position[0]),
            int(position[1])
        ]

        self.save()

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.data = copy.deepcopy(
            self.default
        )

        self.save()

    # =====================================================
    # GET PROFILE INFO
    # =====================================================

    def get_profile_info(self):
        """
        Get performance profile info untuk ditampilkan di UI.
        """

        return {
            "profile": self.performance_profile,
            "multiplier": self.get_float("timing_multiplier", 1.0),
            "move_duration": self.get_float("move_duration", 0.25),
            "click_delay": self.get_float("click_delay", 0.8),
            "search_delay": self.get_float("search_delay", 3.0),
        }
