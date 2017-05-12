# filename: er_combivac.py
# version 0.1 written by HR@KIT 2012
# updates: 05/2017 (JB)
# driver file for Combivac pressure meter used at AlOx sputter tool

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import time,sys
import atexit

class Pressure_Dev(object): 
    # in the moment only access to a combivac cm 31
    def __init__(self,device="/dev/ttyUSB5"):

        self.ack="\x06"
        self.nak="\x15"
        baudrate = 2400
        timeout = 0.1
        
        # Port A on the USB_to_serial converter,Port A with C, Port B ends with K
        #device = "/dev/tty.usbserial-FTB4J8SK" 
        #device = "/dev/ttyUSB5"
        self.ser = self._std_open(device,baudrate,timeout)
        atexit.register(self.ser.close)
            
        # load inficon comands
        
        
    def _std_open(self,device,baudrate,timeout):
        import serial
        # open serial port, 9600, 8,N,1, timeout 0.1
        #device="/dev/tty.usbserial"
        return serial.Serial(device, baudrate, timeout=timeout)
        
    def remote_cmd(self,cmd):
        cmd+="\r"

        # clear queue first, old data,etc
        rem_char = self.ser.inWaiting()
        if rem_char:
            self.ser.read(rem_char)
        
        # send command
        self.ser.write(cmd)
        # wait until data is processed
        time.sleep(0.5)
        # read back
        rem_char = self.ser.inWaiting()
        value = self.ser.read(rem_char)
        
        # for i in value: print hex(ord(i))
        # everything is okay ?
        if value[0] <> self.ack:
            print value
            #for i in value: print hex(ord(i))
            if value[0] == self.nak:
                print "er_combivac: NAK occured"
            print "er_combivac: Error in writing/reading"
            return None
        else:
            return value.strip(self.ack)
    
    def getTM1(self):
        value = self.remote_cmd("MES R TM1")
        # "TM1:MBAR  : 1.00E+03"
        try:
                gauge,pressure = value.split(" : ")
                return float(pressure.strip())
        except Exception as m:
            print m
            return 0

    def getTM2(self):
        value = self.remote_cmd("MES R TM2")
        # "TM1:MBAR  : 1.00E+03"
        try:
                gauge,pressure = value.split(" : ")
                return float(pressure.strip())
        except Exception as m:
            print m
            return 0
            
    def getUHV(self):
        value = self.remote_cmd("MES R PM1")
        try:
                gauge,pressure = value.split(" : ")
                return float(pressure.strip())
        except Exception as m:
            print m
            return 0
            
    def setHV(self,on=True):
        if on:
            return self.remote_cmd("HVs w pm1,On")
        else:
            return self.remote_cmd("HVs w pm1,OFF")
            
if __name__ == "__main__":
    p1 = Pressure_Dev()
    #print p1.setHV(on=False)
    print "Penning:", p1.getUHV()
    print "Pirani 1:", p1.getTM1()    
