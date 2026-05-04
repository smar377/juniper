#!/usr/bin/python

import os
from jnpr.junos import Device
from myTables.configTables import UserAccountTable

JUNOS_HOST = os.environ.get('JUNOS_HOST', 'vmx-11')
JUNOS_USER = os.environ.get('JUNOS_USER', 'brook')

dev = Device(host=JUNOS_HOST, user=JUNOS_USER)
ua = UserAccountTable(dev)
dev.open()

ua.get()
for account in ua:
    print("Username: {}\nUser class: {}".format(account.username, account.userclass))
    
dev.close()

