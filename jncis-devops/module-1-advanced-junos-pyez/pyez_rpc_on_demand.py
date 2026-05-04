#!/usr/bin/python

import os
from jnpr.junos import Device

JUNOS_HOST = os.environ.get('JUNOS_HOST', '172.25.11.1')
JUNOS_USER = os.environ.get('JUNOS_USER', 'brook')
JUNOS_PASSWD = os.environ.get('JUNOS_PASSWD')

if __name__ == '__main__':
    with Device(host=JUNOS_HOST, user=JUNOS_USER, passwd=JUNOS_PASSWD) as dev:
        route_lxml_element = dev.rpc.get_route_information(table="inet.0")
        list_of_routes = route_lxml_element.findall('.//rt')
        for route in list_of_routes:
            print("Route: {} Protocol: {}".format(route.findtext('rt-destination'), route.findtext('rt-entry/protocol-name'))) 
