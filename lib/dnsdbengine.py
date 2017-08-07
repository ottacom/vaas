import dns.query #http://www.dnspython.org/
import dns.tsigkeyring
import dns.update
import dns.resolver
import loadconfig
import smartvalidation
import sys #https://stackoverflow.com/questions/13842116/how-do-we-get-txt-cname-and-soa-records-from-dnspython

import ipaddress
import subprocess
import socket
origGetAddrInfo = socket.getaddrinfo





def dns_txt_query(txtrecord):

    try:

        answer=dns.resolver.query(txtrecord, "TXT")
        for rdata in answer:
           for txt_string in rdata.strings:

               return txt_string

    except:
        return ""


def reverse(ip):
        #reversing ip
        if len(ip) <= 1:
                return ip
        l = ip.split('.')
        return '.'.join(l[::-1])



def dns_add_record(deployment_domain,rtype,invalue,outvalue):


        command =""
        defaulttl = "300"

        #command += "update delete %s A\n" % domain
        #command += "update add %s "+rtype+"\n" % domain
        if rtype == "A" or rtype == "TXT":
            #update add $DOMAIN 30 A $IPV4
            command += "zone "+deployment_domain+"\n"
            command += "update add "+invalue+"."+deployment_domain+" "+defaulttl+" "+rtype+" "+outvalue+"\n"

        if rtype == "PTR":
            ptr_invalue = reverse(invalue)
            command += "update add "+ptr_invalue+".in-addr.arpa "+defaulttl+" "+rtype+" "+outvalue+"\n"

        #command +=  "show\nsend\n"
        command = "sudo nsupdate -k {0} << EOF\n{1}\nEOF\n".format(loadconfig.get_rndckey(), command)
        #print("Calling the following command now:\n\n" + command)
        sub=subprocess.call(command, shell=True)
        if sub <> 0 :
            return False
        else:
            return True


def dns_del_record(deployment_domain,rtype,invalue):


        command =""
        defaulttl = "300"

        #command += "update delete %s A\n" % domain
        #command += "update add %s "+rtype+"\n" % domain
        if rtype == "A" or rtype == "TXT":
            #update add $DOMAIN 30 A $IPV4
            command += "zone "+deployment_domain+"\n"
            command += "update delete "+invalue+"."+deployment_domain+" "+rtype+"\n"

        if rtype == "PTR":
            ptr_invalue = reverse(invalue)

            command += "update delete "+ptr_invalue+".in-addr.arpa. "+rtype+"\n"

        #command +=  "show\nsend\n"
        command = "sudo nsupdate -k {0} << EOF\n{1}\nEOF\n".format(loadconfig.get_rndckey(), command)

        #print("Calling the following command now:\n\n" + command)
        sub=subprocess.call(command, shell=True)
