# control script for pressures in MC and LL version 0.1 written by JB@KIT 07/2013

import os,sys
sys.path.append('../lib')
from er_MKS_PDR900 import Pressure_Dev

import time,sys

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


if __name__ == "__main__":   #if executed as main (and not imported)

    time.sleep(1)
    
    print "Running..."
    
    pLL = Pressure_Dev("LL")
    pMC = Pressure_Dev("MC")
    
    while True:
        path = "../logs/pressurelog" + str(time.strftime("%d%m%y")) + ".txt"
        log_file = open(path,'w')   #create log file
        
        while int(time.strftime("%H%M%S",time.localtime(time.time()+65))) < 235959:
            log_file.write(str(time.strftime("%H:%M:%S")) + ":   LL: " + str(pLL.getPressure()) + "   MC: " + str(pMC.getPressure()) + "\n")
            time.sleep(10)
            
        log_file.close()
        time.sleep(70)