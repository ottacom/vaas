from tinydb import TinyDB
import simplejson as json

db = TinyDB('./tinydb/vaas.json')
print db.search(inventory.macaddress.matches('^0'))
