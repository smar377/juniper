#!/usr/bin/python

from jnpr.junos import Device

if __name__ == '__main__':
    with Device(host='172.25.11.1', user='brook', passwd='onepiece123') as dev:
        route_lxml_element = dev.rpc.get_route_information(table="inet.0")
        list_of_routes = route_lxml_element.findall('.//rt')
        for route in list_of_routes:
            print("Route: {} Protocol: {}".format(route.findtext('rt-destination'), route.findtext('rt-entry/protocol-name'))) 
