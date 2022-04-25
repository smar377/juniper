#!/usr/bin/python

from jnpr.junos import Device
from jnpr.junos.op.arp import ArpTable

with Device(host="vmx-11", user="brook") as dev:
    arp = ArpTable(dev)
    arp.get()

    for mac in arp:
        print("{}:  {}  {}".format(mac.mac_address, mac.ip_address, mac.interface_name))
    
