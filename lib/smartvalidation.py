import socket
import validators
from netaddr import * #http://netaddr.readthedocs.io/en/latest/tutorial_01.html
import os, sys
from lib import spinner
import subprocess
import messagemanager




def check_hostname_syntax(hostname):

    #syntax rfc control
    if len(hostname) > 255:

        return False

    if hostname:
        #if re.match("^[a-zA-Z0-9]*$", hostname):
        if not set('[~!@#$%^&*()+{}":;\']+$').intersection(hostname):
                return True
        else:
            print messagemanager.display_message('1', [hostname])
            return False

def check_prefix_syntax(prefix):

        if not set('[~!@#$%^&*()+{}":;\']+$').intersection(prefix):
            return True
        else:
            print messagemanager.display_message('2', [prefix])
            return False

def check_codeid(codeid):

    if not set('[~!@#$%^&*()+{}":;\']+$').intersection(codeid) and len(codeid) == 32:
            return True
    else:

        print messagemanager.display_message('3', [codeid])
        return False



def check_group_syntax(group):

    #syntax rfc control
    if len(group) > 255:

        return False

    if group:

        if not set('[~!@#$%^&*()+{}":;\']+$').intersection(group):
                return True
        else:

            print messagemanager.display_message('4', [group])

            return False

def check_dns_hostname_presence(hostname,silence):
    try:
        ip=socket.gethostbyname(hostname)
        if ip:
            if (silence ==""):
                print messagemanager.display_message('5', [hostname,ip])
            return True
    except  socket.gaierror as e:
            return False
    except :
            messagemanager.display_message('6', [])
            return False

def check_dns_ipaddress_presence(ipaddress,silence):
    try:
        hostname=socket.gethostbyaddr(ipaddress)
        hostmane_res=hostname[0]
        if hostname:
            if (silence ==""):
                print "The ip address "+ipaddress+" is already taken from "+hostmane_res+" please  inventory"
            return True

    except  socket.herror as e:
            if e.args[0] == 1:
                return False

    except :
            print "I can't verify if the ip address "+ipaddress+" is already taken , please check your DNS"
            return True


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






def check_ipaddress_scope(ipaddress,scope_start,scope_end):
    if not ((IPAddress(ipaddress) >= IPAddress(scope_start)) and  (IPAddress(ipaddress) <= IPAddress(scope_end))):
            print "The ip "+ipaddress+" is out of the scope"
            return False


def check_ipaddress_network_presence(ipaddress,interface,silence):
    #try:
            # ping is optional (sends a WHO_HAS request)

        # command = 'ping -c 2 '+ipaddress+' -I '+interface+' -W 1 > /dev/null'
        command = 'fping '+ipaddress+' -I '+interface+' > /dev/null'
        sub=subprocess.call(command, shell=True)

        if sub == 1:
            return False
        if sub == 0 :
            fields = os.popen('arp -a '+ipaddress).read().split()
            if (silence ==""):
                print "The ip address "+ipaddress+" is already present into the deployment network with macaddress "+fields[3]

            return True
        else:
            print"Something is going wrong on network side validation during syscall arping"
            return True
    #except Exception, e:
        print e
        print "Something is going wrong on network side validation , please check if network deployment network interface is correct in ./conf/default.conf"
        return True


def check_macaddress_network_presence(macaddress,interface,silence):

    try:

        localmac = open('/sys/class/net/'+interface+'/address').readline().strip()
        if localmac==macaddress:
            print "The macaddress "+macaddress+" is already present on this server"
            return True
        command = 'arping -c 2 '+macaddress+' -i '+interface+' -W 1 > /dev/null'
        sub=subprocess.call(command, shell=True)
        if sub == 1:
            return False
        if sub == 0 :
            fields = ('arping -c 1 '+macaddress+' -i '+interface+' -W 1 > /dev/null').read().split()
            if (silence ==""):
                print "The macaddress "+macaddress+" is already present the deployment the network on ip"+fields[1]
            return True
        else:
            print"Something is going wrong on network side validation during syscall arping"
            return True

    except Exception, e:
        print e
        print "Something is going wrong on network side validation , please check if network deployment network interface is correct in ./conf/default.conf"
        return False
