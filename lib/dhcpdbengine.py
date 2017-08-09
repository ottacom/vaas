import pypureomapi
import loadconfig
import sys

dhcp_server_ip="127.0.0.1"
port = 7911



def dhcp_add_host (macaddress,ipaddress,dpl_hostname):

    try:
        dpl_hostname=str(dpl_hostname.strip())
        o = pypureomapi.Omapi(dhcp_server_ip,port, "vaas_key", loadconfig.get_dhcpkey())
        o.add_host_supersede_name(ipaddress,macaddress,dpl_hostname)
        return True
    except:
        print "Something is going wron on dhcp server , please check your config"
        return False


def dhcp_del_host (macaddress,ipaddress,dpl_hostname):

    try:
        dpl_hostname=str(dpl_hostname.strip())
        o = pypureomapi.Omapi(dhcp_server_ip,port, loadconfig.get_dhcpkey_name(), loadconfig.get_dhcpkey())
        o.del_host(macaddress)
        return True
    except:
        print "Something is going wron on dhcp server , please check your config"
        return False
