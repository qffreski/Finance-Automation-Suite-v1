import psutil
import platform


class PerformanceDetector:
    """
    Detect system performance dan adjust automation speed.
    """

    def __init__(self, logger=None):
        self.logger = logger

    # =====================================================
    # GET SYSTEM INFO
    # =====================================================

    def get_cpu_count(self):
        """Get jumlah CPU cores."""
        return psutil.cpu_count(logical=False) or 1

    def get_ram_gb(self):
        """Get total RAM dalam GB."""
        return psutil.virtual_memory().total / (1024 ** 3)

    def get_ram_percent(self):
        """Get persentase RAM yang digunakan."""
        return psutil.virtual_memory().percent

    def get_cpu_percent(self):
        """Get persentase CPU yang digunakan (average 1 detik)."""
        return psutil.cpu_percent(interval=1)

    # =====================================================
    # DETECT PROFILE
    # =====================================================

    def detect_profile(self):
        """
        Detect performance profile: 'slow', 'normal', 'fast'
        
        Slow   : CPU cores <= 2 OR RAM <= 4GB OR RAM usage > 80%
        Fast   : CPU cores >= 8 AND RAM >= 16GB AND RAM usage < 50%
        Normal : Lainnya
        """

        cpu_cores = self.get_cpu_count()
        ram_gb = self.get_ram_gb()
        ram_percent = self.get_ram_percent()

        if self.logger:
            self.logger.info(f"System: CPU={cpu_cores} cores, RAM={ram_gb:.1f}GB, Usage={ram_percent}%")

        # SLOW
        if cpu_cores <= 2 or ram_gb <= 4 or ram_percent > 80:
            profile = "slow"

        # FAST
        elif cpu_cores >= 8 and ram_gb >= 16 and ram_percent < 50:
            profile = "fast"

        # NORMAL
        else:
            profile = "normal"

        if self.logger:
            self.logger.info(f"Performance Profile: {profile}")

        return profile

    # =====================================================
    # GET TIMING MULTIPLIER
    # =====================================================

    def get_timing_multiplier(self, profile):
        """
        Get multiplier untuk timing delays.
        
        Fast   : 0.5x (lebih cepat)
        Normal : 1.0x (standar)
        Slow   : 1.5x (lebih lambat)
        """

        multipliers = {
            "fast": 0.5,
            "normal": 1.0,
            "slow": 1.5
        }

        return multipliers.get(profile, 1.0)

    # =====================================================
    # GET OPTIMIZED CONFIG
    # =====================================================

    def get_optimized_config(self):
        """
        Get default config dengan timing yang sudah di-optimize.
        """

        profile = self.detect_profile()
        multiplier = self.get_timing_multiplier(profile)

        config = {
            "profile": profile,
            "multiplier": multiplier,

            # ============================================
            # AUTOMATION (CORE)
            # ============================================

            "click_delay": 0.8 * multiplier,
            "typing_speed": 0.05 * multiplier,
            "upload_speed": 250,
            "retry": 3,

            # ============================================
            # GLOBAL DELAY
            # ============================================

            "move_duration": 0.25 * multiplier,      # Mouse movement
            "typing_delay": 0.2 * multiplier,        # Typing dalam field
            "dialog_delay": 1.5 * multiplier,        # Dialog open
            "search_delay": 3.0 * multiplier,        # Search operation
            "attachment_delay": 2.0 * multiplier,    # Attachment dialog
            "save_delay": 1.0 * multiplier,          # Save operation
            "countdown_delay": 1.0 * multiplier,     # Calibration countdown

            # ============================================
            # PDF
            # ============================================

            "pdf_dir": "",

            # ============================================
            # CALIBRATION
            # ============================================

            "positions": {}
        }

        return config
