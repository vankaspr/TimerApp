from .config import setup_logging, get_logs_dir
from logging import getLogger

__all__ = [
    "setup_logging",
    "get_logs_dir",
    "get_logger",
]


def get_logger(name: str = None):
    """
    :param name:
    :return:Returns the configured logger.
    If no name is specified, returns the root logger.
    """

    return getLogger(name)
