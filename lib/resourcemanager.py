import os
import sys
import subprocess
from progress.spinner import Spinner
import psutil
from subprocess import check_output, CalledProcessError
import time


def chek_resource ():
    state=""
    spinner = Spinner('Checking for new resource...')

    while state != 'FINISHED':
        #ps  -o pid -C vaas-deploy-vm.py
        #pcounter = subprocess.Popen(['ps', '-ef | grep vaas |wc -l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pcounter = subprocess.Popen(['pgrep', '[v]aas-deploy-vm'], stdout=subprocess.PIPE, shell=False)
        nproc= len(pcounter.communicate()[0].split())
        if nproc == 1 :

            state = "FINISHED"
            os.popen('setterm -cursor on').read()

        else:
            #priority queue handle
            plist = []
            #child = subprocess.Popen(['pgrep', '-f', 'vaas-deploy-vm'], stdout=subprocess.PIPE, shell=False)
            father = subprocess.Popen(['pgrep', '[v]aas-deploy-vm'], stdout=subprocess.PIPE, shell=False)
            response = father.communicate()[0]
            for pid in response.split():
                 plist.append(pid)
                #  print "io "+ str(os.getpid())
                #  print "il piu vecchio "+ str(min(plist))
            if  str(min(plist)) ==  str(os.getpid()):

                 state = "FINISHED"

            time.sleep(2)
            spinner.next()



def free_resource(fname):
    try:
        pts="."+os.popen('who am i', 'r').read().split()[1].replace("/","")
        os.remove(fname+pts)
    except:
        pass

def restore_cursor():
    subprocess.Popen(['setterm', '-cursor on'])
