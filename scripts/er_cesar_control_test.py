# control script for Ar clean using Cesar136 version 0.1 written by JB@KIT 05/2013

from er_cesar136 import Cesar136_Dev

import time,sys
import atexit
#import struct
import serial
        

if __name__ == "__main__":   #if executed as main (and not imported)
    
    ar_cl = Cesar136_Dev()   #Ar clean
    print ar_cl.getStatus()
    
    # start operation routine
    
    time.sleep(5)
    print "Hello world!"
    
    # end operation routine