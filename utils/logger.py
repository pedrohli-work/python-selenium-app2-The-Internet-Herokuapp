import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# Define the project root directory (two levels above this file)
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Define the directory for log files and ensure it exists
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str = "tests", level_str: str = "INFO") -> logging.Logger:
    """
    Create and configure a logger instance with console and file handlers.

    Features:
        - Console logging with simple format.
        - File logging with detailed format and rotation (max 10MB per file, 10 backups).
        - Logging level can be specified via `level_str`, default is INFO.

    Args:
        name (str): Name of the logger. Defaults to "tests".
        level_str (str): Logging level as string (e.g., "DEBUG", "INFO"). Defaults to "INFO".

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Return existing logger if already configured
    if logger.handlers:
        return logger

    # Determine logging level
    level = getattr(logging, level_str.upper(), logging.INFO)
    logger.setLevel(level)

    # Console formatter and handler
    console_fmt = logging.Formatter("%(levelname)s | %(message)s")
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(console_fmt)

    # File formatter and handler with rotation
    file_fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    )
    log_file = os.path.join(LOG_DIR, "run.log")
    fh = RotatingFileHandler(
        log_file, 
        maxBytes=10_000_000, 
        backupCount=10, 
        encoding="utf-8"
        )
    fh.setLevel(level)
    fh.setFormatter(file_fmt)

    # Attach handlers
    logger.addHandler(ch)
    logger.addHandler(fh)

    # Prevent messages from propagating to the root logger
    logger.propagate = False

    return logger
