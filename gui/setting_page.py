from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QSpinBox,
    QDoubleSpinBox,
    QMessageBox,
    QGridLayout,
)


class SettingPage(QWidget):

    def __init__(self, context):

        super().__init__()

        # =====================================================
        # CONTEXT
        # =====================================================

        self.context = context
        self.config = context.config
        self.logger = context.logger
        self.calibration = context.calibration

        # =====================================================
        # STATE
        # =====================================================

        self.calibration_key = None

        self.init_ui()

    # =====================================================
    # UI
    # =====================================================

    def init_ui(self):

        layout = QVBoxLayout(self)

        # =====================================================
        # PERFORMANCE PROFILE
        # =====================================================

        profile_group = QGroupBox("Performance Profile")
        profile_layout = QGridLayout()

        profile_info = self.config.get_profile_info()

        # Profile name
        profile_name = profile_info.get("profile", "unknown").upper()
        self.lbl_profile = QLabel(f"Profile: {profile_name}")
        self.lbl_profile.setStyleSheet("font-weight: bold; font-size: 12px;")
        profile_layout.addWidget(self.lbl_profile, 0, 0, 1, 2)

        # Multiplier
        multiplier = profile_info.get("multiplier", 1.0)
        self.lbl_multiplier = QLabel(f"Timing Multiplier: {multiplier}x")
        profile_layout.addWidget(self.lbl_multiplier, 1, 0, 1, 2)

        # Move duration
        move_duration = profile_info.get("move_duration", 0.25)
        self.lbl_move = QLabel(f"Mouse Move Duration: {move_duration:.2f}s")
        profile_layout.addWidget(self.lbl_move, 2, 0, 1, 2)

        # Click delay
        click_delay = profile_info.get("click_delay", 0.8)
        self.lbl_click = QLabel(f"Click Delay: {click_delay:.2f}s")
        profile_layout.addWidget(self.lbl_click, 3, 0, 1, 2)

        # Search delay
        search_delay = profile_info.get("search_delay", 3.0)
        self.lbl_search = QLabel(f"Search Delay: {search_delay:.2f}s")
        profile_layout.addWidget(self.lbl_search, 4, 0, 1, 2)

        profile_group.setLayout(profile_layout)
        layout.addWidget(profile_group)

        # =====================================================
        # CALIBRATION
        # =====================================================

        calibration_group = QGroupBox("Calibration")
        calibration_layout = QVBoxLayout()

        self.lbl_calibration_status = QLabel(
            "Kalibrasi koordinat untuk automation"
        )
        calibration_layout.addWidget(self.lbl_calibration_status)

        # Grid untuk buttons
        button_grid = QGridLayout()

        positions = [
            "query", "checkbox", "option", "attachment",
            "new", "plus", "file_name", "open",
            "save", "exit1", "exit2", "error"
        ]

        row, col = 0, 0
        self.calibration_buttons = {}

        for pos in positions:

            btn = QPushButton(f"Capture: {pos}")
            btn.clicked.connect(
                lambda checked, key=pos: self.start_calibration(key)
            )

            button_grid.addWidget(btn, row, col)
            self.calibration_buttons[pos] = btn

            col += 1
            if col >= 3:
                col = 0
                row += 1

        calibration_layout.addLayout(button_grid)

        # Reset button
        btn_reset = QPushButton("Reset All Calibration")
        btn_reset.setStyleSheet("background-color: #ff6b6b; color: white;")
        btn_reset.clicked.connect(self.reset_calibration)
        calibration_layout.addWidget(btn_reset)

        calibration_group.setLayout(calibration_layout)
        layout.addWidget(calibration_group)

        # =====================================================
        # TIMING ADJUSTMENT
        # =====================================================

        timing_group = QGroupBox("Timing Adjustment (Optional)")
        timing_layout = QGridLayout()

        # Move duration
        timing_layout.addWidget(QLabel("Move Duration (s):"), 0, 0)
        self.spin_move = QDoubleSpinBox()
        self.spin_move.setMinimum(0.1)
        self.spin_move.setMaximum(5.0)
        self.spin_move.setSingleStep(0.1)
        self.spin_move.setValue(
            self.config.get_float("move_duration", 0.25)
        )
        timing_layout.addWidget(self.spin_move, 0, 1)

        # Click delay
        timing_layout.addWidget(QLabel("Click Delay (s):"), 1, 0)
        self.spin_click = QDoubleSpinBox()
        self.spin_click.setMinimum(0.1)
        self.spin_click.setMaximum(5.0)
        self.spin_click.setSingleStep(0.1)
        self.spin_click.setValue(
            self.config.get_float("click_delay", 0.8)
        )
        timing_layout.addWidget(self.spin_click, 1, 1)

        # Search delay
        timing_layout.addWidget(QLabel("Search Delay (s):"), 2, 0)
        self.spin_search = QDoubleSpinBox()
        self.spin_search.setMinimum(1.0)
        self.spin_search.setMaximum(10.0)
        self.spin_search.setSingleStep(0.5)
        self.spin_search.setValue(
            self.config.get_float("search_delay", 3.0)
        )
        timing_layout.addWidget(self.spin_search, 2, 1)

        # Dialog delay
        timing_layout.addWidget(QLabel("Dialog Delay (s):"), 3, 0)
        self.spin_dialog = QDoubleSpinBox()
        self.spin_dialog.setMinimum(0.5)
        self.spin_dialog.setMaximum(5.0)
        self.spin_dialog.setSingleStep(0.1)
        self.spin_dialog.setValue(
            self.config.get_float("dialog_delay", 1.5)
        )
        timing_layout.addWidget(self.spin_dialog, 3, 1)

        timing_group.setLayout(timing_layout)
        layout.addWidget(timing_group)

        # =====================================================
        # SAVE TIMING
        # =====================================================

        btn_save_timing = QPushButton("Save Timing Settings")
        btn_save_timing.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_save_timing.clicked.connect(self.save_timing)
        layout.addWidget(btn_save_timing)

        # Stretch
        layout.addStretch()

    # =====================================================
    # CALIBRATION
    # =====================================================

    def start_calibration(self, key):

        self.logger.info(f"Start calibration: {key}")

        self.calibration_key = key

        # Disable all buttons
        for btn in self.calibration_buttons.values():
            btn.setEnabled(False)

        self.lbl_calibration_status.setText(
            f"Calibrating '{key}'... Pindahkan mouse ke posisi dalam 5 detik"
        )

        # Start async capture
        self.calibration.capture_async(
            key,
            progress_callback=self.on_countdown,
            finished_callback=self.on_calibration_finished,
            error_callback=self.on_calibration_error,
            status_callback=self.on_calibration_status
        )

    def on_countdown(self, count):
        """Update countdown display."""
        self.lbl_calibration_status.setText(
            f"Calibrating '{self.calibration_key}'... {count}"
        )

    def on_calibration_finished(self, pos):
        """Callback ketika capture selesai."""
        x, y = pos
        self.logger.info(f"Calibration finished: {self.calibration_key} -> ({x}, {y})")

        # Re-enable all buttons
        for btn in self.calibration_buttons.values():
            btn.setEnabled(True)

        self.lbl_calibration_status.setText(
            f"✓ '{self.calibration_key}' berhasil dikalibrasi: ({x}, {y})"
        )

    def on_calibration_status(self, status):
        """Callback untuk status update."""
        self.lbl_calibration_status.setText(status)

    def on_calibration_error(self, error):
        """Callback ketika error."""
        self.logger.error(f"Calibration error: {error}")

        # Re-enable all buttons
        for btn in self.calibration_buttons.values():
            btn.setEnabled(True)

        QMessageBox.critical(
            self,
            "Calibration Error",
            f"Calibration gagal: {error}"
        )

    def reset_calibration(self):
        """Reset semua calibration."""
        reply = QMessageBox.question(
            self,
            "Reset Calibration",
            "Yakin ingin reset semua calibration?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            self.config.data["positions"] = {}
            self.config.save()

            self.logger.warning("All calibration reset")

            QMessageBox.information(
                self,
                "Success",
                "Semua calibration telah direset."
            )

            self.lbl_calibration_status.setText(
                "Kalibrasi koordinat untuk automation"
            )

    # =====================================================
    # TIMING SETTINGS
    # =====================================================

    def save_timing(self):
        """Save timing adjustments."""
        self.config.set("move_duration", self.spin_move.value())
        self.config.set("click_delay", self.spin_click.value())
        self.config.set("search_delay", self.spin_search.value())
        self.config.set("dialog_delay", self.spin_dialog.value())

        self.logger.info("Timing settings saved")

        QMessageBox.information(
            self,
            "Success",
            "Timing settings telah disimpan."
        )
