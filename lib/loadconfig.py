import configparser
import validators #https://validators.readthedocs.io/en/latest/#module-validators.domain
import sys
import re
import os.path
from difflib import SequenceMatcher


def load():

    global macaddress_family
    global deployment_network_scope_from
    global deployment_network_scope_to
    global deployment_domain
    global hostname_prefix
    global ansible_cfg
    global rndckey
    global tinydbfile
    global ipclass
    global ipnetwork
    global deployment_interface
    global dhcpkey
    global dhcpkey_name
    try:

            defaultsettings = configparser.ConfigParser()
            defaultsettings.read("./conf/default.conf")
            macaddress_family=defaultsettings.get('Networking', 'macaddress_family').lower()
            deployment_network_scope_from=defaultsettings.get('Networking', 'deployment_network_scope_from')
            deployment_network_scope_to=defaultsettings.get('Networking', 'deployment_network_scope_to')
            deployment_domain=defaultsettings.get('Networking', 'deployment_domain').lower()
            deployment_interface=defaultsettings.get('Networking', 'deployment_interface').lower()
            hostname_prefix=defaultsettings.get('Networking', 'hostname_prefix').lower()
            ansible_cfg=defaultsettings.get('Ansible', 'ansible_cfg')
            rndckey=defaultsettings.get('Dns', 'rndckey')
            dhcpkey=defaultsettings.get('Dhcp', 'dhcpkey')
            dhcpkey_name=defaultsettings.get('Dhcp', 'dhcpkey_name')
            tinydbfile=defaultsettings.get('Tinydb', 'tinydbfile')

            if not deployment_domain:

                    print "The deployment_domain is mandatadory"
                    quit()
                    sys.exit(1)
            else:

                    if validators.domain(deployment_domain) != True:
                        print "The domain "+deployment_domain+" specified into default.conf is not rfc compliant"
                        quit()
                        sys.exit(1)

            if not macaddress_family:

                    print "The macaddress_family is mandatadory"
                    quit()
                    sys.exit(1)
            else:

                    temp=macaddress_family+":00:00:00"
                    if  validators.mac_address(temp) != True:
                        print "The macaddress_family "+macaddress_family+" specified into default.conf is wrong, please consider the last 3 hex value only 22:33:44"
                        quit()
                        sys.exit(1)

            if not deployment_network_scope_from:

                    print "The deployment_network_scope_from is mandatadory"
                    quit()
                    sys.exit(1)
            else:


                    if  validators.ip_address.ipv4(deployment_network_scope_from) != True:
                        print "Error: The ip_address "+deployment_network_scope_from+" specified into default.conf is not rfc compliant"
                        quit()
                        sys.exit(1)

            if not deployment_network_scope_to:

                    print "Error: The deployment_network_scope_to is mandatadory"
                    quit()
                    sys.exit(1)
            else:


                    if  validators.ip_address.ipv4(deployment_network_scope_to) != True:
                        print "Error: The ip_address "+deployment_network_scope_to+" specified into default.conf is not rfc compliant"
                        quit()
                        sys.exit(1)



            if hostname_prefix:

                if  not re.match("^[a-zA-Z0-9_-]*$", hostname_prefix):
                    print "Error: The hostname_prefix specified into default.conf is not rfc compliant"
                    quit()
                    sys.exit(1)


            if not ansible_cfg:
                print "Error: The ansible configuration file is mandatadory"
                quit()
                sys.exit(1)
            else:
                if not os.path.exists(ansible_cfg):
                    print "Error: The file "+ansible_cfg+" specified into default.conf it doesn't exits or there are permission problems"
                    quit()
                    sys.exit(1)

            if not rndckey:
                print "Error: The rndckey is mandatadory"
                quit()
                sys.exit(1)

            if not tinydbfile:
                print "Error: The tynidbfile is mandatadory"
                quit()
                sys.exit(1)

            #Check scope and detecting ip class
            s = SequenceMatcher(None, deployment_network_scope_from, deployment_network_scope_to)
            match = s.find_longest_match(0, len(deployment_network_scope_from), 0, len(deployment_network_scope_to))
            ipclass =deployment_network_scope_from[match.a:(match.b+match.size)][:-1]
            if not ipclass:
                print "The scope is overquoted , please consider only class class A,B,C (192.168.80.0-192.168.90.254"
                quit()
                sys.exit(1)
            else:
                octect=ipclass.count('.')
                if octect == 1:
                    ipnetwork =ipclass+".0.0.0\8"
                if octect == 2:
                    ipnetwork =ipclass+".0.0\16"
                if octect == 3:
                    ipnetwork =ipclass+".0\24"
            ###




    except Exception, e:
        print e
        print "Something is wrong into the configuration file, please take a look on ./conf/default.conf"
        sys.exit(1)


def get_macaddress_family():

    return macaddress_family

def get_deployment_network_scope_from():

    return deployment_network_scope_from

def get_deployment_network_scope_to():

    return deployment_network_scope_to

def get_deployment_domain():

    return deployment_domain

def get_deployment_interface():

    return deployment_interface

def get_hostname_prefix():

    return hostname_prefix

def get_ansible_cfg():

    return ansible_cfg

def get_rndckey():

    return rndckey

def get_dhcpkey():

    return dhcpkey
def get_dhcpkey_name():
    return dhcpkey_name
def get_tinydbfile():

    return tinydbfile

def get_ipclass():

    return ipclass

def get_ipnetwork():

    return ipnetwork
