#!/usr/bin/python

import os
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import yaml

JUNOS_USER = os.environ.get('JUNOS_USER', 'brook')

junos_hosts = ['vmx-11', 'vmx-12']

for host in junos_hosts:
    filename = host + '.yml'
    with open(filename, 'r') as fh:
        data = yaml.safe_load(fh)
    try:
        with Device(host=host, user=JUNOS_USER) as dev:
            try:
                with Config(dev, mode="exclusive") as conf:
                    conf.load(template_path="case1.j2", template_vars=data, format="text")
                    conf.pdiff()
                    conf.commit()
            except LockError:
                print("The config database was locked!")
    except ConnectError:
        print("Connection error!")
