import socket
import validators
from netaddr import * #http://netaddr.readthedocs.io/en/latest/tutorial_01.html
import os, sys
from lib import spinner


def check_hostname_syntax(hostname):

    #syntax rfc control
    if len(hostname) > 255:

        return False

    if hostname:
        #if re.match("^[a-zA-Z0-9]*$", hostname):
        if not set('[~!@#$%^&*()+{}":;\']+$').intersection(hostname):
                return True
        else:

            print"The hostname "+hostname+" specified is not rfc compliant"
            return False

def check_prefix_syntax(prefix):

        if not set('[~!@#$%^&*()+{}":;\']+$').intersection(prefix):
            return True
        else:
            print "The prefix "+prefix+" specified is not rfc compliant"
            return False

def check_group_syntax(group):

    #syntax rfc control
    if len(group) > 255:

        return False

    if group:

        if not set('[~!@#$%^&*()+{}":;\']+$').intersection(group):
                return True
        else:

            print"The group "+group+" specified is not rfc compliant"
            return False

def check_dns_hostname_presence(hostname):
    try:


        ip=socket.gethostbyname(hostname)
        if ip:

            print "This hostname "+hostname+" is already taken from "+ip+" please check your inventory"
            return False
    except  socket.gaierror as e:
            return True
    except :
            print "I can't verify if the hostname is already taken , please check your DNS"
            return False

def verify_dns_hostname_presence(hostname):
    return True
    ip=socket.gethostbyname(hostname)
    if not ip:

        return False

def check_dns_configuration(hostname):
    try:


            ip=socket.gethostbyname(hostname)
            return True
    except socket.gaierror as e:
            print "Something wrong in the DNS configuration , impossible to resolve "+hostname+" please set up yor DNS correctly before start a deploy"
            return False
    except :

            print "I can't verify if the hostname is already taken , please check your DNS"
            return False

def check_macaddress(macaddress):

    if  validators.mac_address(macaddress) != True:
        print "The macaddress "+macaddress+" specified is not rfc compliant"
        return False

    else:
        return True


def check_ipaddress(ipaddress):
    if  validators.ip_address.ipv4(ipaddress) != True:
            print "The ipaddress "+ipaddress+" specified is not rfc compliant"
            return False
    else:
        return True

def check_dns_ipaddress_presence(ipaddress):
    try:
        hostname=socket.gethostbyaddr(ipaddress)
        hostmane_res=hostname[0]
        if hostname:
            print "The ip address "+ipaddress+" is already taken from "+hostmane_res+" please check your inventory"
            return False

    except  socket.herror as e:
            if e.args[0] == 1:
                return True

    except :
            print "I can't verify if the ip address "+ipaddress+" is already taken , please check your DNS"
            return False


def verify_dns_ipaddress_presence(ipaddress):
    return True

    hostname=socket.gethostbyaddr(ipaddress)
    hostmane_res=hostname[0]
    if not hostname:

        return False





def check_ipaddress_scope(ipaddress,scope_start,scope_end):


    if not ((IPAddress(ipaddress) >= IPAddress(scope_start)) and  (IPAddress(ipaddress) <= IPAddress(scope_end))):
            print "The ip "+ipaddress+" is out of the scope"
            return False

def check_ipaddress_network_presence(ipaddress,interface):

    # ping is optional (sends a WHO_HAS request)

    os.popen('ping -c 2 %s -I %s -W 1'  % (ipaddress,interface))

    # grep with a space at the end of IP address to make sure you get a single line
    fields = os.popen('grep "%s " /proc/net/arp' % ipaddress).read().split()
    if len(fields) == 6 and fields[3] != "00:00:00:00:00:00":
        if fields[3]==macaddress:
            print "The ip address "+ipaddress+" with macaddress "+fields[3]+" is already present the deployment the network"
            return False
    else:
            return True


def check_macaddress_network_presence(macaddress,interface):



    localmac = open('/sys/class/net/'+interface+'/address').readline().strip()
    if localmac==macaddress:
        print "The macaddress "+macaddress+" is already present on this server"
        return False

    os.popen('arping -c 2 %s -i %s -W 1' % (macaddress,interface))
    # grep with a space at the end of IP address to make sure you get a single line
    fields = os.popen('grep "%s " /proc/net/arp' % macaddress).read().split()
    if len(fields) == 6 and fields[3] != "00:00:00:00:00:00":
        if fields[3]==macaddress:
            print "The macaddress "+macaddress+" with ipaddress "+fields[1]+" is already present the deployment the network"
            return False
    else:
            return True
