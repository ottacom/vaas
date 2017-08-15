
from tinydb import TinyDB, where , Query
from time import gmtime, strftime
import time
import loadconfig
import hashlib
#import tabulate
import json
from progress.spinner import Spinner
#from terminaltables import AsciiTable, DoubleTable, SingleTable
import texttable as tt
def db_init_database():
    global db
    global table_inventory
    try:
        #init tinydb

        db = TinyDB(loadconfig.get_tinydbfile())
        #db = TinyDB(loadconfig.get_tinydbfile(), storage=ConcurrencyMiddleware(CachingMiddleware(JSONStorage)))
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

def find_hostid_by_ipaddress (ip):

    #el=db.get.table('inventory').search(where('ipaddress') == ipaddress)
    #print db.table('inventory').all()[0].keys()[1] # get only one key
    #print db.table('inventory').all()[0].keys() # get alle keys
    try:
        inventory = Query()
        el = db.table('inventory').get(inventory.ipaddress == ip)
        if el.eid:
            return el.eid
    except Exception, e:
        #print e
        print "The Host is not present in the inventory"



def get_hostdata_by_field (key,value,outvalue):
    try:
        data =""
        data1 = ""
        inventory = Query()
        #print db.get.table('inventory').search(where(key) == value)
        if (key == 'ipaddress'):
            data = db.table('inventory').get(inventory.ipaddress == value)
        if (key == 'macaddress'):
            data = db.table('inventory').get(inventory.macaddress == value)
        if (key == 'fqdn_hostname'):
            data = db.table('inventory').get(inventory.fqdn_hostname == value)
        if (key == 'codeid'):
            data = db.table('inventory').get(inventory.codeid == value)

        jsonrow=json.dumps(data)
        data1  = json.loads(jsonrow)

        if (outvalue == 'ipaddress'):
            return data1['ipaddress']
        if (outvalue == 'macaddress'):
            return data1['macaddress']
        if (outvalue == 'fqdn_hostname'):
            return data1['fqdn_hostname']
        if (outvalue == 'codeid'):
            return data1['codeid']

    except Exception, e:
        #print e
        return ""


def verify_group_presence (group):
    if db.table('inventory').search(where('group')== group):
        return True
    else :
        return False

def db_add_host(macaddress,ipaddress,fqdn_hostname,group,template,ansiblevariables,username):
        nextrec=len(db.table('inventory'))+1
        ddate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ts = hashlib.md5(str(time.time()).replace(".","")).hexdigest()
        table_inventory.insert({'codeid' : ts , 'macaddress': macaddress, 'ipaddress': ipaddress ,
        'fqdn_hostname' :  fqdn_hostname ,'group' : group , 'template' : template , 'ansiblevariables' :ansiblevariables , 'username' : username , 'ddate' : ddate})
        #waiting for write
        spinner = Spinner('Check invnentory consistency')
        state = ""
        while state != 'END' :
            if len(db.table('inventory')) == nextrec:
                state='END'
            else:
                spinner.next()



def db_del_host(ipaddress):
        table_inventory.remove(where('ipaddress') == ipaddress)


def db_show_inventory():
    i=0
    if len(db.table('inventory')) == 0:

        print "Sorry, there's nothing to show here, the db is empty"

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


def db_show_hostlist():
    i=0
    if len(db.table('inventory')) == 0:

        print "Sorry, there's nothing to show here, the db is empty"

    else :
         tab = tt.Texttable()
         x = [[]] # The empty row will have the header





         for row in table_inventory.all():

             i = i+1
             jsonrow=json.dumps(row)
             fjson=json.loads(jsonrow)
             x.append([str(i),str(fjson['codeid']),str(fjson['fqdn_hostname']),str(fjson['ipaddress']),str(fjson['macaddress']),str(fjson['ddate']),str(fjson['username'])])

         tab.add_rows(x)
         tab.header(['Number','CodeId','Hostname', 'Ipaddress', 'Macaddress','Created','Username'])
         tab.set_cols_align(['c','c','c','c','c','c','c'])
         tab.set_cols_width([9,32,30,15,17,10,10])
         print tab.draw()
