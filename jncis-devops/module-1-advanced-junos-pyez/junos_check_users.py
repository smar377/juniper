#!/usr/bin/python

from jnpr.junos import Device
from myTables.configTables import UserAccountTable

dev = Device(host="vmx-11", user="brook")
ua = UserAccountTable(dev)
dev.open()

ua.get()
for account in ua:
    print("Username: {}\nUser class: {}".format(account.username, account.userclass))
    
dev.close()

