#!/usr/bin/python

import os
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

JUNOS_HOST = os.environ.get('JUNOS_HOST', '172.25.11.1')
JUNOS_USER = os.environ.get('JUNOS_USER', 'brook')
JUNOS_PASSWD = os.environ.get('JUNOS_PASSWD')

with Device(host=JUNOS_HOST, user=JUNOS_USER, passwd=JUNOS_PASSWD) as dev:
    with Config(dev, mode='private') as cu:
        cu.load('set system services netconf traceoptions file test.log', format='set')
        cu.pdiff()
        cu.commit()
