#!/usr/bin/python

from junos import Junos_Configuration
import jcs
from lxml import etree

if __name__ == '__main__':
    
    jcs.syslog("8", "Translation script Junos_Configuration = " + etree.tostring(Junos_Configuration))
    xml_config = "<routing-options><static>"

    for sr in Junos_Configuration.xpath("//*[local-name()='prefix']"):
        name = sr.xpath("./*[local-name()='name']")[0].text
        nh = sr.xpath("./*[local-name()='nh']")[0].text
        operation = sr.xpath("./*[local-name()='name']/@operation")[0]
        jcs.syslog("8", "Translation script, name={}, nh={}, operation={}".format(name, nh, operation))

        xml_config += """<route>
                           <name>{0}</name>
                           <next-hop>{1}</next-hop>
                         </route>  """.format(name, nh)

    xml_config += "</static></routing-options>"

    jcs.emit_change(xml_config, "transient-change", "xml")
