#!/usr/bin/python
from tinydb import TinyDB, where , Query
import argparse
import texttable as tt
import json


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






def db_add_error(message):
        nextrec=len(db.table('table_message'))+1
        table_message.insert({'codeid' : str(nextrec) , 'message': message})
        #waiting for write



def db_del_error(codeid):

        table_message.remove(where('codeid') == str(codeid))


def db_show_errors():

    i=0
    if len(db.table('table_message')) == 0:

        print "Sorry, there's nothing to show here, the db is empty"

    else :
         tab = tt.Texttable()
         x = [[]] # The empty row will have the header

         for row in table_message.all():

              i = i+1
              jsonrow=json.dumps(row)
              fjson=json.loads(jsonrow)
              x.append([str(fjson['codeid']),str(fjson['message'])])

         tab.add_rows(x)
         tab.header(['CodeId','Message'])
         tab.set_cols_align(['c','c'])
         tab.set_cols_width([10,100])
         print tab.draw()



if __name__ == "__main__":
    #load and normalize command parameters

    db_init_database()

    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--message',
                  required=False,
                  help="""Text of the message""")
    parser.add_argument('-d', '--delete',
                  required=False,
                  help="""Id message to be removed""")
    parser.add_argument('-l', '--list',
                  required=False,
                  help="""Show message list""")

    args = parser.parse_args()

    if args.list:
        db_show_errors()
    if args.message:
        db_add_error(args.message)
    if args.delete:
        db_del_error(args.delete)
