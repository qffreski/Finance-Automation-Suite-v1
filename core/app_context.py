from config.config_manager import ConfigManager
from config.calibration import CalibrationTool
from core.logger import Logger

from modules.file_selector import FileSelector
from modules.kingdee_automation import KingdeeAutomation


class AppContext:

    def __init__(self):

        # =====================================================
        # CORE
        # =====================================================

        self.logger = Logger()
        
        # Pass logger ke ConfigManager untuk performance detection logging
        self.config = ConfigManager(logger=self.logger)

        self.logger.title("Finance Automation Suite Initialized")
        self.logger.info(f"Performance Profile: {self.config.performance_profile}")
        self.logger.info(f"Timing Multiplier: {self.config.get_float('timing_multiplier', 1.0)}x")

        # =====================================================
        # CALIBRATION
        # =====================================================

        self.calibration = CalibrationTool(
            config=self.config,
            logger=self.logger
        )

        # =====================================================
        # FILE SELECTOR
        # =====================================================

        self.file_selector = FileSelector(
            config=self.config,
            logger=self.logger
        )

        # =====================================================
        # AUTOMATION
        # =====================================================

        self.automation = KingdeeAutomation(
            config=self.config,
            logger=self.logger,
            file_selector=self.file_selector
        )
