# Pressure DEV version 0.1 written by HR@KIT 2012
# 
import time,sys
import atexit
import struct
class Pressure_Dev(object): 
    # in the moment only access to a combivac cm 31
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
            
        # load inficon comands
        
    def _Pack_Cmd(self, Command, Value = 0, Type = 0):
        "_Pack_Cmd formates and returns a proper datagram with Command, Value and Type"

        fmt = ">BBBBi"
        binout = struct.pack(fmt,
                             self.address,
                             Command,
                             Type,
                             self.motor,
                             Value)
        # calc and add checksum
        csm = reduce(lambda x,y:x+y, map(ord, binout)) % 256
        binout+=struct.pack(">B",csm)
        
        if self.Debug:
                print  "_Pack_Cmd datagram \n1\t2\t3\t4\t5\t6\t7\t8\t9"
                for i in binout:
                    print hex(ord(i)),"\t",
                print ""
        return binout

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
	fmt = ">8B"
	binstr = struct.pack(fmt,data_str_len, page_nr, Status, Error, Value_high, Value_low, SW_Version, Sensor_Type)
	# calc and add checksum
	calc_csm = reduce(lambda x,y:x+y, map(ord, binstr)) % 256
	if calc_csm == csm:
	    return calc_pressure_from_data(Value_high, Value_low)
	else:
	    return None
        #return  data_str_len, page_nr, Status, Error, Value_high, Value_low, SW_Version, Sensor_Type, csm

    def calc_pressure_from_data(self,Value_high, Value_low):
	return 10**((Value_high * 256. + Value_low) / 4000 - 12.5)
	
    def _std_open(self,device,baudrate,timeout):
        import serial
        # open serial port, 9600, 8,N,1, timeout 0.1
        #device="/dev/tty.usbserial"
        return serial.Serial(device, baudrate, timeout=timeout)
        
    def read_in_string(self):

        # clear queue first, old data,etc
	time.sleep(0.05)
        rem_char = self.ser.inWaiting()
	print rem_char
        if rem_char:
            self.ser.read(rem_char)
	rem_char = self.ser.inWaiting()
	print rem_char
	time.sleep(0.1)
	# read back
	rem_char = self.ser.inWaiting()
	print rem_char
	#rem_char = 9
	value = self.ser.read(rem_char)
	value = bytearray(value)
	#print "index: ",value.find(7)
	for i,b in enumerate(value):
		if b==7 and value[i+1] == 5 and i+9<len(value):
			print "msg starts",i
			print self._Unpack_Cmd(str(value[i:i+9]))
	#print "#"+value+"#"
	#for i in value: print hex(ord(i))
	
        # everything is okay ?
        #if value[0] <> 7 and value[1] <> 5:
        #    print value
            #for i in value: print hex(ord(i))
 
        #else:
        #    return value.strip(self.ack)

    def getTM1(self):
	pass

    def getTM2(self):
	pass
    def getIVM(self):
	pass
    def setHV(self,on=True):
	pass
if __name__ == "__main__":
    p1 = Pressure_Dev()
    p1.read_in_string()
    #print p1.setHV(on=False)
    #print "Penning:", p1.getPM()
    #print "Pirani 1:", p1.getTM1()    
