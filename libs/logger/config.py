import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path



def get_logs_dir():
    """Determines the correct folder for the logs"""
    if getattr(sys, "frozen", False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).parent.parent.parent

    logs_dir = base_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir


def setup_logging():
    """Root Logger Setup"""
    logs_dir = get_logs_dir()
    log_file = logs_dir / "app.log"

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    def handle_exceptions(exp_type, exc_value, exc_traceback):
        logger.critical(
            "Unhandled exception",
            exc_info=(exp_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exceptions

    logger.info("Logging system initialized")

