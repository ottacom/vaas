
from tinydb import TinyDB, where
from time import gmtime, strftime
import time
import loadconfig
import hashlib
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

        print "The hostname "+fqdn_hostname+" is already present in the database"
        return True
    if db.table('inventory').search(where('macaddress') == macaddress ):

        print "The macaddress "+macaddress+" is already present in the database"
        return True

    if db.table('inventory').search(where('ipaddress') == ipaddress ):

        print "The ipaddress"+ipaddress+" is already present in the database"
        return True

    return False




def verify_group_presence (group):
    if db.table('inventory').search(where('group')== group):
        return True
    else :
        return False

def db_add_host(macaddress,ipaddress,hostname,fqdn_hostname,group,template,ansiblevariables,username):
        ddate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ts = hashlib.md5(str(time.time()).replace(".","")).hexdigest()
        table.insert({'id' : ts , 'macaddress': macaddress, 'ipaddress': ipaddress ,
        'hostname': hostname , 'fqdn_hostname' :  fqdn_hostname ,
        'group' : group , 'template' : template , 'ansiblevariables' :ansiblevariables , 'username' : username , 'ddate' : ddate})

def db_del_host(ipaddress):
        table.remove(where('ipaddress') == ipaddress)
