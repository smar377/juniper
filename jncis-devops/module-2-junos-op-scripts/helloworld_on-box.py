from jnpr.junos import Device
from pprint import pprint

if __name__ == '__main__':
    with Device() as dev:
        pprint(dev.facts)
