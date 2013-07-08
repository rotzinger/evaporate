# pressure readout for pressures in MC and LL version 0.1 written by JB@KIT 07/2013

import os,sys
sys.path.append('../lib')
from er_MKS_PDR900 import Pressure_Dev

import time,sys

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


if __name__ == "__main__":   #if executed as main (and not imported)

    #time.sleep(1)
    pLL = Pressure_Dev("LL")
    pMC = Pressure_Dev("MC")
    
    while True:
        print str(time.strftime("%H:%M:%S")) +  "   LL: " + str(pLL.getPressure()) + "   MC: " + str(pMC.getPressure())
        a = raw_input("More?")
        if a == "q":
            break
        #time.sleep(20)