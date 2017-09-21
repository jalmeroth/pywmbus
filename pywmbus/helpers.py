#!/usr/bin/env python
"""This is a docstring."""
import logging
from .const import LOGGERS
_LOGGER = logging.getLogger(__name__)


def enable_debug(mode):
    """Enable debug logging"""
    for index in LOGGERS:
        # iterate over all available LOGGER
        if (mode >> index) & 0x1:
            logger_name = LOGGERS[index]
            logging.getLogger(logger_name).setLevel(logging.DEBUG)
            _LOGGER.info("Logger: %s enabled", logger_name)
