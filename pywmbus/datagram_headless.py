#!/usr/bin/env python
"""This is a docstring."""
import logging
from .datagram import Datagram
_LOGGER = logging.getLogger(__name__)


class HeadlessDatagram(Datagram):
    """docstring for HeadlessDatagram"""
    def __init__(self, data, *args, **kwargs):
        super(HeadlessDatagram, self).__init__(data, *args, **kwargs)
        _LOGGER.warning("Not implemented.")
