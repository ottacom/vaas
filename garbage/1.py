#!/usr/bin/python
from __future__ import print_function
import json
overarch = {}
overarch["us"] = [
    "kc.example.com",
    "la.example.net",
]

overarch["germany"] = ["de.test.net"]

overarch["france"] = ["fr.test.net"]

overarch["vps"] = {"children":["us", "germany"], "hosts":[]}

hostvars = {}
hostvars["kc.example.com"] = {"openvpn.port":17601}
hostvars["la.example.net"] = {"ansible_ssh_port":40000}

overarch["_meta"] = {"hostvars":hostvars}

print(json.dumps(overarch, sort_keys=True, indent=2, separators=(',', ': ')))

