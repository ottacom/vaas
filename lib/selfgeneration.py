from tinydb import TinyDB, where
import tinydbengine
import simplejson as json
import loadconfig
import netaddr
from difflib import SequenceMatcher
import sys

def selfgenerate_macaddress():
    #try:
        global next_macaddress
        #generating  macaddress

        db = TinyDB(loadconfig.get_tinydbfile())
        tot=len(db.table('inventory').all())
        #print tot
        if tot == 0:
            next_macaddress = loadconfig.get_macaddress_family()+":00:00:00"

        else:

            #REGEX query
            inventory=db.table('inventory').search(where('macaddress').matches('^'+loadconfig.get_macaddress_family()))

            maclist =[]

            for row in inventory:

                    #print val[x]["macaddress"]
                    #macaddress=inventory[x]["macaddress"]
                    macaddress = row["macaddress"].replace(":", "")
                    macaddress = int(macaddress)
                    maclist.append(macaddress)



            start, end = min(maclist), max(maclist)
            miss_macaddress = sorted(set(range(start, end + 1)).difference(maclist))

            #empty db
            if not miss_macaddress and not maclist:
                next_macaddress=loadconfig.get_macaddress_family()+":00:00:00"

            else:
                #no hall use the higest add
                if not miss_macaddress:
                    next_macaddress= str(int(max(maclist)+1))
                    next_macaddress = str(int(next_macaddress))
                    next_macaddress = ':'.join(s.encode('hex') for s in next_macaddress.decode('hex'))
                else:
                    #find hall
                    miss_macaddress = sorted(set(range(start, end + 1)).difference(maclist))
                    next_macaddress = str(int(miss_macaddress[0]))
                    next_macaddress = ':'.join(s.encode('hex') for s in next_macaddress.decode('hex'))

        if len(next_macaddress) <= 14:
             next_macaddress="00:"+next_macaddress




    #except Exception, e:
    #    print e
    #    print "Something is going wrong during the macaddress self generation process, please check the consistency"
    #    sys.exit(1)




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



            start, end = min(iplist), max(iplist)
            miss_ipaddress = sorted(set(range(start, end + 1)).difference(iplist))

            #empty db
            if not miss_ipaddress and not iplist:
                next_ipaddress = loadconfig.get_deployment_network_scope_from()
            else:
                #no hall use the higest add
                if not miss_ipaddress:
                    next_ipaddress= str(int(max(iplist)+1))
                    next_ipaddress = str(int(next_ipaddress))
                    next_ipaddress=str(netaddr.IPAddress(next_ipaddress))
                else:
                    #find hall
                    
                    next_ipaddress = str(int(miss_ipaddress[0]))
                    next_ipaddress=str(netaddr.IPAddress(next_ipaddress))



    except Exception, e:
        print e
        print "Something is going wrong during the ipaddress sel generation process, please check the consistency"
        sys.exit(1)


def get_next_hostname():

    return next_hostname

def get_next_macaddress():

    return next_macaddress

def get_next_ipaddress():

    return next_ipaddress
