#!/usr/bin/python

from jnpr.junos import Device
from lxml import etree
import sys

if __name__ == '__main__':

    # Process arguments
    args = {"match": ""}
    for arg in args:
        if arg in sys.argv:
            index = sys.argv.index(arg)
            args[arg] = sys.argv[index+1]

    # Open Device connection and execute Junos OS RPC
    with Device() as dev:
        if args["match"] == "":
            root = dev.rpc.get_interface_information()
        else:
            root = dev.rpc.get_interface_information(interface_name=args["match"])
    
        # Start building output XML document
        xml = etree.Element('interface-status-info')

        # Parse output for required data
        for intf in root.xpath("interface-information/physical-interface"):

            # Retrieve data for the interface name and operational status
            name = intf.findtext("name")
            oper_status = intf.findtext("oper-status")

            # Append the XML for each interface to a list
            xml_item = etree.Element('status-info')
            interface = etree.SubElement(xml_item, 'interface')
            interface.text = name
            status = etree.SubElement(xml_item, 'status')
            status.text = oper_status
            xml.append(xml_item)

        # Print the XML RPC output
        print(etree.tostring(xml, pretty_print=True))
