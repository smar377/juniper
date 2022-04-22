#!/usr/bin/python

from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from pprint import pprint

dev = Device(host="172.25.11.1", user="brook", passwd="onepiece123")
with StartShell(dev) as ss:
    pprint(ss.run('cli -c "monitor traffic interface em0"', this=None, timeout=15))
