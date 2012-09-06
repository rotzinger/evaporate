# Pressure DEV version 0.1 written by HR@KIT 2012
# leybold/inficon ionivac + combivac it23 monitor  
import time,sys
import atexit
import struct
class Pressure_Dev(object): 
    def __init__(self):

        self.ack="\x06"
        self.nak="\x15"
        baudrate = 9600
        timeout = 0.1
        
        # Port A on the USB_to_serial converter,Port A with C, Port B ends with K
        device = "/dev/tty.usbserial-FTB4J8SK"
	device = "/dev/tty.usbserial"
	device = "/dev/ttyUSB0"
        self.ser = self._std_open(device,baudrate,timeout)
        atexit.register(self.ser.close)

    def _Unpack_Cmd(self,data):
	
	""" From the inficon manual
	0 Datenstring-Laenge 7 (fester Wert)
	1 Seiten Nr. 5
	2 Status : Status-Byte
	3 Fehler : Fehler-Byte
	4 Messwert high Byte 0 ... 255 : Berechnen des Druckwertes
	5 Messwert low Byte 0 ... 255 : Berechnen des Druckwertes
	6 Software-Version 0 ... 255 : Softwareversion
	7 Sensortyp 10 (fur BPG400-Messroehren)
	8 Checksumme 0 ... 255 : Synchronisation
	"""
	
        "unpack and return data"
        fmt=">9B"
        data_str_len, page_nr, Status, Error, Value_high, Value_low, SW_Version, Sensor_Type, csm = struct.unpack(fmt,data)
	# check checksum
	fmt = ">7B"
	binstr = struct.pack(fmt, page_nr, Status, Error, Value_high, Value_low, SW_Version, Sensor_Type)
	# calc and add checksum
	calc_csm = reduce(lambda x,y:x+y, map(ord, binstr)) % 256
	if calc_csm == csm:
	    return self.calc_pressure_from_data(Value_high, Value_low)
	else:
	    #print calc_csm, csm
	    return None
	
	# one also has access to the following data ...
        #return  data_str_len, page_nr, Status, Error, Value_high, Value_low, SW_Version, Sensor_Type, csm

    def calc_pressure_from_data(self,Value_high, Value_low):
	return 10**((Value_high * 256. + Value_low) / 4000 - 12.5)
	
    def _std_open(self,device,baudrate,timeout):
        import serial
        # open serial port, 9600, 8,N,1, timeout 0.1
        return serial.Serial(device, baudrate, timeout=timeout)
        
    def pick_data_from_stream(self):

        # clear queue first, old data,etc
	#time.sleep(0.05)
        rem_char = self.ser.inWaiting()
	#print rem_char
        if rem_char:
            self.ser.read(rem_char)	
	# now the fresh data ....
	time.sleep(0.1)
	# read back
	rem_char = self.ser.inWaiting()
	# print rem_char
	# rem_char = 9
	value = self.ser.read(rem_char)
	# converting to a bytearray makes live easier ...
	value = bytearray(value)
	
	# simply just take the first one captured nine bytes where the 
	# pattern matches, 
	# FIXME: the checksum is checked but not reported, 
	# only "None" is returned in case of a mismatch
	for i,b in enumerate(value):
	    if i+9<len(value) and b==7 and value[i+1] == 5:
		return self._Unpack_Cmd(str(value[i:i+9]))


    def getTM1(self):
	# the IONIVAC does not need this call
	pass

    def getTM2(self):
	# the IONIVAC does not need this call
	pass
    
    def getUHV(self):
	"main and only func to be called from outside"
	data = self.pick_data_from_stream()
    	if data:
	     return data
        else:
             raise IOError
    def setHV(self,on=True):
	# not implemented
	pass

if __name__ == "__main__":
    p1 = Pressure_Dev()
    print p1.pick_data_from_stream()
