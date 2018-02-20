# AJA DCXS DEV version 0.1 written by HR@KIT 12/2012
# Power supply for sputtering guns
import time
import atexit
#import struct
import serial

class DCXS_Dev(object):
        
    def __init__(self, device = "/dev/ttyUSB7" ):
        # open serial port, 9600, 8,N,1, timeout 1s
        #device="/dev/tty.usbserial"
        baudrate = 38400
        timeout = 0.1
        # Port A on the USB_to_serial converter, Port B ends with K
        #device = "/dev/cu.usbserial-FTK3DEL5A"
        #device = "/dev/ttyUSB0" 
        self.ser = self._std_open(device,baudrate,timeout)
        atexit.register(self.ser.close)
        
    def _std_open(self,device,baudrate,timeout):
        return serial.Serial(device, baudrate, timeout=timeout)
                
    def remote_cmd(self,cmd):
        self.ser.write(cmd)
        
        time.sleep(0.1)
        #value = self.ser.readline().strip("\x06")
        rem_char = self.ser.inWaiting()
        
        value = self.ser.read(rem_char) # .strip("\x06")
        #print "##"+value+"##"+value.strip()+"###"
        return value #value.strip()
    
        
    def getVersion(self):
        return self.remote_cmd("?")
    def getState(self):
        return self.remote_cmd("a")    
    def getSetPoint(self):
        return self.remote_cmd("b")
    def getRegulationMode(self):
        """
        if mode = 0:
            # Power
        if mode = 1:
            # Voltage
        if mode = 2:
            # Current
        """
        return self.remote_cmd("c")
        
    def getPower(self):
        return self.remote_cmd("d")
    def getCurrent(self):
        return self.remote_cmd("f")
    def getVoltage(self):
        return self.remote_cmd("e")
    def getTotalTime(self):
        minutes = self.remote_cmd("i")
        seconds = self.remote_cmd("j")
        return minutes, seconds
    def getRemainingTime(self):
        minutes = self.remote_cmd("k")
        seconds = self.remote_cmd("l")
        return minutes, seconds
    def getFault(self):
        return bool(self.remote_cmd("o"))
    def getMaterial(self):
        return self.remote_cmd("n")    
    def getGun(self):
        return self.remote_cmd("y")
    
    # commands for setting values with the power supply
    
    def check_range(self,value,minval,maxval):
        if value < minval or value > maxval:
            print "value out of range error: " + str(value) + " " + str(minval) + " " + str(maxval)
            raise ValueError
    """   
    def setOn(self,ON = False):
        if ON:
            self.remote_cmd('A')        
        else:
            self.remote_cmd('B')      
    """
    def setStatus(self,status = True):
        if status:
            self.remote_cmd('A')
        else:
            self.remote_cmd('B')
        
    def setPoint(self,value):
        self.check_range(value,0,1000)
        cmd = 'C'+str(value)
        self.remote_cmd(cmd) 
        
    def setPower(self,value):
        self.setPoint(value)

    def setRegulationMode(self,mode):
        self.check_range(value,0,2)
        cmd = 'D'+str(mode)
        self.remote_cmd(cmd)

    def setDepositionTime(self,minutes,seconds):
        self.check_range(minutes,0,999)
        cmd = 'G'+str(minutes)
        self.remote_cmd(cmd)
        
        self.check_range(seconds,0,59)
        cmd = 'H'+str(seconds)
        self.remote_cmd(cmd)
    
    def setMaterialName(self,name):
        if len(name) > 8:
            print "Maximal length for material name is 8 characters!"
            raise ValueError
        cmd = 'I'+str(name)
        self.remote_cmd(cmd)    
    
    def setGunToEdit(self,gun_num):
        self.check_range(gun_num,0,5)
        cmd = 'Z'+str(gun_num)
        self.remote_cmd(cmd)        

if __name__ == "__main__":
    rd=DCXS_Dev()
    #print rd.getHello()
    print 'Version:',rd.getVersion()
    print 'Voltage:',rd.getVoltage()
    print 'TotalTime',rd.getTotalTime()
    #print 'Gun', rd.getGun()
    #print "reg",rd.setRegulationMode()
    #print 'SetPower',rd.setPower(3)
    print 'SetOn',rd.setStatus(False)
    #print 'Thickness:',rd.getThickness()*100
