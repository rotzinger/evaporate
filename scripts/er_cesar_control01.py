# control script for Ar clean using Cesar136 version 0.1 written by JB@KIT 05/2013

from lib.er_cesar136 import Cesar136_Dev

import time,sys
import atexit
#import struct
import serial
        

if __name__ == "__main__":   #if executed as main (and not imported)
    
    time.sleep(1)
    
    log_file = open("log" + str(time.localtime()[2]) + str(time.localtime()[1]) + str(time.localtime()[0]) + ".txt",'w')   #create log file
    log_file.close()
    
    ar_cl = Cesar136_Dev()   #Ar clean
    print "Setting Echo Mode On",ar_cl.EchoModeOn()
    print "Setting Remote Control On",ar_cl.setRemoteControlOn()
    print "Pulse Mode Off",ar_cl.setPulseMode(0,0,0)
    print "ICP Mode Off",ar_cl.setICPMode(0,0,0,0,0,0)    
    
    # start operation routine
    
    #settings
    print "Mode: ",ar_cl.setOperationMode(0,100,0)   #P_fwd = 100W
    print "Matches: ",ar_cl.setMatches(375,580)      #capacities
    
    time.sleep(3)
    
    log_file = open("log" + str(time.localtime()[2]) + str(time.localtime()[1]) + str(time.localtime()[0]) + ".txt",'a')
    log_file.write(str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + "   " + ar_cl.getStatus() + "\n")
    
    print "Status:\n",ar_cl.getStatus()
    time.sleep(5)
    
    #commands
    
    count = 0
    while count < 12:   #12 x 10min = 2hours

        print time.localtime()[3],":",time.localtime()[4]," RF Power On ",ar_cl.setRFOn()   #switch on
        log_file.write(str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + "   " + "RF Power On\n")
        
        slc = 0
        while slc < 10:   #wait 5min
            time.sleep(30);
            log_file.write(str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + "   " + "RF Power: " + ar_cl.getStatus().splitlines()[1].split()[1]  + "\n")
            if int(ar_cl.getStatus().splitlines()[1].split()[1]) > 15:
                print time.localtime()[3],":",time.localtime()[4]," Reflected Power too high! Process aborted."
                log_file.write(str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + "   " + "Process aborted, Prefl: " + ar_cl.getStatus().splitlines()[1].split()[1]  + "\n")
                count = 12
                break
                
        print time.localtime()[3],":",time.localtime()[4]," RF Power Off ",ar_cl.setRFOff()   #switch off
        log_file.write(str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + "   " + "RF Power Off\n")
           
        if count < 12:
            time.sleep(300);   #wait 5min
            
        count = count + 1
    
    # end operation routine
    
    log_file.close()