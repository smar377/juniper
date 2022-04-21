#!/usr/bin/python

from jnpr.junos import Device

if __name__ == '__main__':
    dev = Device(host='172.25.11.1', user='brook', passwd='onepiece123')
    dev.open()
    print(dev.facts)
    dev.close

