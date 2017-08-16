import pypureomapi
import sys

keyname = "jpm_key"
secret  = "mfVtuvGj7M4QjTfRWHt5p0EoC4Yd6zruJDDgYyeJ6/Eguhx1ZUT6OAIw1C4B6HG92KwZAmxx0SLWN6PwN5Tsmw=="
server  = "127.0.0.1"
port    = 7911

try:
        oma = pypureomapi.Omapi(server, port, keyname, secret, debug=False)
except pypureomapi.OmapiError, err:
        print "OMAPI error: %s" % (err,)
        sys.exit(1)

oma.add_host("10.0.12.1", "00:50:56:9a:00:2b", "pc009.mens.de")
oma.del_host("00:50:56:9a:00:2b")
