
from tinydb import TinyDB, where
from time import gmtime, strftime
import time
import loadconfig
import hashlib
import tabulate
import json
#from terminaltables import AsciiTable, DoubleTable, SingleTable
import texttable as tt
def db_init_database():
    global db
    global table_inventory
    try:
        #init tinydb

        db = TinyDB(loadconfig.get_tinydbfile())
        table_inventory = db.table('inventory')
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

def db_add_host(macaddress,ipaddress,fqdn_hostname,group,template,ansiblevariables,username):
        ddate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ts = hashlib.md5(str(time.time()).replace(".","")).hexdigest()
        table_inventory.insert({'id' : ts , 'macaddress': macaddress, 'ipaddress': ipaddress ,
        'fqdn_hostname' :  fqdn_hostname ,'group' : group , 'template' : template , 'ansiblevariables' :ansiblevariables , 'username' : username , 'ddate' : ddate})

def db_del_host(ipaddress):
        table.remove(where('ipaddress') == ipaddress)



def db_show_inventory():
    i=0
    if len(db.table('inventory')) == 0:
        return "The inventory is empty"
    else :
         tab = tt.Texttable()
         x = [[]] # The empty row will have the header





         for row in table_inventory.all():

             i = i+1
             jsonrow=json.dumps(row)
             fjson=json.loads(jsonrow)
             x.append([str(i),str(fjson['fqdn_hostname']),str(fjson['ipaddress']),str(fjson['macaddress']),str(fjson['template']),str(fjson['ansiblevariables']),str(fjson['ddate']),str(fjson['username'])])

         tab.add_rows(x)
         tab.header(['Number','Hostname', 'Ipaddress', 'Macaddress','Template','AnsibleVariables','Created','Username'])
         tab.set_cols_align(['c','c','c','c','c','c','c','c'])
         tab.set_cols_width([9,30,15,17,20,20,10,10])
         print tab.draw()
