# CESAR 136 version 0.1 written by JB@KIT 05/2013
# RF-Generator for plasma clean
#13.56MHz, 600W

import time,sys
import atexit
import serial

class Cesar136_Dev(object):
        
    def __init__(self):    #initialize new insatances
        # open serial port, 9600, 8,N,1, timeout 1s
        #device="/dev/tty.usbserial"
        baudrate = 9600
        timeout = 0.1
        # Port A on the USB_to_serial converter, Port B ends with K
        #device = "/dev/cu.usbserial-FTK3DEL5A"
        device = "/dev/ttyUSB0" 
        self.ser = self._std_open(device,baudrate,timeout)
        atexit.register(self.ser.close)
        
    def _std_open(self,device,baudrate,timeout):
        return serial.Serial(device, baudrate, timeout=timeout)
                
    def remote_cmd(self,cmd):
	cmd+='\n'
        self.ser.write(cmd)
        
        time.sleep(0.5)    #wait 0.5s
        #value = self.ser.readline().strip("\x06")
        rem_char = self.ser.inWaiting()
        
        value = self.ser.read(rem_char) # .strip("\x06")
        #print "##"+value+"##"+value.strip()+"###"
        return value #.strip()
    
       
    #commands and settings
    
    def setEchoModeOn(self):
        return self.remote_cmd("SECHO 1")
    def setEchoModeOff(self):
        return self.remote_cmd("SECHO 0")
       
    def setRemoteControlOff(self):
        return self.remote_cmd("SRC 0");     
    def setRemoteControlOn(self):
        return self.remote_cmd("SRC 1");
        
    def setRFOff(self):
        return self.remote_cmd("SRF 0")
    def setRFOn(self):
        return self.remote_cmd("SRF 1")

    
    def setOperationMode(self,mode,p,bias):
        return self.remote_cmd("SOM " + str(mode) + " " + str(p) + " " + str(bias))
        
    def setPulseMode(self,mode,f,duty_cycle):
        return self.remote_cmd("SPM " + str(mode) + " " + str(f) + " " + str(duty_cycle))
        
    def setMatches(self,c1,c2):
        return self.remote_cmd("SMAT 0 " + str(c1) + " " + str(c2))
    def setMatchingAuto(self,c1,c2):
        return self.remote_cmd("SMAT 1 " + str(c1) + " " + str(c2))
        
    def setICPMode(self,state,c1,c2,p_ign,p_fwd,t_ign):
        return self.remote_cmd("SICP " + str(c1) + " " + str(c2) + " " + str(p_ign) + " " + str(p_fwd) + " " + str(t_ign))
        
        
    #info
    #def info(self,cmd):
    #    return self.remote_cmd(cmd)
    
    def getStatus(self):
        return self.remote_cmd("GST")
    def getPfwd(self):
        self.setEchoModeOff()
        return self.getStatus().split()[1]
    def getPrefl(self):
        self.setEchoModeOff()
        return self.getStatus().split()[2]
    def getBias(self):
        self.setEchoModeOff()
        return self.getStatus().split()[3]
    def getC1(self):
        self.setEchoModeOff()
        return self.getStatus().split()[4]
    def getC2(self):
        self.setEchoModeOff()
        return self.getStatus().split()[5]
        
        

if __name__ == "__main__":   #if executed as main (and not imported)
    time.sleep(1) 
    rd = Cesar136_Dev()

    #print "Setting Echo Mode On",rd.setEchoModeOn()
    print "Setting Echo Mode Off",rd.setEchoModeOff()
    print "Setting Remote Control On",rd.setRemoteControlOn()
    print "Status:"
    return_val = rd.getStatus()
    ret_val_split = return_val.split()
    for i in str(return_val): print "#",i,"#", hex(str(i))
    print len(return_val), return_val.split()
    print "Setting RF on:", rd.setRFOn()
    print "waiting 5s...",time.sleep(5)
    print "Setting RF off:", rd.setRFOff()
    print "Setting LOCAL Mode",rd.setRemoteControlOff()
 
