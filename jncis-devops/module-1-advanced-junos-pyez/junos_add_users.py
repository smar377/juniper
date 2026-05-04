#!/usr/bin/python

import os
from jnpr.junos import Device

# Import the custome Table/View
from myTables.configTables import UserAccountTable
from passlib.hash import sha512_crypt

JUNOS_HOST = os.environ.get('JUNOS_HOST', 'vmx-11')
JUNOS_USER = os.environ.get('JUNOS_USER', 'brook')
NEW_USER_PASSWD = os.environ.get('NEW_USER_PASSWD')

dev = Device(host=JUNOS_HOST, user=JUNOS_USER)
dev.open()

# Create Table instance and associate to the device
ua = UserAccountTable(dev)
ua.username = "nami"
ua.userclass = "super-user"

# Use sha512_crypt to generate a salted hash compatible with Junos
ua.password = sha512_crypt.hash(NEW_USER_PASSWD)

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

