#!/usr/bin/python

from jnpr.junos import Device
from jnpr.junos.utils.config import Config

if __name__ == '__main__':
    with Device(host='172.25.11.1', user='brook', passwd='onepiece123') as dev:
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
