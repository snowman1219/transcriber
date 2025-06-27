"""Centralized logging configuration for the transcriber package."""

import logging
import sys
from pathlib import Path


def setup_logger(
    name: str | None = None,
    level: int = logging.INFO,
    log_file: Path | None = None,
    console_output: bool = True,
) -> logging.Logger:
    """Set up a logger with consistent formatting.

    Args:
        name: Logger name. If None, returns root logger
        level: Logging level (default: INFO)
        log_file: Optional file path to write logs
        console_output: Whether to output to console (default: True)

    Returns:
        Configured logger instance

    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)-8s] %(message)s [%(pathname)s:%(lineno)d]", datefmt="%Y-%m-%d %H:%M:%S")

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
