#!/usr/bin/env python
"""This is a docstring."""
import logging
import crcmod
from .datagram import Datagram
from .datagram_field import DatagramField
from .datagram_record import DataRecord
from .exceptions import WMBusChecksumError, WMBusDataLengthError
from .const import (
    ACC_FIELD, STATE_FIELD, CONF_FIELD
)
_LOGGER = logging.getLogger(__name__)

_CRC_16 = crcmod.predefined.mkCrcFun("crc-16-en-13757")


def sans_checksum(data):
    """Verify checksums and remove them from data"""
    _LOGGER.debug("data: %s (%d)", data.hex(), len(data))

    # header consists of 10 bytes
    end = 10
    # but leave L-Field aside
    new_data = data[1:end]
    # each 16th byte comes a checksum
    times = int((len(data) / 16))

    for i in range(1, times):
        start = end + 2
        end = start + 16
        _LOGGER.debug(
            "%d:%d %s",
            start,
            end,
            data[start:end].hex()
        )
        # self.data['_crc'].append(DatagramField(CRC_FIELD, data[10:12]))
        csum_calc = _CRC_16(data[start:end])
        csum_data = int.from_bytes(data[end:end + 2], byteorder="big")
        _LOGGER.debug(
            "csum: %s vs. %s",
            hex(csum_calc),
            hex(csum_data)
        )

        if csum_calc != csum_data:
            raise "Checksum {} mismatch".format(i)

        new_data += data[start:end]
    # last 2 bytes are a checksum too
    start = end + 2
    end = len(data) - 2

    csum_calc = _CRC_16(data[start:end])
    csum_data = int.from_bytes(data[-2:], byteorder="big")

    if csum_calc != csum_data:
        raise WMBusChecksumError("Checksum mismatch")

    # append all the rest that is left
    new_data += data[start:end]
    if data[0] != len(new_data):
        raise WMBusDataLengthError()

    _LOGGER.debug("new_data: %s (%d)", new_data.hex(), len(new_data))
    return new_data


class ShortDatagram(Datagram):
    """docstring for ShortDatagram"""
    def __init__(self, data, *args, **kwargs):
        super(ShortDatagram, self).__init__(data, *args, **kwargs)

        self.data['_acc_field'] = DatagramField(ACC_FIELD, data[13:14])
        self.data['_state_field'] = DatagramField(STATE_FIELD, data[14:15])
        self.data['_conf_field'] = DatagramField(CONF_FIELD, data[15:17])

        self._new_data = sans_checksum(data)

        self.records = []
        remaining = self._new_data[14:]
        _LOGGER.debug("remaining: %s", remaining.hex())
        while remaining:
            try:
                record = DataRecord(remaining)
            except IndexError:
                _LOGGER.warning("Ignoring remaining data: %s", remaining.hex())
                remaining = None
            else:
                self.records.append(record)
                remaining = record.record_data_remaining

    @staticmethod
    def parse(data):
        return ShortDatagram(data)

    @property
    def state(self):
        """Return state"""
        return self.data.get('_state_field').field_value

    @property
    def access_no(self):
        """Return access number"""
        return self.data.get('_acc_field').field_value

    @property
    def configuration(self):
        """Return configuration"""
        return self.data.get('_conf_field').field_value
