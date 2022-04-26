from jnpr.junos import Device
import argparse

# Define the arguments dictionary
arguments = {
    "interface": "Interface to display",
    "family": "Family to display (inet, inet6)"
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for key in arguments:
        # Add all arguments to parser
        parser.add_argument('-' + key, required=True, help=arguments[key])
    args = parser.parse_args()
    print(args)

    # Create a Device instance and open connection
    with Device() as dev:

        # Call the RPC using standard Junos PyEZ functionality
        res = dev.rpc.get_interface_information(interface_name=args.interface, terse=True, normalize=True)
        
        # Print interface name and operational status
        print args.interface + " status: " + res.findtext("logical-interface/oper-status")
        
        # Define XPath string
        XPATH = "//address-family[address-family-name=$family]/interface-address/ifa-local"

        # Apply XPath to the result of RPC call, print all addresses
        for elem in res.xpath(XPATH, family=args.family):
            print args.family + " address " + elem.text
