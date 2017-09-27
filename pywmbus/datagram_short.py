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

    csum_len = 2
    head_len = 9
    body_len = data[0] - head_len
    remainder = body_len % 16
    times = int((body_len - remainder) / 16)
    times += 1 if remainder > 0 else 0
    # +1 for header crc, +1 for L-field
    full_len = ((times + 1) * csum_len) + data[0] + 1

    _LOGGER.debug("%d: %d, %d = %d", len(data), times, remainder, full_len)

    if len(data) < full_len:
        raise WMBusDataLengthError("Not enough input data")

    # header consists of 10 bytes
    end = 10
    # copy over header but leave L-Field aside
    new_data = data[1:end]

    for i in range(0, times):
        start = end + 2
        # last round, if remainder
        if remainder > 0 and i == times - 1:
            # calculate missing bytes
            end = start + remainder
        else:
            end = start + 16  # 16 bytes data

        part = data[start:end]

        if part:
            # self.data['_crc'].append(DatagramField(CRC_FIELD, data[10:12]))
            _LOGGER.debug("%d %d:%d %s", i, start, end, part.hex())

            csum_calc = _CRC_16(part)
            csum_data = int.from_bytes(data[end:end + 2], byteorder="big")

            _LOGGER.debug("csum: %s vs. %s", hex(csum_calc), hex(csum_data))

            if csum_calc != csum_data:
                raise WMBusChecksumError("Checksum {} mismatch".format(i))

            new_data += data[start:end]

    if data[0] != len(new_data):
        raise WMBusDataLengthError("Not enough output data")

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
