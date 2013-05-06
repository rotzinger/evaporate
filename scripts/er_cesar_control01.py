# control script for Ar clean using Cesar136 version 0.2 written by JB@KIT 05/2013

import os,sys
sys.path.append('../lib')
from er_cesar136 import Cesar136_Dev

import time,sys
import atexit
#import struct
import serial
#import os
        

if __name__ == "__main__":   #if executed as main (and not imported)
    
    time.sleep(1)
    
    path = "../logs/log" + str(time.localtime()[2]) + str(time.localtime()[1]) + str(time.localtime()[0]) + str(time.localtime()[3]) + str(time.localtime()[4]) + ".txt"
    log_file = open(path,'w')   #create log file
    log_file.close()
    print "Log-File in /logs"
    
    ar_cl = Cesar136_Dev()   #Ar clean
    ar_cl.setEchoModeOff()
    print "Setting Echo Mode Off"
    ar_cl.setRemoteControlOn()
    print "Setting Remote Control On"
    ar_cl.setPulseMode(0,0,0)
    print "Pulse Mode Off"
    ar_cl.setICPMode(0,0,0,0,0,0) 
    print "ICP Mode Off"
    
    # start operation routine
    
    #settings
    print "Mode: ",ar_cl.setOperationMode(0,100,0)   #P_fwd = 100W
    time.sleep(1)
    print "Matches: ",ar_cl.setMatches(375,625)      #capacities
    time.sleep(10)
    ar_cl.setMatches(375,625)
    time.sleep(5)
    
    log_file = open(path,'a')
    log_file.write(str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + ":" + str(time.localtime()[5]) + "   " + ar_cl.getStatus() + "\n")
    
    print "Status:\n",ar_cl.getStatus()
    time.sleep(1)
    print ar_cl.getPrefl()
    a = raw_input("Press Enter to start process.")
    
    #commands
    
    count = 0
    while count < 5:   #12 x 10min = 2hours

        print time.localtime()[3],":",time.localtime()[4]," RF Power On ",ar_cl.setRFOn()   #switch on
        log_file.write(str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + str(time.localtime()[5]) + "   " + "RF Power On\n")
        
        slc = 0
        while slc < 20:   #wait 5min
            time.sleep(15)
            log_file.write(str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + str(time.localtime()[5]) + "   " + "RF Power: " + ar_cl.getPrefl() + "\n")
            if int(ar_cl.getPrefl()) > 15:
                print time.localtime()[3],":",time.localtime()[4],":",str(time.localtime()[5])," Reflected Power too high! Process aborted."
                log_file.write(str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + ":" + str(time.localtime()[5]) + "   " + "Process aborted, Prefl: " + ar_cl.getStatus().splitlines()[1].split()[1]  + "\n")
                count = 12
                break
	    slc = slc + 1
                
        print time.localtime()[3],":",time.localtime()[4],":",str(time.localtime()[5])," RF Power Off",ar_cl.setRFOff()   #switch off
        log_file.write(str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + ":" + str(time.localtime()[5]) + "   " + "RF Power Off\n")
           
        if count < 12:
            time.sleep(300);   #wait 5min
            
        count = count + 1
    
    # end operation routine
    
    time.sleep(1)
    print "Status:\n",ar_cl.getStatus()
    log_file.close()

    ar_cl.setRemoteControlOff()
    print "Setting Remote Control Off"
