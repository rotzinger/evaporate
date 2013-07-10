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
        log_file.write("Write error - ignore\n")
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

    c1 = 430
    c2 = 726

    effective_clean_time = 16   #effective clean time in minutes
    pause_time = 30             #pause time in seconds

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
        while count < int(effective_clean_time) / 2:   #do (time in minutes / 4) times

            ar_cl.setRFOn()   #switch on
            print time.strftime("%H:%M:%S")," RF Power On"
            log_file.write(str(time.strftime("%H:%M:%S")) + "   " + "RF Power On\n")

            refl = 0
            slc = 0

            #second_end = str(time.strftime("%S"))
            #second = str((int(time.strftime("%S"))+48)%60).zfill(2)
            #minute = str((int(time.strftime("%M"))+2)%60+((int(time.strftime("%S"))+48)/60)-1).zfill(2)
            #hour = str(int(time.strftime("%H")) + ((int(time.strftime("%M"))+2)+((int(time.strftime("%S"))+48)/60)-1)/60).zfill(2)
            #tOff12 = int(hour + minute + second)   #save time when to escape routine
            tOff = int(time.strftime("%H%M%S",time.localtime(time.time()+120)))
            #print tOff

            err = 0
            while int(time.strftime("%H%M%S",time.localtime(time.time()+12))) < tOff:   #wait 2min
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
                        count = int(effective_clean_time) / 2 + 1
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

            j = 0
            while int(time.strftime("%H%M%S")) != tOff and j < 50 and count < int(effective_clean_time) / 2:
                time.sleep(0.3)     #make 2 min full
                j = j + 1

            ar_cl.setRFOff()   #switch off
            print time.strftime("%H:%M:%S")," RF Power Off"
            log_file.write(str(time.strftime("%H:%M:%S")) + "   " + "RF Power Off\n")

            if count < int(effective_clean_time) / 2:
                #ar_cl.setRemoteControlOff()   #Setting Remote Control Off
                time.sleep(int(pause_time));   #wait pause time
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