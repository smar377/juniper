#!/usr/bin/python

from jnpr.junos import Device
import jxmlease

if __name__ == '__main__':
    with Device(host='172.25.11.1', user='brook', passwd='onepiece123') as dev:
        parser = jxmlease.EtreeParser()
        route_lxml_element = dev.rpc.get_route_information(table="inet.0")
        ezxml = parser(route_lxml_element)
        for rt in ezxml['route-information']['route-table']['rt']:
            print("Route: {} Protocol: {}".format(rt['rt-destination'], rt['rt-entry']['protocol-name'])) 
