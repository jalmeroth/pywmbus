#!/usr/bin/env python
"""This is a docstring."""
import logging
from .datagram import Datagram
from .datagram_headless import HeadlessDatagram
from .datagram_short import ShortDatagram
from .datagram_long import LongDatagram
from .exceptions import WMBusTypeError
_LOGGER = logging.getLogger(__name__)


def parse(data):
    """Parse frame data"""
    if not isinstance(data, bytearray):
        raise WMBusTypeError("ERROR")

    try:
        telegram = Datagram(data)
    except Exception as err:
        raise err

    result = telegram

    if telegram.is_headless:
        result = HeadlessDatagram(data)
    elif telegram.is_short:
        result = ShortDatagram(data)
    elif telegram.is_long:
        result = LongDatagram(data)
    else:
        _LOGGER.debug("Unknown Datagram: %s", data.hex())

    return result
