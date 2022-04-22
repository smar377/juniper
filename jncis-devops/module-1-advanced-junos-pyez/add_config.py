#!/usr/bin/python

from jnpr.junos import Device
from jnpr.junos.utils.config import Config

with Device(host='172.25.11.1', user='brook', passwd='onepiece123') as dev:
    with Config(dev, mode='private') as cu:
        cu.load('set system services netconf traceoptions file test.log', format='set')
        cu.pdiff()
        cu.commit()
