# MKS MFC Controller 647C DEV version 1.0 written by HR/JB@KIT 10/2013
# Mass flow controller monitor/controller

import time,sys
import atexit
#import struct
import serial
from threading import Lock

class MKS647C_Dev(object):
        
    def __init__(self,channel = 1 ,mutex = None, SerialPort = None):
        self.channel = channel
        if mutex:
            self.mutex = mutex
        else:
            self.mutex = Lock()
            
        if SerialPort:
            self.SerialPort =  SerialPort
        else:    
            # open serial port, 9600, 8,N,1, timeout 1s
            #device="/dev/tty.usbserial"
            baudrate = 9600
            timeout = 1
            # Port A on the USB_to_serial converter, Port B ends with K
            #device = "/dev/cu.usbserial-FTK3DEL5A"
            device = "/dev/ttyUSB3" 
            self.SerialPort = self._std_open(device,baudrate,timeout)
            atexit.register(self.SerialPort.close)
        
    def _std_open(self,device,baudrate,timeout):
        return serial.Serial(device, baudrate, timeout=timeout)
    def getSerialPort(self):
        return self.SerialPort
    def getMutex(self):
        return self.mutex
    def remote_cmd(self,cmd):
        # the 647C requires carriage return termination
        cmd += '\r'
        with self.mutex:
            self.SerialPort.write(cmd)
        
            time.sleep(0.2)   #increase from .1 to .2
            #value = self.ser.readline().strip("\x06")
            rem_char = self.SerialPort.inWaiting()
        
            value = self.SerialPort.read(rem_char) # .strip("\x06")
            time.sleep(0.2)   #to avoid wrong communication
            return value.strip()
        
        
        
    def getFlowSetPoint(self):
    	cmd = "FS " + str(self.channel) +" R"
    	flow = self.remote_cmd(cmd)   #gives N2 flow #indent error?
    	return float(flow)/10*self.getGasCorrectionFactor()
    def setFlowSetPoint(self,value):
        cmd = "FS " + str(self.channel) + str(int(float(value)/self.getGasCorrectionFactor()*10))
        return self.remote_cmd(cmd)   
    
    
    def getActualFlow(self):
        cmd = "FL " + str(self.channel)
        flow = self.remote_cmd(cmd)   #gives N2 flow
        return float(flow)/10*self.getGasCorrectionFactor()
    
    
    def getPressureSetPoint(self):
        cmd = "PS R"
        return self.remote_cmd(cmd)
    def setPressureSetPoint(self,value):
        # value in 0.1 percent of fullscale: 0..1100
        cmd = "PS "+str(value)
        return self.remote_cmd(cmd)    
    
    def getActualPressure(self):
        cmd = "PR"
        return self.remote_cmd(cmd)
        
    def getActualPCS(self):
        #check for PCS
        cmd = "PC"
        return self.remote_cmd(cmd)
    
    def setPressureMode(self,On = True):
        # On = 1 (Auto)
        # Off = 0
        if On:
            cmd = "PM 1"
        else:
            cmd = "PM 0"
        return self.remote_cmd(cmd)
    
    def PressureModeOn(self):
        cmd = "PM R"
        status = self.remote_cmd(cmd)
        if int(status) == 1:
            return True
        else:
            return False
        
    def setFlowRange(self,value):
        """
        # most likely only 3 and 6 are used 
        0  = 1.000 SCCM 
        1  = 2.000 SCCM 
        2  = 5.000 SCCM 
        3  = 10.00 SCCM 
        4  = 20.00 SCCM 
        5  = 50.00 SCCM 
        6  = 100.0 SCCM 
        7  = 200.0 SCCM 
        8  = 500.0 SCCM 
        9  = 1.000 SLM
        10 = 2.000 SLM 
        11 = 5.000 SLM 
        12 = 10.00 SLM 
        13 = 20.00 SLM 
        14 = 50.00 SLM 
        15 = 100.0 SLM 
        16 = 200.0 SLM 
        17 = 400.0 SLM 
        18 = 500.0 SLM 
        19 = 1.000 SCMM 
        20 = 1.000 SCFH
        21 = 2.000 SCFH
        22 = 5.000 SCFH
        23 = 10.00 SCFH
        24 = 20.00 SCFH
        25 = 50.00 SCFH
        26 = 100.0 SCFH
        27 = 200.0 SCFH
        28 = 500.0 SCFH
        29 = 1.000 SCFM
        30 = 2.000 SCFM
        31 = 5.000 SCFM
        32 = 10.00 SCFM
        33 = 20.00 SCFM
        34 = 50.00 SCFM
        35 = 100.0 SCFM
        36 = 200.0 SCFM
        37 = 500.0 SCFM
        38 = 30.00 SLM
        39 = 300.0 SLM 
        
        """
        cmd = "RA "+str(self.channel)+" "+str(value)
        return self.remote_cmd(cmd)
        
    def setFlowRange10sccm(self):
        return self.setFlowRange(3)
        
    def setFlowRange100sccm(self):
        return self.setFlowRange(6)
    
    def getFlowRange(self):
        # from manual,
        flows = [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 
                 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 400.0, 500.0, 
                 1.0, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 
                 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 30.0, 300.0]
        units = ['SCCM', 'SCCM', 'SCCM', 'SCCM', 'SCCM', 'SCCM', 'SCCM', 'SCCM', 'SCCM', 
                 'SLM', 'SLM ', 'SLM ', 'SLM ', 'SLM ', 'SLM ', 'SLM ', 'SLM ', 'SLM ', 'SLM ', 
                 'SCMM', 'SCFH', 'SCFH', 'SCFH', 'SCFH', 'SCFH', 'SCFH', 'SCFH', 'SCFH', 
                 'SCFH', 'SCFM', 'SCFM', 'SCFM', 'SCFM', 'SCFM', 'SCFM', 'SCFM', 'SCFM', 
                 'SCFM', 'SLM', 'SLM ']
        
        cmd = "RA "+str(self.channel)+" R"
        flownum = int(self.remote_cmd(cmd))
        return flows[flownum],units[flownum]
    
    def setGasCorrectionFactor(self,factor):
    	#ffactor = "00" + str(factor).strip(".")
        cmd = "GC "+str(self.channel)+str(factor)
        return self.remote_cmd(cmd)
    
    def getGasCorrectionFactor(self):
        cmd = "GC "+str(self.channel)+" R"
        res = self.remote_cmd(cmd)
	return float(res)/100
    
    def setMode(self,mode = 0, master_channel = 0):
        """
        MO c m [i]channel
        c = 1..8 
        m = 0 mode = independent
        m = 1 mode = slave
        m = 2 mode = extern
        m = 3 mode = PCS
        m = 9 mode = test
        i = 1..8 modeindex, reference to master (only if m equal 1) 
        """
        if mode == 1:
            cmd = "MO "+ str(self.channel) +" 1 "+ str(master_channel)
        else:
            cmd = "MO "+ str(self.channel) +str(mode)
    def getMode(self):
        master_channel = -1
        cmd = "GC "+str(self.channel)+" R"
        mode, master_channel = (self.remote_cmd(cmd)).split()
        return int(mode), int(master_channel)
    
    
    def setHighLimit(self,l):   #in 0.1 percent: 0..1100
        cmd = "HL " + str(self.channel) + " " + str(l)
        return self.remote_cmd(cmd)
        
    def setLowLimit(self,l):
        cmd = "LL " + str(self.channel) + " " + str(l)
        return self.remote_cmd(cmd)
        
    def getHighLimit(self):   #in 0.1 percent: 0..1100
        cmd = "HL " + str(self.channel) + " R"
        return self.remote_cmd(cmd)
        
    def getLowLimit(self):
        cmd = "LL " + str(self.channel) + " R"
        return self.remote_cmd(cmd)
    
    def setPressureUnit(self,pu = 13):
        cmd = "PU " + str(pu)
        return self.remote_cmd(cmd)
    """ 
    15: 1mbar
    13: 100ubar
    11: 1ubar
    """
    def getPressureUnit(self):
        cmd = "PU R"
        return self.remote_cmd(cmd)
        
    
    def setOnAll(self):
    	return self.remote_cmd("ON 0")
    def setOn(self):
        return self.remote_cmd("ON " + str(self.channel))
    def setOffAll(self):
        return self.remote_cmd("OF 0")
    def setOff(self):
        return self.remote_cmd("OF " + str(self.channel))
        
        
    def check_channelStatus(self):
        return self.remote_cmd("ST " + str(self.channel))
        
    def setDefault(self):
        return self.remote_cmd("DF")
        
    def hardware_reset(self):
        return self.remote_cmd("RE")
        
    def getVersion(self):
        return self.remote_cmd("ID")
	 
    """
    # commands for setting values with the power supply
    
    def check_range(self,value,minval,maxval):
        if value < minval or value > maxval:
            print "value out of range error: " + str(value) + " " + str(minval) + " " + str(maxval)
            raise ValueError
        
    def setOn(self,ON = False):
        if ON:
            self.remote_cmd('A')        
        else:
            self.remote_cmd('B')            
	"""
   
    def init_controller(self):
        print "Initializing controller..."
	self.setPressureUnit()
		
	self.channel = 1	#Argon
	self.setFlowSetPoint(19)
	self.setFlowRange100sccm()
	self.setGasCorrectionFactor("0137")
	self.channel = 2	#N2
	self.setFlowSetPoint(0)
	self.setFlowRange100sccm()
	self.setGasCorrectionFactor("0100")
	
	self.channel = 3	#O2
	self.setFlowSetPoint(0)
	self.setFlowRange100sccm()
	self.setGasCorrectionFactor("0100")
	
	self.channel = 4	#ArO2
	self.setFlowSetPoint(0)
	self.setFlowRange10sccm()
	self.setGasCorrectionFactor("0100") #1.12
	print "Done."



