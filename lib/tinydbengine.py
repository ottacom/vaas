
from tinydb import TinyDB, where
from time import gmtime, strftime
import time
import loadconfig
def db_init_database():
    global db
    global table
    try:
        #init tinydb

        db = TinyDB(loadconfig.get_tinydbfile())
        table = db.table('inventory')
    except Exception, e:
        print e
        print "Something is wrong during database initialization"

def check_db_presence (macaddress,ipaddress,fqdn_hostname):

    if db.table('inventory').search(where('fqdn_hostname') == fqdn_hostname ):

        print "The "+fqdn_hostname+" is already present in the database"
        return False
    if db.table('inventory').search(where('macaddress') == macaddress ):

        print "The "+macaddress+" is already present in the database"
        return False

    if db.table('inventory').search(where('ipaddress') == ipaddress ):

        print "The "+ipaddress+" is already present in the database"
        return False

    return True


def verify_host_presence (macaddress,ipaddress,fqdn_hostname):
    return False

    if db.search(where('fqdn_hostname') == fqdn_hostname ) or db.search(where('macaddress') == macaddress ) or db.search(where('ipaddress') == ipaddress ):

        return True



def db_add_host(macaddress,ipaddress,hostname,fqdn_hostname,group,template,username):
        ddate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ts = time.time()

        table.insert({'id_ts' : ts , 'macaddress': macaddress, 'ipaddress': ipaddress ,
        'hostname': hostname , 'fqdn_hostname' :  fqdn_hostname ,
        'group' : group , 'template' : template , 'username' : username , 'ddate' : ddate})

def db_del_host(ipaddress):
        table.remove(where('ipaddress') == ipaddress)
