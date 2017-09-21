#!/usr/bin/env python
"""This is a docstring."""
import logging
from .serial_device import SerialDevice
_LOGGER = logging.getLogger(__name__)


class CulStick(SerialDevice):
    """docstring for CulStick"""
    def __init__(self, *args, **kwargs):
        super(CulStick, self).__init__(*args, **kwargs)
        # Check for CUL-Stick version
        self.write("V")
        self.process_data(self.read())

        if self.is_cul_stick:
            self.write('X1')
            self.write('X')
            self.read()
            self.write('brs')

    @property
    def is_cul_stick(self):
        """True is stick is CUL868"""
        return self._stick and "CUL" in self._stick

    def process_data(self, data):
        """Process Data from CulStick"""
        if data.startswith('V '):
            self._stick = data[2:]
