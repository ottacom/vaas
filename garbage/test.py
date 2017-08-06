from tinydb import TinyDB
import simplejson as json

db = TinyDB('./tinydb/vaas.json')
load=json.dumps(db.all())
val=json.loads(load)
tot=len(db)
for x in range(0,tot):
	print val[x]["macaddress"]
