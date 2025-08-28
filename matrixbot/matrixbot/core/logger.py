import logging
import sys


class Logger(logging.Logger):
    """Custom logger class for Matrix bot."""

    def __init__(
        self, name, level="INFO", filename="matrixbot.log", save_logfile=False
    ):
        super().__init__(name, level)
        self.filename = filename
        self.save_logfile = save_logfile
        self.file_handler = None
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(level)
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.console_handler.setFormatter(self.formatter)
        self.addHandler(self.console_handler)

        if save_logfile:
            self.set_filename(filename)

    def set_filename(self, filename):
        self.filename = filename
        if self.save_logfile:
            self.file_handler = logging.FileHandler(filename)
            self.file_handler.setLevel(self.level)
            self.file_handler.setFormatter(self.formatter)
            self.addHandler(self.file_handler)

    def set_level(self, level):
        self.setLevel(level)
        if self.file_handler:
            self.file_handler.setLevel(level)
