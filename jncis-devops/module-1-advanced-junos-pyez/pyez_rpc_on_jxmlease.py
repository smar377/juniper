#!/usr/bin/python

import os
from jnpr.junos import Device
import jxmlease

JUNOS_HOST = os.environ.get('JUNOS_HOST', '172.25.11.1')
JUNOS_USER = os.environ.get('JUNOS_USER', 'brook')
JUNOS_PASSWD = os.environ.get('JUNOS_PASSWD')

if __name__ == '__main__':
    with Device(host=JUNOS_HOST, user=JUNOS_USER, passwd=JUNOS_PASSWD) as dev:
        parser = jxmlease.EtreeParser()
        route_lxml_element = dev.rpc.get_route_information(table="inet.0")
        ezxml = parser(route_lxml_element)
        for rt in ezxml['route-information']['route-table']['rt']:
            print("Route: {} Protocol: {}".format(rt['rt-destination'], rt['rt-entry']['protocol-name'])) 
