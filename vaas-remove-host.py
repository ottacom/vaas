#!/usr/bin/python
import argparse
import validators
import re
from lib import loadconfig
from lib import smartvalidation
from lib import dnsdbengine
from lib import tinydbengine
from lib import selfgeneration
from lib import progressbar
from lib import dhcpdbengine

import validators #https://validators.readthedocs.io/en/latest/#module-validators.domain
import dns.query #http://www.dnspython.org/
import dns.tsigkeyring
import dns.update
import dns.resolver
import sys
import os
import getpass
from time import gmtime, strftime



def progressbar(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s -->%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben



def overall_parameters_validation(codeid,ipaddress):
    progressbar(10,100,'Check codeid......      ')

    if smartvalidation.check_codeid(codeid) == False:
        return False


    progressbar(20,100,'Check RFC ipaddress compliance..      ')
    if  smartvalidation.check_ipaddress(ipaddress) == False:
            return False
    else:
        if smartvalidation.check_dns_ipaddress_presence(ipaddress,"s") == True:
            return False
        else:
            progressbar(45,100,'Check scope...                         ')
            if smartvalidation.check_ipaddress_scope(ipaddress,loadconfig.get_deployment_network_scope_from(),loadconfig.get_deployment_network_scope_to()) == False:
                return False


    progressbar(60,100,'Check database inventory..      ')
    idfound=tinydbengine.get_hostdata_by_field('ipaddress',ipaddress,'codeid')
    if not idfound:
        print
        print "The codeid "+codeid+" it doesn't exist in the inventory"
        return False


    progressbar(80,100,'Check database inventory..      ')
    ipfound=tinydbengine.get_hostdata_by_field('codeid',codeid,'ipaddress')

    if not ipfound:
        print
        print "The ipaddress "+ipaddress+" it doesn't exist in the inventory"
        return False
    if idfound == codeid and ipaddress == ipfound:
        #Hurra' everything's fine here !! Go ahead
        progressbar(100,100,'Host founded in the inventory with CodeId '+idfound)
        return True
    else:
        print
        print "The ipaddress "+ipaddress+" it doesn't match with the code "+idfound+" , this code is assigned to "+ipfound
        return False


def delete_host():
    #Rollback


    progressbar(10,100, "Retrieving data from the database...           ")
    progressbar(30,100, "Deleting host from the database...           ")
    dpl_hostname=str(tinydbengine.get_hostdata_by_field('ipaddress',ipaddress,'fqdn_hostname').split(".")[0])
    macaddress=tinydbengine.get_hostdata_by_field('ipaddress',ipaddress,'macaddress')
    fqdn_hostname=dpl_hostname+str(loadconfig.get_deployment_domain())
    tinydbengine.db_del_host(ipaddress)
    progressbar(50,100, "Deleting host from the DNS...                ")
    dnsdbengine.dns_del_record(loadconfig.get_deployment_domain(), 'A', dpl_hostname)
    dnsdbengine.dns_del_record(loadconfig.get_deployment_domain(), 'PTR', ipaddress)
    dnsdbengine.dns_del_record(loadconfig.get_deployment_domain(), 'TXT', dpl_hostname+".info")
    progressbar(60,100, "Deleting host lease from the DHCP...         ")

    dhcpdbengine.dhcp_del_host(macaddress)
    progressbar(70,100, "Checking if db is clean...         ")
    if tinydbengine.check_db_presence(macaddress,ipaddress,fqdn_hostname) == False:
        progressbar(80,100, "Checking if DNS is clean...         ")
        if smartvalidation.check_dns_hostname_presence(dpl_hostname,"") == False:
            progressbar(100,100, "The host "+fqdn_hostname+" with ip "+ipaddress+" has been deleted, everything is clear here!")
        else:
            progressbar(100,100, "The host "+fqdn_hostname+" with ip "+ipaddress+" has been deleted  , but Something wrong please check the DNS and the inventory")
    print
#MAIN
if __name__ == "__main__":





    #VMware asing mac address from 00:50:56:00:00:00 to 00:50:56:3F:FF:FF


    #Load defaultsettings initialization
    loadconfig.load()
    tinydbengine.db_init_database()

    parser = argparse.ArgumentParser()


    parser.add_argument('-c', '--codeid',
                          required=True,
                          help="""The Codeid of the node that needs to be removed from inventory, please do vaas-show-hostid to show all the ids""")

    parser.add_argument('-i', '--ipaddress',
                         required=True,
                         help="""Ip address of the host that needs to be removed from inventory""")



    #load and normalize command parameters
    args = parser.parse_args()
    #Prefix needs to be the frist control in order to generate the hostname
    codeid=args.codeid
    ipaddress=args.ipaddress
    print "Removing host from the inventory...."
    print
    progressbar(0,100, "Retrieving data from the database...           ")
    if overall_parameters_validation(codeid,ipaddress) == True:

        delete_host()




    print
