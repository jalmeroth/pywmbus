#!/usr/bin/env python
"""This is a docstring."""
import logging
from .const import (
    A_FIELD, ACC_FIELD, CI_FIELD,
    CRC_FIELD, M_FIELD, ID_FIELD,
    STATE_FIELD, FIELD_TYPES, STATES,
    CONF_FIELD, DIF_FIELD, DIFE_FIELD,
    VIF_FIELD, VIFE_FIELD, DIFS, VIFS,
    VIFES
)
_LOGGER = logging.getLogger(__name__)


class DatagramField(object):
    """docstring for DatagramField"""
    def __init__(self, field_type, field_value):
        super(DatagramField, self).__init__()
        self._field_type = None
        self._field_value = None

        self.field_type = field_type

        if self.field_type in [M_FIELD]:
            self.field_value = int.from_bytes(field_value, byteorder='little')
        elif self.field_type in [A_FIELD,
                                 ACC_FIELD,
                                 CI_FIELD,
                                 CRC_FIELD,
                                 STATE_FIELD,
                                 CONF_FIELD]:
            self.field_value = int.from_bytes(field_value, byteorder='big')
        # elif self.field_type in [CRC_FIELD]:
        #     self.field_value = field_value.hex()
        elif self.field_type in [ID_FIELD]:
            # reversed order, hex-string
            self.field_value = field_value[::-1].hex()
        else:
            self.field_value = field_value

    @property
    def field_type(self):
        """Get field_type"""
        return self._field_type

    @field_type.setter
    def field_type(self, val):
        """Set field_type"""
        _LOGGER.debug("field_type: %s", val)
        self._field_type = val

    @property
    def field_value(self):
        """Get field_value"""
        result = self._field_value
        if self.field_type == A_FIELD and self._field_value in FIELD_TYPES:
            # device type
            result = "{} ({})".format(
                self._field_value, FIELD_TYPES[self._field_value])
        elif self.field_type == STATE_FIELD and self._field_value in STATES:
            # state
            result = STATES[self._field_value]
        else:
            pass
        return result

    @field_value.setter
    def field_value(self, val):
        """Set field_value"""
        _LOGGER.debug("field_value: %s", val)
        self._field_value = val


class DIF(DatagramField):
    """docstring for DIF"""
    def __init__(self, *args):
        super(DIF, self).__init__(DIF_FIELD, *args)

        self._meta_data = DIFS.get(self.data_field, {
            "desc": "UNKNOWN",
            "length": 0,
        })

    @property
    def data_field(self):
        """Return data_field"""
        return self.field_value & 0xf

    @property
    def data_length(self):
        """Return data_length"""
        return self._meta_data["length"]

    @property
    def func_field(self):
        """Return func_field"""
        return (self.field_value >> 4) & 0x3

    @property
    def lsb(self):
        """Return lsb"""
        return (self.field_value >> 6) & 0x1

    @property
    def ext(self):
        """Return ext"""
        return (self.field_value >> 7) & 0x1

    @property
    def desc(self):
        """Return desc"""
        return self._meta_data["desc"]


class DIFE(DatagramField):
    """docstring for DIFE"""
    def __init__(self, field_value, *args):
        field_value = int.from_bytes(field_value, byteorder='big')
        super(DIFE, self).__init__(DIFE_FIELD, field_value, *args)

    @property
    def storage_no(self):
        """Return storage no."""
        return self.field_value & 0xf

    @property
    def tariff(self):
        """Return tariff"""
        return (self.field_value >> 4) & 0x3

    @property
    def sub_unit(self):
        """Return sub_unit"""
        return (self.field_value >> 6) & 0x1

    @property
    def ext(self):
        """Return ext"""
        return (self.field_value >> 7) & 0x1


class VIF(DatagramField):
    """docstring for VIF"""
    def __init__(self, *args):
        super(VIF, self).__init__(VIF_FIELD, *args)

        self._meta_data = VIFS.get(self.data_field, {
            "desc": "UNKNOWN",
        })

    @property
    def data_field(self):
        """Return data_field"""
        return self.field_value & 0x7f

    @property
    def ext(self):
        """Return ext"""
        return (self.field_value >> 7) & 0x1

    @property
    def desc(self):
        """Return desc"""
        return self._meta_data["desc"]


class VIFE(DatagramField):
    """docstring for VIFE"""
    def __init__(self, field_value, *args):
        field_value = int.from_bytes(field_value, byteorder='big')
        super(VIFE, self).__init__(VIFE_FIELD, field_value, *args)

        self._meta_data = VIFES.get(self.data_field, {
            "desc": "UNKNOWN",
        })

    @property
    def data_field(self):
        """Return data_field"""
        return self.field_value & 0x7f

    @property
    def ext(self):
        """Return ext"""
        return (self.field_value >> 7) & 0x1

    @property
    def desc(self):
        """Return desc"""
        return self._meta_data["desc"]
