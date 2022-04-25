#!/usr/bin/python

from jnpr.junos import Device

# Import the custome Table/View
from myTables.configTables import UserAccountTable
import crypt

dev = Device(host="vmx-11", user="brook")
dev.open()

# Create Table instance and associate to the device
ua = UserAccountTable(dev)
ua.username = "nami"
ua.userclass = "super-user"

# Use 'crypt' to transform password into the salted hash
ua.password = crypt.crypt("onepiece123")

# Generate amd store the configuration data
ua.append()


"""
Lock, load change, commit, and unlock the Junos configuration; this line can be replaced with:
    ua.lock()
    ua.load(merge=True)
    ua.commit(comment="Junos PyEZ commit - adding new user 'nami'")
    ua.unlock()
"""
ua.set(merge=True, comment="Junos PyEZ commit - adding new user 'nami'")

dev.close()

