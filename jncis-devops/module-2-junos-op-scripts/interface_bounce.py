from jnpr.junos import Device 
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from time import sleep
import argparse

# Define the arguments dictionary
arguments = {
    "interface": "Name of the interface to disable/enable",
    "delay": "Time to wait before enabling the interface (seconds)"
}

"""
Define a change_config function that accepts three parameters:
    1. Config instance
    2. Junos set-command configuration and
    3. Human-readable description of the operation
"""
def change_config(dev_cfg, set_cmds, op_descr):
    print op_descr + " : Locking the configuration"
    try:
        # Lock configuration and process LockError exception
        dev_cfg.lock()
    except LockError:
        print("Error: Unable to lock configuration")
        # Return False if config change was not successful
        return False

    print op_descr + " : Loading configuration changes"
    try:
        dev_cfg.load(set_cmds, format="set")
    # Load configuration and process ConfigLoadError exception
    except ConfigLoadError as err:
        print "Unable to load configuration changes: \n" + err
        print "Unlocking configuration"
        try:
            # In case load was not successfull, try to unlocak if possible
            dev_cfg.unlock()
        except UnlockError:
            print "Error: Unable to unlock configuration"
        return False
    
    print op_descr + " : Committing the configuration"
    try:
        dev_cfg.commit()
    # Commit configuration and process CommitError exception
    except CommitError:
        print "Error: Unable to commit configuration"
        print "Unlocking the configuration"
        try:
            # In case load was not successfull, try to unlocak if possible
            dev_cfg.unlock()
        except UnlockError:
            print "Error: Unable to unlock configuration"
        return False
    
    print op_descr + " : Unlocking the configuration"
    try:
        dev_cfg.unlock()
    # Unlock configuration and process UnlockError exception
    except UnlockError:
        print("Error: Unable to unlock configuration")
        # Return False if config change was not successful
        return False

    # Return True only if everything went as expected
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for key in arguments:
        # Add all arguments to parser
        parser.add_argument('-' + key, required=True, help=arguments[key])
    args = parser.parse_args()

    # Work with Device and Config instances usinf context managers
    with Device() as dev:
        with Config(dev) as conf:

            # Disable the interface. Proceed only if True is returned
            if change_config(conf, "set interfaces " + args.interface + " disable", "Disabling interface"):
                print "Waiting %s seconds..." % args.delay
                
                # Pause the script
                sleep(float(args.delay))

                # Enable the interface and analyze the result
                if change_config(conf, "delete interfaces " + args.interface + " disable", "Enabling interface"):
                    print "Interface bounce script finished successfully!"
                else:
                    print "Error enabling the interface, it will remain disabled."
