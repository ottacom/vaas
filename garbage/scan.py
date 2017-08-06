#!/usr/bin/env python
import sys
import os
import nmap                         # import nmap.py module


try:
    nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(0)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(0)


nma = nmap.PortScannerAsync()
nma.scan(hosts='192.168.80.0/24', arguments='-sP -T5', callback=callback_result)
while nma.still_scanning():
    print("Waiting ...")
    nma.wait(2)   # you can do whatever you want but I choose to wait after the end of the scan
