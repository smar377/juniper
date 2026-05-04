#!/usr/bin/python

import os
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

JUNOS_HOST = os.environ.get('JUNOS_HOST', '172.25.11.1')
JUNOS_USER = os.environ.get('JUNOS_USER', 'brook')
JUNOS_PASSWD = os.environ.get('JUNOS_PASSWD')

if __name__ == '__main__':
    with Device(host=JUNOS_HOST, user=JUNOS_USER, passwd=JUNOS_PASSWD) as dev:
        conf = Config(dev)
        data = """interfaces {
            ge-0/0/1 {
                unit 0 {
                    family inet {
                        address 172.17.1.150/24;
                    }
                }
            }
        }"""
        conf.lock()
        conf.load(data, format='text')
        conf.pdiff()
        if conf.commit_check():
            conf.commit()
        else:
            conf.rollback()
        conf.unlock()