if __name__ == "__main__":

    Ar = MKS647C_Dev(1)
    mutex = Ar.getMutex()
    N2 = MKS647C_Dev(2,mutex)
    O2 = MKS647C_Dev(3,mutex)
    ArO = MKS647C_Dev(4,mutex)
    
    print "Setting off all", Ar.setOffAll()

    Ar.init_controller()
    """
    print "Version: ",Ar.getVersion()
    print Ar.getFlowSetPoint()
    print N2.getFlowSetPoint()
    print O2.getFlowSetPoint()
    print ArO.getFlowSetPoint()

    print Ar.getGasCorrectionFactor()
    print N2.getGasCorrectionFactor()
    
    print Ar.getActualFlow()
    print N2.getActualFlow()
    print O2.getActualFlow()
    print ArO.getActualFlow()
    
    print Ar.setFlowSetPoint(19)
    print N2.setFlowSetPoint(15)
    print O2.setFlowSetPoint(16)
    print ArO.setFlowSetPoint(7)
    
    time.sleep(1)
    
    print Ar.getFlowSetPoint()
    print N2.getFlowSetPoint()
    print O2.getFlowSetPoint()
    print ArO.getFlowSetPoint()
    
    print Ar.getFlowRange()
    print N2.getFlowRange()
    print O2.getFlowRange()
    print ArO.getFlowRange()
    
    print Ar.getActualPressure()
    
    print Ar.setFlowRange100sccm()
    print N2.setFlowRange10sccm()
    print O2.setFlowRange100sccm()
    print ArO.setFlowRange10sccm()
    
    print Ar.getFlowSetPoint()
    print N2.getFlowSetPoint()
    print O2.getFlowSetPoint()
    print ArO.getFlowSetPoint()
    
    print Ar.getGasCorrectionFactor()
    print Ar.setGasCorrectionFactor("0120")
    print Ar.getGasCorrectionFactor()
    
    print Ar.getPressureUnit()
    """
