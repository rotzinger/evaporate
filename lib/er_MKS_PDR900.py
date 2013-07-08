# Pressure MKS DEV version 1.0 written by JB@KIT 2013
# 
import time,sys
import atexit

class Pressure_Dev(object): 
    def __init__(self,device_sel = "LL"):

        self.ack="ACK"
        self.nak="NAK"
        baudrate = 9600
        timeout = 0.1
        
        if device_sel == "MC":
	   device = "/dev/ttyUSB2"
	else:
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
        return self.remote_cmd("@001SNC?;FF")[7:-3]
        
    def getAddress(self):
        return self.remote_cmd("@254ADC?;FF")
        
    #transducer methods
        
    def getBaudT(self):
        return self.remote_cmd("@xxxBR?;FF")[7:-3]
        
    def getAddressT(self):
        return self.remote_cmd("@xxxAD?;FF")[7:10]
        
    def getPressure(self,address):
        return self.remote_cmd("@" + address + "PR3?;FF")[7:14]
        
                
if __name__ == "__main__":
    pMC = Pressure_Dev("MC")
    #print p1.getSerial()
    print "Baudrate Transducer MC: ", pMC.getBaudT()
    addrMC = str(pMC.getAddressT())    #transducer address
    print "Pressure: ", pMC.getPressure(addrMC)
    
    pLL = Pressure_Dev("LL")
    print "Baudrate Transducer LL: ", pMC.getBaudT()
    addrLL = str(pLL.getAddressT())    #transducer address
    print addrLL
    print "Pressure LL: ", pMC.getPressure(addrLL)