#!/usr/bin/python

import os
from jnpr.junos import Device
from jnpr.junos.op.arp import ArpTable

JUNOS_HOST = os.environ.get('JUNOS_HOST', 'vmx-11')
JUNOS_USER = os.environ.get('JUNOS_USER', 'brook')

with Device(host=JUNOS_HOST, user=JUNOS_USER) as dev:
    arp = ArpTable(dev)
    arp.get()

    for mac in arp:
        print("{}:  {}  {}".format(mac.mac_address, mac.ip_address, mac.interface_name))
    
