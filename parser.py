#!/usr/bin/env python
"""This is a docstring."""
import time
import logging
import argparse
import pywmbus
from pywmbus.cul_stick import CulStick
from pywmbus.helpers import enable_debug
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
_LOGGER = logging.getLogger(__name__)


def parse(data):
    """Parse wM-Bus Frame"""
    if data.startswith('b'):
        data = data[1:]

    try:
        data = bytearray().fromhex(data)
    except ValueError as err:
        _LOGGER.error("Error: %s", err)
        _LOGGER.error("Input: %s", data)
        data = None

    if data:
        telegram = pywmbus.parse(data)
        print("\nmanufacturer: {}".format(telegram.manufacturer))
        print("device id: {}".format(telegram.device_id))
        print("device version: {}".format(telegram.device_version))
        print("device type: {}".format(telegram.device_type))
        print("control info: {}".format(hex(telegram.control_info)))
        if telegram.is_short:
            print("access number: {}".format(telegram.access_no))
            print("state: {}".format(telegram.state))
            print("configuration: {}".format(telegram.configuration))
            print("records ({}): {}".format(
                len(telegram.records), telegram.records))


def main():
    """Main loop"""

    # initialize Arg-parser
    parser = argparse.ArgumentParser()
    # setup Arg-parser
    parser.add_argument(
        '-d', '--debug', type=int, help='Enable debug mode')
    parser.add_argument(
        '-r', '--raw', action="append", type=str, help='RAW Message')
    parser.add_argument(
        '-s', '--serial', type=str, help='Path to serial device')
    parser.add_argument(
        '-b', '--baud', default=9600, type=int, help='Baudrate')

    # parse arguments
    args, unknown = parser.parse_known_args()

    if args.debug:
        enable_debug(args.debug)

    _LOGGER.debug("args: " + str(args) + " unknown: " + str(unknown))

    if args.serial:
        device = CulStick(args.serial, args.baud)
        while True:
            data = device.read()
            if data and data.startswith('b'):
                parse(data[1:])
            time.sleep(1)
    elif args.raw:
        for raw in args.raw:
            parse(raw)
    else:
        parser.print_usage()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Quitting")
