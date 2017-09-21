#!/usr/bin/env python
"""This is a docstring."""
import logging
from datetime import date, datetime
from .datagram_field import DIF, DIFE, VIF, VIFE

_LOGGER = logging.getLogger(__name__)


class DataRecord(object):
    """docstring for DataRecord"""
    def __init__(self, data):
        super(DataRecord, self).__init__()
        self._record_start = 2  # DIF + VIF

        self._dat = None
        self._dif = None
        self._vif = None
        self._dife = []
        self._vife = []

        self.data = data
        self._initialize()

    @staticmethod
    def parse(data):
        """Parse Data records"""
        return DataRecord(data)

    @property
    def data(self):
        """Return data."""
        return self._dat

    @data.setter
    def data(self, val):
        """Set Data."""
        self._dat = val

    @property
    def record_data(self):
        """Return data record"""
        return self.data[self.record_data_start:self.record_data_end]

    @property
    def record_data_length(self):
        """Return length of Record data"""
        return self._dif.data_length

    @property
    def record_data_start(self):
        """Return start of Record data"""
        start = self._record_start  # DIF + VIF
        if self._dif.ext:
            start += len(self._dife)
        if self._vif.ext:
            start += len(self._vife)
        return start

    @property
    def record_data_end(self):
        """Return end of Record data"""
        return self.record_data_start + self.record_data_length

    @property
    def record_data_remaining(self):
        """Return remaining data"""
        return self.data[self.record_data_end:]

    def _initialize(self):
        """ Initialize Record object """
        self._dif = DIF(self.data[0])

        if self._dif.ext:
            # for each possible dife
            for index in range(0, 10):
                start = index + 1
                end = start + 1
                dife = DIFE(self.data[start:end])
                self._dife.append(dife)
                if not dife.ext:
                    break
        vif_index = 1 + len(self._dife)  # plus 1 for DIF
        self._vif = VIF(self.data[vif_index])

        if self._vif.ext:
            # for each possible vife
            for index in range(0, 10):
                start = index + 2 + len(self._dife)
                end = start + 1
                vife = VIFE(self.data[start:end])
                self._vife.append(vife)
                if not vife.ext:
                    break

    def date_time_cp32(self):
        """Return date_time from record_data"""
        data = int.from_bytes(self.record_data, byteorder='little')
        minute = data & 0x3f
        hours = (data >> 8) & 0x1f
        day = (data >> 16) & 0x1f
        month = (data >> 24) & 0xf
        year = (((data >> 28) & 0xf) << 3) + ((data >> 21) & 0x7)
        if year >= 0 and year <= 80:
            year += 2000
        datetime_string = "{}-{:02d}-{:02d} {:02d}:{:02d}".format(
            year, month, day, hours, minute
        )
        _LOGGER.debug("DateTime: %s", datetime_string)
        return datetime.strptime(
            datetime_string, '%Y-%m-%d %H:%M').isoformat(sep=' ')

    def date_cp16(self):
        """Return date from record_data"""
        data = int.from_bytes(self.record_data, byteorder='little')
        if data != 0xffff:
            day = data & 0x1f
            month = (data >> 8) & 0xf
            year = (((data >> 12) & 0xf) << 3) + ((data >> 5) & 0x7)
            if year >= 0 and year <= 80:
                year += 2000
        else:
            (year, month, day) = (1970, 1, 1)
        _LOGGER.debug("Date: %d-%d-%d", year, month, day)
        return date(year, month, day).isoformat()

    def __repr__(self):
        """Representation of this record"""
        result = None

        # DIF
        _LOGGER.debug("DIF: %s", "{:08b}".format(self._dif.field_value))
        _LOGGER.debug(
            "DIF_DATA: %s (%s - %d Byte(s))",
            "{:04b}".format(self._dif.data_field),
            self._dif.desc,
            self._dif.data_length
        )
        _LOGGER.debug("DIF_FUNC: %s", "{:02b}".format(self._dif.func_field))
        _LOGGER.debug("DIF_LSB: %s", "{:1b}".format(self._dif.lsb))
        _LOGGER.debug("DIF_EXT: %s", "{:1b}".format(self._dif.ext))

        # DIFE
        for dife in self._dife:
            _LOGGER.debug("DIFE: %s", "{:08b}".format(dife.field_value))
            _LOGGER.debug("DIFE_STORAGE: %s", "{:04b}".format(dife.storage_no))
            _LOGGER.debug("DIFE_TARIFF: %s", "{:02b}".format(dife.tariff))
            _LOGGER.debug("DIFE_SUBUNIT: %s", "{:1b}".format(dife.sub_unit))
            _LOGGER.debug("DIFE_EXT: %s", "{:1b}".format(dife.ext))
        _LOGGER.debug("DIFE_BYTES: %d", len(self._dife))

        # VIF
        _LOGGER.debug(
            "VIF: %s", "{:08b}".format(self._vif.field_value))
        _LOGGER.debug(
            "VIF_DATA: %s (%s)",
            "{:07b}".format(self._vif.data_field),
            self._vif.desc
        )
        _LOGGER.debug(
            "VIF_EXT: %s", "{:1b}".format(self._vif.ext))

        # VIFE
        for vife in self._vife:
            _LOGGER.debug(
                "VIFE: %s", "{:08b}".format(vife.field_value))
            _LOGGER.debug(
                "VIFE_DATA: %s (%s)",
                "{:07b}".format(vife.data_field),
                vife.desc
            )
            _LOGGER.debug(
                "VIFE_EXT: %s", "{:1b}".format(vife.ext))

        # DATA
        _LOGGER.debug("REC_DATA: %s", self.record_data.hex())

        if self._vif.data_field == 0b1101101 and \
                self._dif.data_field == 0b0100:
            # DateTime
            result = self.date_time_cp32()
        elif self._vif.data_field == 0b1101100 and \
                self._dif.data_field == 0b0010:
            # Date
            result = self.date_cp16()
        elif self._dif.data_field in [0b1001, 0b1010, 0b1011, 0b1100, 0b1110]:
            # BCD
            result = "{:x}".format(
                int.from_bytes(self.record_data, byteorder='little'))
        else:
            # All the rest
            result = "{:d}".format(
                int.from_bytes(self.record_data, byteorder='big'))
        return result
