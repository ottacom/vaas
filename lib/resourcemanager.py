import os
import glob
from progress.spinner import Spinner


def chek_resource (fname,times=None):
    pts="."+os.popen('who am i', 'r').read().split()[1].replace("/","")
    i = 0
    #Creating a lockfile avoid overlapping
    for name in glob.glob('/tmp/*.pts*'):
        i=i+1

    if i == 0:
        open(fname+pts, 'a').close()
        os.utime(fname+pts, None)

    else:

        spinner = Spinner('Waiting for new resource...')
        state = ""

        while state != 'FINISHED':
            i = 0
            # Do some work
            for name in glob.glob('/tmp/*.pts*'):
                i=i+1
            if i == 0:
                open(fname+pts, 'a').close()
                os.utime(fname+pts, None)
                state = 'FINISHED'
            else:
                spinner.next()


def free_resource(fname):
    try:
        pts="."+os.popen('who am i', 'r').read().split()[1].replace("/","")
        os.remove(fname+pts)
    except:
        pass
