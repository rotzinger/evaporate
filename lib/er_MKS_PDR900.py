# filename: er_MKS_PDR900.py
# Jochen Braumueller <jochen.braumueller@kit.edu>, 2013
# updates: 05/2017
# driver file for MKS PDR900 pressure meter used at Plasma1 and AlOx sputter tools

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
    def __init__(self,device_sel = "pl1_MC"):
        '''
        instantiate passing a parameter device_sel, which is one of
        pl1_LL, pl1_MC, AlOx_LL or directly a valid serial device
        '''

        self.ack="ACK"
        self.nak="NAK"
        baudrate = 9600
        timeout = 0.1
        
        if device_sel == "pl1_LL":
            device = "/dev/ttyUSB2"
        elif device_sel == "pl1_MC":
            device = "/dev/ttyUSB1"
        elif device_sel == "AlOx_LL":
            device = "/dev/ttyUSB4"
        else:
            if '/dev/ttyUSB' in device_sel:
                device = device_sel
            else:
                print "Error loading MKS PDR900 instrument: Device not recognized."
                raise ValueError
       
        self.ser = self._std_open(device,baudrate,timeout)
        atexit.register(self.ser.close)
        
    def _std_open(self,device,baudrate,timeout):
        import serial
        # open serial port, 9600, 8,N,1, timeout 0.1
        return serial.Serial(device, baudrate, timeout=timeout)
        
    def remote_cmd(self,cmd):
        cmd+="\n"

        # clear queue first, old data,etc
        rem_char = self.ser.inWaiting()
        if rem_char:
            self.ser.read(rem_char)
        
        # send command
        self.ser.write(cmd)
        # wait until data is processed
        time.sleep(0.2)
        # read back
        rem_char = self.ser.inWaiting()
        value = self.ser.read(rem_char)
        return value
        
    #due to compatibility...
    def getTM1(self):
        return self.getPressure(self.getAddressT())
    def getTM2(self):
        return self.getPressure(self.getAddressT())
    def getUHV(self):
        return self.getPressure(self.getAddressT())
                
    #controller methods
    def getSerial(self):
        return self.remote_cmd("@001SNC?;FF")[7:-3]
    def getAddress(self):
        return self.remote_cmd("@254ADC?;FF")
        
    #transducer methods
    def getBaudT(self):
        return self.remote_cmd("@xxxBR?;FF")[7:-3]
    def getAddressT(self):
        return self.remote_cmd("@xxxAD?;FF")[7:10]
    def getPressure(self,address=None):
        try:
            if not address:
                address = self.getAddressT()
            return self.remote_cmd("@" + address + "PR3?;FF")[7:14]
        except Exception as m:
            print m
            return 0
        
    def setAddressT(self,address = "002"):
        return self.remote_cmd("@xxxAD!" + address + ";FF")
        
                
if __name__ == "__main__":
    pMC = Pressure_Dev("pl1_MC")
    print "Baudrate Transducer MC: ", pMC.getBaudT()
    addrMC = str(pMC.getAddressT())    #transducer address
    print "Pressure MC: ", pMC.getPressure(addrMC)
    
    pLL = Pressure_Dev("pl1_LL")
    print "Baudrate Transducer LL: ", pLL.getBaudT()
    addrLL = str(pLL.getAddressT())    #transducer address
    print "Pressure LL: ", pLL.getPressure(addrLL)
