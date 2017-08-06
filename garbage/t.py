import ipaddress
n = ipaddress.ip_network('192.168.12.10/24')
netw = int(n.network_address)
mask = int(n.netmask)
print netw
print mask
