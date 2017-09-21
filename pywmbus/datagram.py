#!/usr/bin/env python
"""This is a docstring."""
import json
import logging
import crcmod
from .exceptions import WMBusChecksumError
from .datagram_field import DatagramField
from .const import (
    A_FIELD, C_FIELD, CI_FIELD, CRC_FIELD, L_FIELD, M_FIELD, ID_FIELD
)

_LOGGER = logging.getLogger(__name__)
_CRC_16 = crcmod.predefined.mkCrcFun("crc-16-en-13757")


class Datagram(object):
    """docstring for Datagram"""
    def __init__(self, data, *args, **kwargs):
        super(Datagram, self).__init__()
        _LOGGER.debug("Unused arguments: %s / %s", args, kwargs)
        self._data = {
            '_crc': []
        }

        self.data['_l_field'] = DatagramField(L_FIELD, data[0])
        self.data['_c_field'] = DatagramField(C_FIELD, data[1])
        self.data['_m_field'] = DatagramField(M_FIELD, data[2:4])
        self.data['_a_field_id'] = DatagramField(ID_FIELD, data[4:8])
        self.data['_a_field_version'] = DatagramField(A_FIELD, data[8:9])
        self.data['_a_field_type'] = DatagramField(A_FIELD, data[9:10])
        self.data['_crc'].append(DatagramField(CRC_FIELD, data[10:12]))

        if self.data['_c_field'].field_value == 0xc4:
            # Data in between 12:32 is still unknown
            _LOGGER.info("This type of Datagram is experimental")
            self.data['_ci_field'] = DatagramField(CI_FIELD, data[32:33])
        else:
            self.data['_ci_field'] = DatagramField(CI_FIELD, data[12:13])

        if self.data['_crc'][0].field_value != _CRC_16(data[0:10]):
            raise WMBusChecksumError("Checksum 0 mismatch")

    @staticmethod
    def parse(data):
        """Parse data and return Datagram object"""
        _LOGGER.debug("parsing data: %s", data)
        return Datagram(data)

    @property
    def is_headless(self):
        """Is a headless frame"""
        return self.control_info in [0x69, 0x70, 0x71, 0x78, 0x79]

    @property
    def is_short(self):
        """Is a short frame"""
        return self.control_info in [0x6A, 0x6E, 0x74, 0x7A, 0x7B, 0x7D, 0x7F]

    @property
    def is_long(self):
        """Is a long frame"""
        return self.control_info in [0x6B, 0x6F, 0x72, 0x73, 0x75, 0x7C, 0x7E]

    @property
    def length(self):
        """Return length field"""
        return self.data.get('_l_field').field_value

    @property
    def command(self):
        """Return command field"""
        return self.data.get('_c_field').field_value

    @property
    def data(self):
        """Return data attribut"""
        return self._data

    @data.setter
    def data(self, data):
        """Set data attribut"""
        _LOGGER.debug("set data: %s", data)
        self._data = data

    @property
    def control_info(self):
        """Return Control Info"""
        return self.data.get('_ci_field').field_value

    @property
    def device_id(self):
        """Return the Device Id"""
        return self.data.get('_a_field_id').field_value

    @property
    def device_version(self):
        """Return the Device version"""
        return self.data.get('_a_field_version').field_value

    @property
    def device_type(self):
        """Return the Device type"""
        return self.data.get('_a_field_type').field_value

    @property
    def manufacturer(self):
        """Return the Manufacturer Id"""
        return "{0}{1}{2}".format(
            chr(((self.data.get('_m_field').field_value >> 10) & 0x001F) + 64),
            chr(((self.data.get('_m_field').field_value >> 5) & 0x001F) + 64),
            chr(((self.data.get('_m_field').field_value) & 0x001F) + 64)
        )

    def __repr__(self):
        result = {}
        for obj in self._data:
            if obj == "_crc":
                for key, val in enumerate(self._data[obj]):
                    result["{}_{}".format(obj, key)] = val.field_value
            else:
                result[obj] = self._data[obj].field_value
        return json.dumps(result)
