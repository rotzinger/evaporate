# control script for pressures in MC and LL version 0.2
# written by JB@KIT 07/2013, 12/2016

import os,sys
sys.path.append('../lib')
from er_MKS_PDR900 import Pressure_Dev

import time
import os

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


if __name__ == "__main__":   #if executed as main (and not imported)

    time.sleep(1)
    interv = 20   #logging interval in seconds
    
    print "Running..."
    
    pLL = Pressure_Dev("LL")
    pMC = Pressure_Dev("MC")
    
    while True:
	folder = os.path.join('../logs',time.strftime('%Y'),time.strftime('%m%Y'))
	if not os.path.exists(folder):
		os.makedirs(folder)
	filename = os.path.join(folder,'p_log'+time.strftime('%d%m%y')+'.dat')
        #path = "../logs/pressurelog" + str(time.strftime("%d%m%y")) + ".txt"
        #log_file = open(filename,'w')   #create log file
        
        while int(time.strftime("%H%M",time.localtime(time.time()+interv+5))) != 0:
            with open(filename,'a') as f: f.write(str(time.strftime("%H:%M:%S")) + ":   LL: " + str(pLL.getPressure()) + "   MC: " + str(pMC.getPressure()) + "\n")
            time.sleep(interv)
            
        #log_file.close()
        time.sleep(70)
