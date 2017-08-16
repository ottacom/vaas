from tinydb import TinyDB, where , Query
import json
import hashlib


def db_init_database():

    global db
    global table_message

    try:
        #init tinydb

        db = TinyDB("./tinydb/servicedb.json")
        table_message = db.table('table_message')
    except Exception, e:
        print e
        print "Something is wrong during database initialization"


def display_message(number,dynvalue):
    try:

        db_init_database()
        query_error = Query()
        fjson=json.loads(json.dumps(db.table('table_message').get(query_error.codeid == number)))
        i=0

        for i in range (0,len(dynvalue)):
            i=i+1
            #clean_dynvalue = ''.join(e for e in dynvalue[i-1] if e.isalnum())
            #error_normalize=(fjson['message']).replace("#"+str(i),str(clean_dynvalue))
            error_normalize=(fjson['message']).replace("#"+str(i),dynvalue[i-1])

        return error_normalize

    except:

        for i in range (0,len(dynvalue)):
            i=i+1
            error_normalize=((fjson['message']).replace("#"+str(i),""))

        return error_normalize
        pass
