# control script for Ar clean using Cesar136 version 1.0 written by JB@KIT 05/2013 

import os,sys
sys.path.append('../lib')
from er_cesar136 import Cesar136_Dev

import time,sys
import atexit
#import struct
import serial
#import os
    
    
w_err = 0 
        
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def writeStatusInLogFile():
    global w_err
    try:
        log_file.write(str(time.strftime("%H:%M:%S"))+ "   " + "Pfwd: " + str(ar_cl.getPfwd()) + "   Prefl: " + str(ar_cl.getPrefl()) + "   Ubias: " + str(ar_cl.getBias()) + "   C1: " + str(ar_cl.getC1()) + "   C2: " + str(ar_cl.getC2()) + "\n")
        #print "write"
    except:   #ignore single errors in readout
        print "Write error - ignore"
        log_file.write("Write error - ignore")
        w_err = w_err + 1
        if w_err > 4:
            raise IndexError
    return;
        
        
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


if __name__ == "__main__":   #if executed as main (and not imported)
    
    time.sleep(1)
    
    path = "../logs/log" + str(time.strftime("%d%m%y")) + "_" + str(time.strftime("%H%M%S")) + ".txt"
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
    
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #settings
    
    c1 = 355
    c2 = 605
    
    tot_time = 150   #total clean time in minutes
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
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
   
    ar_cl.setRemoteControlOff()
    a = raw_input("Adjust Matches. Press Enter to start process.")
    ar_cl.setRemoteControlOn()
    
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #commands
    
    try:
        #ar_cl.setMatchingAuto(c1,c2)
        count = 0
        p_refl_err = 0
        while count < int(tot_time) / 4:   #do (time in minutes / 4) times
    
            ar_cl.setRFOn()   #switch on
            print time.strftime("%H:%M:%S")," RF Power On"
            log_file.write(str(time.strftime("%H:%M:%S")) + "   " + "RF Power On\n")
            
            refl = 0
            slc = 0
                      #str(int(time.strftime("%d"))+(int(time.strftime("%H")) + (int(time.strftime("%M"))+2)/60)/24)
            tOff = int(str((int(time.strftime("%H")) + (int(time.strftime("%M"))+2)/60)%24) + str((int(time.strftime("%M"))+2)%60).zfill(2) + str(time.strftime("%S")))   #save time when to switch off plasma
            #                                 (hour  +   (min+2)/60)/24                                   (hour  +  (min+2)/60)%24                                        (min+2)%60                                       sec
            #print tOff
            
            err = 0
            while int(time.strftime("%H%M%S")) < tOff - 10:   #wait 2min
                time.sleep(8)
                writeStatusInLogFile()
            
                try:
                    refl = refl + int(ar_cl.getPrefl())
                except:
                    print "Error reading out Prefl - ignore"
                    err = err + 1
                    if err > 4:
                        raise IndexError
                    
                if refl/3 > 20:   #if reflected power too high
                    print time.strftime("%H:%M:%S"), "Reflected Power too high! Switch off\n"
                    ar_cl.setRFOff()   #switch off
                    p_refl_err = p_refl_err + 1
                    writeStatusInLogFile()
                    if p_refl_err > 2:   #if too many errors occured
                        log_file.write("Reflected Power too high! Process aborted.\n")
                        count = int(tot_time) / 4 + 1
                        ar_cl.setRFOff()   #switch off
                        print "RF finally off."
                        break
                    else:   #ok so far
                        time.sleep(4)
                        ar_cl.setRFOn()   #switch on, retry
                        print time.strftime("%H:%M:%S")," RF Power On, retry"
                        refl = 0
                    
                if slc % 3 == 2:   #initialize every three iterations
                    refl = 0
                    
   	        slc = slc + 1
               
            if tOff - int(time.strftime("%H%M%S")) < 12:
                time.sleep(tOff - int(time.strftime("%H%M%S")))     #make 2 min full
            else:
                time.sleep(5)   #catch exception (possibly occuring at midnight -> be careful when cleaning at midnight...)
                
            ar_cl.setRFOff()   #switch off
            print time.strftime("%H:%M:%S")," RF Power Off"
            log_file.write(str(time.strftime("%H:%M:%S")) + "   " + "RF Power Off\n")
            
            if count < int(tot_time) / 4:
                #ar_cl.setRemoteControlOff()   #Setting Remote Control Off
                time.sleep(120);   #wait 2min
                #ar_cl.setRemoteControlOn()   #Setting Remote Control On
                p_refl_err = 0   #reset Prefl error count
                
            count = count + 1
    
    except Exception as detail:
        ar_cl.setRFOff()   #switch off
        print time.strftime("%H:%M:%S")," RF Power Off due to   ",detail
        log_file.write(str(time.strftime("%H:%M:%S")) + "   " + "RF Power Off\n")
    
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # end operation routine
    
    time.sleep(0.1)
    print "Status:\n",ar_cl.getStatus()
    log_file.close()

    ar_cl.setRemoteControlOff()
    print "Setting Remote Control Off"