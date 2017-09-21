🔥 WIP 🔥 wM-Bus implementation in Python
=======================================

This project implements parts of the wireless M-Bus standard, defined in
DIN EN 13757-1 and following. Currently, there is support for
unencrypted short frames (namely CI 0x7a) only. Pull-requests are
welcome.

Installation
------------

PIP
~~~

::

    pip install pywmbus

Manually
~~~~~~~~

::

    git clone https://github.com/jalmeroth/pywmbus.git
    cd pywmbus
    python setup.py install

Dependencies
~~~~~~~~~~~~

-  Python 3
-  `crcmod <http://crcmod.sourceforge.net/>`__ used for checksum
   validation
-  `pyserial <https://github.com/pyserial/pyserial>`__ used for serial
   communication with
   `CUL-Stick <http://shop.busware.de/product_info.php/cPath/1_35/products_id/29>`__

Usage
-----

::

    usage: parser.py [-h] [-d DEBUG] [-r RAW] [-s SERIAL] [-b BAUD]

    optional arguments:
      -h, --help            show this help message and exit
      -d DEBUG, --debug DEBUG
                            Enable debug mode
      -r RAW, --raw RAW     RAW Message
      -s SERIAL, --serial SERIAL
                            Path to serial device
      -b BAUD, --baud BAUD  Baudrate

Example
~~~~~~~

::

    $ ./parser.py -r 34446532121257073804FDEC7A90000000046D280029290C0539351356A0000C13683720014C05806611004C13879649105300426C1F2C326CFFFF236E
    manufacturer: LSE
    device id: 07571212
    device version: 56
    device type: 4 (Heat)
    control info: 0x7a
    access number: 144
    state: Kein Fehler
    configuration: 0
    records (7): [2017-09-09 00:40:00, 133539, 1203768, 116680, 531087, 2016-12-31, 1970-01-01]    

Tested Smart Meters
-------------------

-  Smarvis WFM26 for Heat
-  Smarvis WMC36 for Water
-  Smarvis WMH36 for Hot Water
