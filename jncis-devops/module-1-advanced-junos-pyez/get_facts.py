#!/usr/bin/python

from jnpr.junos import Device
from pprint import pprint

if __name__ == '__main__':
    dev = Device(host='172.25.11.1', user='brook', passwd='onepiece123')
    dev.open()
    pprint(dev.facts)
    dev.close

