# Pressure MKS DEV version 1.0 written by JB@KIT 2013
# 
import time,sys
import atexit

class Pressure_Dev(object): 
    def __init__(self):

        self.ack="ACK"
        self.nak="NAK"
        baudrate = 9600
        timeout = 0.1
        
        # Port B on the USB_to_serial converter
	device = "/dev/ttyUSB1"
        self.ser = self._std_open(device,baudrate,timeout)
        atexit.register(self.ser.close)
            
        # load inficon comands
        
        
    def _std_open(self,device,baudrate,timeout):
        import serial
        # open serial port, 9600, 8,N,1, timeout 0.1
        return serial.Serial(device, baudrate, timeout=timeout)
        
    def remote_cmd(self,cmd):
        cmd+="\n"

        # clear queue first, old data,etc
        #rem_char = self.ser.inWaiting()
        #if rem_char:
        #    self.ser.read(rem_char)
        
        # send command
        self.ser.write(cmd)
        # wait until data is processed
        time.sleep(0.2)
        # read back
        rem_char = self.ser.inWaiting()
        value = self.ser.read(rem_char)
        return value
        
    
    def getTM1(self):
        #self.remote_cmd("@001DL?;FF")
        # "TM1:MBAR  : 1.00E+03"
	#print value
	return self.remote_cmd("@001DL?;FF")
	#try:
        #	gauge,pressure = value.split(" : ")
        #	return float(pressure.strip())
    	#except:
	#	return None

    def getTM2(self):
        value = self.remote_cmd("MES R TM2")
        # "TM1:MBAR  : 1.00E+03"
	try:
        	gauge,pressure = value.split(" : ")
		return float(pressure.strip())
    	except:
		return None
    def getUHV(self):
        value = self.remote_cmd("MES R PM1")
        try:
                gauge,pressure = value.split(" : ")
                return float(pressure.strip())
        except:
		print 'er_combivac exception ...'
                return None
                
    def getSerial(self):
        return self.remote_cmd("@001SNC?;FF")
        
    def getAddress(self):
        return self.remote_cmd("@254ADC?;FF")
        
    #transducer methods
    
    def getSerialT(self):
        return self.remote_cmd("@002SN?;FF")
        
    def getBaudT(self):
        return self.remote_cmd("@xxxBR?;FF")
        
    def getAddressT(self):
        return self.remote_cmd("@xxxAD?;FF")
        
    def getDelayT(self):
        return self.remote_cmd("@xxxRSD?;FF")
        
    def getPressure(self):
        return self.remote_cmd("@002PR3?;FF")
    
        
                
if __name__ == "__main__":
    p1 = Pressure_Dev()
    #print p1.setHV(on=False)
    #print "Penning:", p1.getUHV()
    #print "Pirani 1:", p1.getTM1()    
    #print p1.getSerial()
    print p1.getSerial()
    time.sleep(1)
    print p1.getSerialT()
    time.sleep(1)
    print p1.getAddressT()
    time.sleep(1)
    print p1.getBaudT()
    time.sleep(1)
    print p1.getDelayT()
    time.sleep(1)
    print p1.getPressure()
