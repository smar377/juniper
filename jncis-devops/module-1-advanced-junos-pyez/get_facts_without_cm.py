#!/usr/bin/python

import os
from jnpr.junos import Device
from pprint import pprint

JUNOS_HOST = os.environ.get('JUNOS_HOST', '172.25.11.1')
JUNOS_USER = os.environ.get('JUNOS_USER', 'brook')
JUNOS_PASSWD = os.environ.get('JUNOS_PASSWD')

if __name__ == '__main__':
    dev = Device(host=JUNOS_HOST, user=JUNOS_USER, passwd=JUNOS_PASSWD)
    dev.open()
    pprint(dev.facts)
    dev.close()
