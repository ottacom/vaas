from tinydb import TinyDB, where
import tinydbengine
import simplejson as json
import loadconfig
import netaddr
import smartvalidation
from difflib import SequenceMatcher
import sys
import re
from decimal import *
from itertools import count, izip



def selfgenerate_macaddress():
    try:
        global next_macaddress
        #generating  macaddress

        db = TinyDB(loadconfig.get_tinydbfile())
        tot=len(db.table('inventory').all())
        next_macaddress = ""
        #print tot
        if tot == 0:
            next_macaddress = loadconfig.get_macaddress_family()+":00:00:00"

        else:

            #REGEX query
            inventory=db.table('inventory').search(where('macaddress').matches('^'+loadconfig.get_macaddress_family()))

            #maclist =[]
            intlist =[]


            dec_mac = ""
            dec_int = ""

            #empty db

            if len(db.table('inventory')) == 0  or len(db.table('inventory').search(where('macaddress') == loadconfig.get_macaddress_family()+":00:00:00")) == 0:
                #fin if the less mac address has been deploeyd
                next_macaddress=loadconfig.get_macaddress_family()+":00:00:00"
            else:
                #encoding mac address
                for row in inventory:


                        lst_macaddress = row["macaddress"].split(":")
                        for hexv in lst_macaddress:
                            octect =str(int("0x"+hexv,0))
                            if len(octect) == 1:
                                    octect="0"+octect
                            dec_mac = dec_mac+octect+"."
                            dec_int = int(dec_mac.replace(".",""))
                        intlist.append(dec_int)
                        #empty the string
                        dec_mac=""
                intlist=sorted(intlist)

                next_macaddress=""
                i=0
                #looping to check if the ip address generate is good enough
                while True:
                    i=+1
                    #looking for some hall
                    if len(db.table('inventory')) == 1:
                            miss_macaddress= str(int(intlist[0]+i))
                    else:

                        nums = (b for intlist, b in izip(intlist, count(intlist[0])) if intlist != b)
                        miss_macaddress=next(nums, None)

                    #there's is not hall
                    if not miss_macaddress :
                        miss_macaddress= str(int(intlist[-1]+i))

                    dot_next_macaddress = re.findall('..',str(miss_macaddress))
                    for dec_value in dot_next_macaddress:
                        octect =str(hex(int(dec_value))).replace("0x","")
                        if len(octect) == 1:
                                octect="0"+octect
                        next_macaddress=next_macaddress+":"+octect
                    if len(next_macaddress) <= 15:
                         next_macaddress="00"+next_macaddress
                    if smartvalidation.check_macaddress_network_presence(next_macaddress,loadconfig.get_deployment_interface(),'s') == False:
                        break

    except Exception, e:
        print e
        print "Something is going wrong during the macaddress self generation process, please check the consistency"
        sys.exit(1)




def selfgenerate_ipaddress():

    try:
        global next_ipaddress


        #Get the ipclass
        s = SequenceMatcher(None, loadconfig.deployment_network_scope_from, loadconfig.deployment_network_scope_to)
        match = s.find_longest_match(0, len(loadconfig.deployment_network_scope_from), 0, len(loadconfig.deployment_network_scope_to))

        ipclass =loadconfig.deployment_network_scope_from[match.a:(match.b+match.size)]

        db = TinyDB(loadconfig.get_tinydbfile())
        tot=len(db.table('inventory').all())
        #print tot

        if tot == 0:
            next_ipaddress = loadconfig.get_deployment_network_scope_from()

        else:

            #REGEX query
            inventory=db.table('inventory').search(where('ipaddress').matches('^'+ipclass))

            iplist =[]

            for row in inventory:

                    ipaddress= int(netaddr.IPAddress(row["ipaddress"]))
                    iplist.append(ipaddress)





            iplist=sorted(iplist)

            #empty db
            next_ipaddress=""
            i=0
            #looping to check if the ip address generate is good enough
            while True:

                i+=1
                #start, end = min(iplist), max(iplist)
                #miss_ipaddress = sorted(set(range(start, end + 1)).difference(iplist))
                nums = (b for iplist, b in izip(iplist, count(iplist[0])) if iplist != b)
                next_ipaddress=next(nums, None)

                if not next_ipaddress and not iplist:
                    next_ipaddress = loadconfig.get_deployment_network_scope_from()
                else:
                    if len(db.table('inventory')) == 1:
                        next_ipaddress=str(int(iplist[-1]+i))
                    else:
                        if len(db.table('inventory').search(where('ipaddress')==loadconfig.get_deployment_network_scope_from())) == 0:
                            next_ipaddress = loadconfig.get_deployment_network_scope_from()
                        #no hall use the higest add
                        if not next_ipaddress:
                            next_ipaddress= str(int(iplist[-1]+i))
                        

                    next_ipaddress=str(netaddr.IPAddress(next_ipaddress))
                if smartvalidation.check_ipaddress_network_presence(next_ipaddress,loadconfig.get_deployment_interface(),'s') == False:
                    break
    except Exception, e:
            print e
            print "Something is going wrong during the ipaddress self generation process, the db consistency"
            sys.exit(1)

def selfgenerate_hostname(prefix,ipaddress):
    global next_hostname

    next_hostname = prefix+ipaddress.replace(".", "-")


def get_next_hostname():

    return next_hostname

def get_next_macaddress():

    return next_macaddress

def get_next_ipaddress():

    return next_ipaddress
