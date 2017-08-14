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



def overall_parameters_validation(macaddress,ipaddress,dpl_hostname,prefix):
    progressbar(35,100,'Dns validation..      ')

    if smartvalidation.check_dns_configuration("ns."+loadconfig.get_deployment_domain()) == False:
        return False



    progressbar(40,100,'Check RFC macaddress compliance..      ')
    if smartvalidation.check_macaddress(macaddress) == False:
        return False

    progressbar(42,100,'Check RFC ipaddress compliance..      ')
    if  smartvalidation.check_ipaddress(ipaddress) == False:
            return False
    else:
        if smartvalidation.check_dns_ipaddress_presence(ipaddress,"") == True:
            return False
        else:
            progressbar(45,100,'Check scope...                         ')
            if smartvalidation.check_ipaddress_scope(ipaddress,loadconfig.get_deployment_network_scope_from(),loadconfig.get_deployment_network_scope_to()) == False:
                return False
    progressbar(50,100,'Check RFC fqdn compliance..      ')
    if smartvalidation.check_hostname_syntax(fqdn_hostname) == False:
        return False
    else:
        if smartvalidation.check_dns_hostname_presence(fqdn_hostname,"") == True:
            return False

    progressbar(52,100,'Check RFC group compliance..      ')

    if smartvalidation.check_group_syntax(group) == False:
        return False

    #Check database
    progressbar(60,100,'Check database inventory..      ')
    if tinydbengine.check_db_presence(macaddress,ipaddress,fqdn_hostname) == True:
        return False
    progressbar(62,100,'Check RFC prefix compliance..      ')
    if smartvalidation.check_prefix_syntax(prefix) == False:
        return False

    progressbar(70,100,'Check if the macaddress is already present on the network..     ')
    if smartvalidation.check_macaddress_network_presence(macaddress,loadconfig.get_deployment_interface(),"") == True:
        return False

    progressbar(95,100,'Check if the ipaddress is already present on the network..      ')
    if smartvalidation.check_ipaddress_network_presence(ipaddress,loadconfig.get_deployment_interface(),"") == True:
        return False


    progressbar(100,100,'Everything is ok here!! Go to deploy '+fqdn_hostname)
    print
    #Hurra' everything's fine here !! Go ahead
    return True


def total_rollback():
    #Rollback
    print "Rollback procedure activated"
    progressbar(100,100, "Deleting host from the database...           ")
    tinydbengine.db_del_host(ipaddress)
    progressbar(70,100, "Deleting host from the DNS...                ")
    dnsdbengine.dns_del_record(loadconfig.get_deployment_domain(), 'A', dpl_hostname)
    dnsdbengine.dns_del_record(loadconfig.get_deployment_domain(), 'PTR', ipaddress)
    dnsdbengine.dns_del_record(loadconfig.get_deployment_domain(), 'TXT', dpl_hostname+".info")
    progressbar(50,100, "Deleting host lease from the DHCP...         ")
    dhcpdbengine.dhcp_del_host(macaddress)
    progressbar(40,100, "Checking if db is clean...         ")
    if tinydbengine.check_db_presence(macaddress,ipaddress,fqdn_hostname) == False:
        progressbar(20,100, "Checking if DNS is clean...         ")
        if smartvalidation.check_dns_hostname_presence(dpl_hostname,"") == False:
            progressbar(0,100, "Rollback completed... Everything is clear here!")
        else:
            progressbar(0,100, "Rollback completed , but Something wrong please check the DNS and the inventory")
    print
