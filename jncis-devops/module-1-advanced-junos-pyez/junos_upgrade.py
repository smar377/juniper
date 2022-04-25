#!/usr/bin/python

from jnpr.junos import Device
from jnpr.junos.utils.scp import SCP
from jnpr.junos.utils.sw import SW
from jnpr.junos.utils.fs import FS
from jnpr.junos.exception import *
from time import sleep
import os

TARGET_VERSION = "18.3R1.9"
IMAGE_FILE = "junos-vmx-x86-64-18.3R1.9.trz"
REMOTE_PATH = "/var/tmp/"

def main():
    dev = Device(host="172.25.11.1", user="brook", passwd="onepiece123", normalize=True)
    dev.open()

    if dev.facts['junos_info']['re0']['text'] == TARGET_VERSION:
        print("Device OS version is already the target version")
        exit(1)

    fs = FS(dev)
    bytes_free = fs.storage_usage()['/dev/ad0s1f']['avail_block']*512
    print("bytes free: ", bytes_free)
    file_size = os.stat(IMAGE_FILE).st_size
    print("We have %d bytes free, image size is %d" % (bytes_free, file_size))
    if bytes_free < file_size:
        print("Error: Not enough space on device")
        exit(1)

    print("Copying image to the device...")
    with SCP(dev, progress=True) as scp:
        scp.put(IMAGE_FILE, remote_path=REMOTE_PATH)

    print("Installing package...")
    sw = SW(dev)
    install_result = sw.install(package=REMOTE_PATH+IMAGE_FILE, no_copy=True, validate=False, progress=True)
    
    if not install_result:
        print("Installation error, exiting...")
        exit(1)

    print("Rebooting...")
    sw.reboot()

    for _ in range(20):
        print("Waiting for device reboot...")
        sleep(50)
        try:
            dev.open(auto_probe=10)
            ver = dev.facts['junos_info']['re0']['text']
        except (ProbeError, ConnectError):
            continue
        dev.close()
        break
    else:
        print("The device did not complete reboot in time, please check.")
        exit(1)

    if ver == TARGET_VERSION:
        print("Reboot complete. Installation successfull.")
    else:
        print("Reboot complete, but something went wrong!")
        exit(1)

if __name__ == "__main__":
    main()


