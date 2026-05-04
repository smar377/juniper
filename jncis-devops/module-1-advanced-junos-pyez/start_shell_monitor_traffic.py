#!/usr/bin/python

import os
from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from pprint import pprint

JUNOS_HOST = os.environ.get('JUNOS_HOST', '172.25.11.1')
JUNOS_USER = os.environ.get('JUNOS_USER', 'brook')
JUNOS_PASSWD = os.environ.get('JUNOS_PASSWD')

dev = Device(host=JUNOS_HOST, user=JUNOS_USER, passwd=JUNOS_PASSWD)
with StartShell(dev) as ss:
    pprint(ss.run('cli -c "monitor traffic interface em0"', this=None, timeout=15))
