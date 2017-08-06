#!/usr/bin/python
import argparse
import validators
import re
from lib import loadconfig
from lib import smartvalidation
from lib import dnsdbengine
from lib import tinydbengine
from lib import selfgeneration

import validators #https://validators.readthedocs.io/en/latest/#module-validators.domain
import dns.query #http://www.dnspython.org/
import dns.tsigkeyring
import dns.update
import dns.resolver
import sys
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
    progressbar(30,100,'Dns validation..      ')

    if smartvalidation.check_dns_configuration("ns."+loadconfig.get_deployment_domain()) == False:
        return False



    progressbar(40,100,'Check RFC macaddress compliance..      ')
    if smartvalidation.check_macaddress(macaddress) == False:
        return False

    progressbar(50,100,'Check RFC ipaddress compliance..      ')
    if  smartvalidation.check_ipaddress(ipaddress) == False:
            return False
    else:
        if smartvalidation.check_dns_ipaddress_presence(ipaddress) == False:
            return False
        else:
            progressbar(55,100,'Check scope...                         ')
            if smartvalidation.check_ipaddress_scope(ipaddress,loadconfig.get_deployment_network_scope_from(),loadconfig.get_deployment_network_scope_to()) == False:
                return False
    progressbar(60,100,'Check RFC fqdn compliance..      ')
    if smartvalidation.check_hostname_syntax(fqdn_hostname) == False:
        return False
    else:
        if smartvalidation.check_dns_hostname_presence(fqdn_hostname) == False:
            return False

    #Check database
    progressbar(70,100,'Check database inventory..      ')
    if tinydbengine.check_db_presence(macaddress,ipaddress,fqdn_hostname) == False:

        return False
    progressbar(80,100,'Check RFC prefix compliance..      ')
    if smartvalidation.check_prefix_syntax(prefix) == False:
        return False
    progressbar(90,100,'Check ipaddress presence on the network..      ')
    if smartvalidation.check_ipaddress_network_presence(ipaddress,loadconfig.get_deployment_interface()) == False:
        return False
    progressbar(100,100,'Check macaddress presence on the network..     ')
    if smartvalidation.check_macaddress_network_presence(macaddress,loadconfig.get_deployment_interface()) == False:
        return False


    progressbar(100,100,'Everything is ok here!! Start deploy of '+fqdn_hostname)
    print
    #Hurra' everything's fine here !! Go ahead
    return True



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
                  help="""Ansible template , see vaas-tpl-list for all templates available""")
    parser.add_argument('-g', '--group',
                  required=True,
                  help="""Ansible group ,if the grup it doesn't exits a new one will be created""")

    parser.add_argument('-p', '--prefix',
                  required=False,
                  help="""Ansible prefix , if note specified it will get the prefix in the default.conf""")
    parser.add_argument('-d', '--deep',
                  required=False,
                  help="""A deep network macaddress scan will be performerd before the deployment, it takes time for large class of network""")


    #load and normalize command parameters
    args = parser.parse_args()
    if args.dpl_hostname:
        dpl_hostname=args.dpl_hostname.lower()
    else:
        dpl_hostname =""
    if args.macaddress:
        macaddress=args.macaddress.lower()
    else:
        macaddress =""
    ipaddress=args.ipaddress
    template=args.template
    if args.group:
        group=args.group.lower()
    else:
        group =""
    if args.prefix:
        prefix=args.prefix.lower()
    else:
        prefix =""
    username=getpass.getuser()

    #normalize  FQDN
    if prefix:
        fqdn_hostname = prefix+dpl_hostname+"."+loadconfig.get_deployment_domain()
    else:
        if loadconfig.get_hostname_prefix:
            fqdn_hostname = loadconfig.get_hostname_prefix()+dpl_hostname+"."+loadconfig.get_deployment_domain()
        else:
            fqdn_hostname = dpl_hostname+"."+loadconfig.get_deployment_domain()

    #####




    if not macaddress:

        selfgeneration.selfgenerate_macaddress()
        progressbar(10,100,'Generating new macaddress..')
        macaddress = selfgeneration.get_next_macaddress()

    if not ipaddress:
        selfgeneration.selfgenerate_ipaddress()
        progressbar(10,100,'Generating new ipaddress..')
        ipaddress = selfgeneration.get_next_ipaddress()


    if overall_parameters_validation(macaddress, ipaddress, dpl_hostname, prefix) == True  :
        progressbar(10,100,'Loading inventory...')

        #Adding host to the db
        progressbar(20,100,'Adding host in the inventory...')


        tinydbengine.db_add_host(macaddress,ipaddress,fqdn_hostname,prefix+dpl_hostname,group,template,username)
        if tinydbengine.verify_host_presence(macaddress,ipaddress,fqdn_hostname) == True:
            print "Someting is going wrong on tinyDB"
            sys.exit(1)


        #Adding host to dns
        progressbar(30,100, "Adding host in the dns...            ")
        ddate = strftime("%Y-%m-%d-%H:%M:%S", gmtime())

        txt_string = macaddress+","+ipaddress+","+group+","+template+","+ddate
        dnsdbengine.dns_add_record(loadconfig.get_deployment_domain(),'A',prefix+dpl_hostname,ipaddress) #adding A record
        dnsdbengine.dns_add_record(loadconfig.get_deployment_domain(),'PTR',ipaddress,prefix+fqdn_hostname) #adding PTR record
        dnsdbengine.dns_add_record(loadconfig.get_deployment_domain(),'TXT',prefix+dpl_hostname+".info",txt_string) #adding TXT record

        if smartvalidation.verify_dns_ipaddress_presence(ipaddress) == False or smartvalidation.verify_dns_hostname_presence(fqdn_hostname) == False:
                progressbar(0,100, "Rollback procedure , nothing has been changed")
                #Rollback
                tinydbengine.db_del_host(ipaddress)
                sys.exit(1)

        progressbar(100,100, "Host "+fqdn_hostname+" has been deployed!")
        print


    else:
        quit()
