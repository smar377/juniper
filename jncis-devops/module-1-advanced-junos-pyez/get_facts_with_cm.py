from jnpr.junos import Device
from pprint import pprint

if __name__ == '__main__':
    with Device(host='172.25.11.1', user='brook', passwd='onepiece123') as dev:
        pprint(dev.facts)
