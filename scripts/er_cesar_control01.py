# control script for Ar clean using Cesar136 version 0.2 written by JB@KIT 05/2013

import os,sys
sys.path.append('../lib')
from er_cesar136 import Cesar136_Dev

import time,sys
import atexit
#import struct
import serial
#import os
        
        
def writeStatusInLogFile():
    log_file.write(str(time.strftime("%H:%M:%S"))+ "   " + "Pfwd: " + ar_cl.getPfwd() + "   Prefl: " + ar_cl.getPrefl + "   Ubias: " + ar_cl.getBias() + "   C1: " + ar_cl.getC1 + "   C2: " + ar_cl.getC2() + "\n")
    return;
        

if __name__ == "__main__":   #if executed as main (and not imported)
    
    time.sleep(1)
    
    path = "../logs/log" + str(time.strftime("%d/%m/%y")) + "_" + str(time.strftime("%H:%M:%S")) + ".txt"
    log_file = open(path,'w')   #create log file
    log_file.close()
    print "Log-File in /logs: ",path
    
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
    
    c1 = 375
    c2 = 625
    
    ar_cl.setOperationMode(0,100,0)
    print "Pfwd: 100W"   #P_fwd = 100W
    time.sleep(0.1)
    ar_cl.setMatches(c1,c2) 
    print "Matches: ",c1,",",c2    #capacities
    time.sleep(10)
    ar_cl.setMatches(c1,c2)
    time.sleep(5)
    
    log_file = open(path,'a')
    log_file.write(str(time.strftime("%H:%M:%S")) + "Status:   " + ar_cl.getStatus() + "\n")
    
    print "Status:\n",ar_cl.getStatus()
    time.sleep(0.1)
    #print ar_cl.getPrefl()
    a = raw_input("Press Enter to start process.")
    
    #commands
    
    count = 0
    while count < 30:   #30 x 4min = 2hours

        ar_cl.setRFOn()   #switch on
        print time.localtime()[3],":",time.localtime()[4]," RF Power On "
        ar_cl.setMatchingAuto(c1,c2)
        log_file.write(str(time.strftime("%H:%M:%S")) + "   " + "RF Power On\n")
        
        slc = 0
        while slc < 10:   #wait 2min
            time.sleep(12)
            writeStatusInLogFile()
            if int(ar_cl.getPrefl()) > 15:   #if reflected power too high
                print time.strftime("%H:%M:%S"), "Reflected Power too high! Process aborted."
                writeStatusInLogFile()
                log_file.write("Process aborted.\n")
                count = 30
                break
	    slc = slc + 1
                
        ar_cl.setRFOff()   #switch off
        print time.strftime("%H:%M:%S")," RF Power Off"
        log_file.write(str(time.strftime("%H:%M:%S")) + "   " + "RF Power Off\n")
           
        if count < 30:
            time.sleep(120);   #wait 2min
            
        count = count + 1
    
    # end operation routine
    
    time.sleep(0.1)
    print "Status:\n",ar_cl.getStatus()
    log_file.close()

    ar_cl.setRemoteControlOff()
    print "Setting Remote Control Off"