#MAIN
if __name__ == "__main__":





    #VMware asing mac address from 00:50:56:00:00:00 to 00:50:56:3F:FF:FF


    #Load defaultsettings initialization
    loadconfig.load()
    tinydbengine.db_init_database()

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--dpl_hostname',
                  required=False,
                  help="""Virtual machine hostname only if not sepcified vill be generate""")
    parser.add_argument('-m', '--macaddress',
                  required=False,
                  help="""Mac address deployment interface (00:1a:22:3b:44:5c:66), if not sepcified vill be generate randomly""")
    parser.add_argument('-i', '--ipaddress',
                  required=False,
                  help="""Virtual machine deployment ip address, if not specified will be assigned the first one available""")
    parser.add_argument('-t', '--template',
                  required=True,
                  help="""Image template , see vaas-tpl-list for all templates available""")
    parser.add_argument('-g', '--group',
                  required=True,
                  help="""Ansible group ,if the grup it doesn't exits a new one will be created""")
    parser.add_argument('-p', '--prefix',
                  required=False,
                  help="""Ansible prefix , if note specified it will get the prefix in the default.conf""")
    parser.add_argument('-v', '--ansiblevariables',
                  required=False,
                  help="""Ansible variables for the host""")
    



    #load and normalize command parameters
    args = parser.parse_args()
    #Prefix needs to be the frist control in order to generate the hostname
    if args.prefix:
        prefix=args.prefix.lower()
    else:
        prefix = loadconfig.get_hostname_prefix().lower()
    if args.dpl_hostname:
        dpl_hostname=prefix+args.dpl_hostname.lower()
        dpl_hostname=str(dpl_hostname.strip())
    else:
        dpl_hostname =""
    if args.macaddress:
        macaddress=args.macaddress.lower()
    else:
        macaddress =""
    ipaddress=args.ipaddress
    template=args.template
    group=args.group
    ansiblevariables = args.ansiblevariables
    username=getpass.getuser()


    print
    print "Vaas phase 1/2 : Starting deep consistency control go-nogo procedure"

    if tinydbengine.verify_group_presence(group) == False:
        print "Info: A new group "+group+" will be create"



    if not macaddress:
        progressbar(10,100,'Generating new macaddress..')
        selfgeneration.selfgenerate_macaddress()
        macaddress = selfgeneration.get_next_macaddress()

    if not ipaddress:
        progressbar(20,100,'Generating new ipaddress..')
        selfgeneration.selfgenerate_ipaddress()
        ipaddress = selfgeneration.get_next_ipaddress()

    if not dpl_hostname:
        progressbar(30,100,'Generating new hostname..')
        selfgeneration.selfgenerate_hostname(prefix,ipaddress)
        dpl_hostname = selfgeneration.get_next_hostname()

    #normalize  FQDN needs to be here after dpl_hostname valorization
    fqdn_hostname = dpl_hostname+"."+loadconfig.get_deployment_domain()



    #####
    #os.system('clear')

    if overall_parameters_validation(macaddress, ipaddress, dpl_hostname, prefix) == False  :
        progressbar(0,100,'No-go problems detected...')
        print
        quit()
        sys.exit(1)



    print "Vaas phase 2/2 : Deploying the host"
    progressbar(1,100,'Working on the  inventory...')


    if tinydbengine.check_db_presence(macaddress,ipaddress,fqdn_hostname) == True:
        print "Someting is going wrong on tinyDB , consider a database consolidation e before"
        sys.exit(1)

    #Adding host to the db
    progressbar(20,100,'Adding host in the inventory...')
    tinydbengine.db_add_host(macaddress,ipaddress,fqdn_hostname,group,template,ansiblevariables,username)
    #Adding host to dns
    progressbar(30,100, "Adding host in the dns...            ")
    ddate = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
    txt_string = macaddress+","+ipaddress+","+group+","+template+","+ddate

    if dnsdbengine.dns_add_record(loadconfig.get_deployment_domain(),'A',dpl_hostname,ipaddress) == False \
        or dnsdbengine.dns_add_record(loadconfig.get_deployment_domain(),'PTR',ipaddress,fqdn_hostname) == False \
        or dnsdbengine.dns_add_record(loadconfig.get_deployment_domain(),'TXT',dpl_hostname+'.info',txt_string)==False :
        progressbar(0,100, "No-go, Rollback procedure activated, nothing has been changed")
        print "Someting is going wrong during DNS update"
        #Rollback
        total_rollback()
        quit()
        sys.exit(1)

    progressbar(40,100, "Adding host lease in the dhcp...")
    if dhcpdbengine.dhcp_add_host(macaddress,ipaddress,dpl_hostname)== False:
        total_rollback()
        quit()
        sys.exit(1)

    if smartvalidation.check_dns_ipaddress_presence(ipaddress,"s") == False or smartvalidation.check_dns_hostname_presence(fqdn_hostname,"s") == False:
            progressbar(0,100, "Rollback procedure activated, nothing has been changed")
            total_rollback()
            quit()
            sys.exit(1)

    progressbar(100,100, "Host "+fqdn_hostname+" with ipaddress "+ipaddress+" has been deployed!")
    print
    print
