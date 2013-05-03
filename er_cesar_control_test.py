# control script for Ar clean using Cesar136 version 0.1 written by JB@KIT 05/2013

from lib.er_cesar136 import Cesar136_Dev

import time,sys
import atexit
#import struct
import serial
        

if __name__ == "__main__":   #if executed as main (and not imported)
    
    time.sleep(1)
    ar_cl = Cesar136_Dev()   #Ar clean
    print "Setting Echo Mode On",ar_cl.EchoModeOn()
    print "Setting Remote Control On",ar_cl.setRemoteControlOn()
    print "Pulse Mode Off",ar_cl.setPulseMode(0,0,0)
    print "ICP Mode Off",ar_cl.setICPMode(0,0,0,0,0,0)    
    
    # start operation routine
    
    #settings
    print "Mode: ",ar_cl.setOperationMode(0,100,0)   #P_fwd = 100W
    print "Matches: ",ar_cl.setMatches(375,580)      #capacities
    
    time.sleep(5)
    
    print "Status:\n",ar_cl.getStatus()
    time.sleep(5)
    
    #commands
    
    # end operation routine