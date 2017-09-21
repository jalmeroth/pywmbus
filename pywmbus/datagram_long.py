#!/usr/bin/env python
"""This is a docstring."""
import logging
from .datagram import Datagram
_LOGGER = logging.getLogger(__name__)


class LongDatagram(Datagram):
    """docstring for LongDatagram"""
    def __init__(self, data, *args, **kwargs):
        super(LongDatagram, self).__init__(data, *args, **kwargs)
        _LOGGER.warning("Not implemented.")
