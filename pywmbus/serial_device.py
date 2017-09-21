#!/usr/bin/env python
"""This is a docstring."""
import time
import logging
import serial
_LOGGER = logging.getLogger(__name__)

SERIALDEV = "/dev/cu.usbmodem1411"
BAUDRATE = 9600
SLEEPING = 1
LINE_END = "\r\n"


class SerialDevice(object):
    """docstring for SerialDevice"""
    def __init__(self, serial_dev=SERIALDEV, baud_rate=BAUDRATE):
        super(SerialDevice, self).__init__()
        _LOGGER.debug("Serial: %s (%d) init.", serial_dev, baud_rate)
        self._stick = None
        try:
            self.ser = serial.Serial(serial_dev, baud_rate)
            # number of bits per bytes
            self.ser.bytesize = serial.EIGHTBITS
            # set parity check: no parity
            self.ser.parity = serial.PARITY_NONE
            # number of stop bits
            self.ser.stopbits = serial.STOPBITS_ONE

            _LOGGER.debug("isOpen: %s", self.ser.isOpen())

        except serial.serialutil.SerialException as err:
            raise err
        else:
            self.ser.flush()

    def write(self, data):
        """Write data to SerialDevice"""
        _LOGGER.debug("SEND: %s (%s)", data, len(data))
        if data and not data.endswith(LINE_END):
            data += LINE_END
        self.ser.write(data.encode('UTF-8'))
        time.sleep(SLEEPING)

    def read(self):
        """Reads data from SerialDevice"""
        data = None
        while self.ser.inWaiting() > 0:
            data = self.ser.read(self.ser.inWaiting())
            data = data.decode('UTF-8').strip()
            _LOGGER.debug("DATA: %s (%s)", data, len(data))
        return data

    def process_data(self, data):
        """Process Data from SerialDevice"""
        raise NotImplementedError()
