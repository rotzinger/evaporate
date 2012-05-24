#!/usr/bin/env python
# ftdi_dac written by HR@KIT in March 2011
# this file is a driver for a single AD5422 16bit Digital to analog converters
# connected to a FTDI FT4232H device.
# Only port A is used in the moment

import time
import struct
from pyftdi.pyftdi.spi import SpiController


class SPI_Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
#(my) spi interface ;-)
class SPI_INTERFACE(object):
    def __init__(self,vendor, product, interface=1):
        self._ctrl = SpiController()
        self._ctrl.configure(vendor, product, interface)
    def set_port(self,cs=0):
        self.spi_port = self._ctrl.get_port(cs)
        
    def set_spi_frequency(self,frequency):
        self.spi_port.set_frequency(frequency)

    def spi(self,data,readlen=0):
        #bytes = self.pack_data(data)
        return self.spi_port.exchange(out=data,readlen=readlen)

    # these two functions are obsolete now
    def pack_data(self, data):
        fmt =  '<'
        for b in data: fmt+="B"
        return struct.pack(fmt,*data)
    
    def unpack_data(self,data):
        fmt='<'
        for i in range(len(data)): fmt+='B'
        
        return list(struct.unpack(fmt,data))


class AD5422(SPI_INTERFACE):
    """ Analog Devices 16bit DAC with SPI interface """
    # AD5422 command register addresses
    CMD_NOP      = 0b00000000
    CMD_DATA     = 0b00000001
    CMD_READBACK = 0b00000010
    CMD_CONTROL  = 0b01010101
    CMD_RESET    = 0b01010110

    def __init__(self,vendor, product, interface=1):
        super(AD5422,self).__init__(vendor, product, interface=1)
        self.set_port(0)
        self.set_spi_frequency(6e6)
        

    def config_DAC(self,on=True, VRange = 5):
        """ Configure very basic settings """

        """         COR OUT SRC  SRS SREN  DASY RANGE
        default = 0b000  1  0000 000  0    0    000 
        default = 0b00010000 (on, single)
        """
        if on:
            onoff = 0x00 | 0x10 
        else:
            onoff = 0x00
        """ unipolar 5 or 10 Volt max output"""
        if VRange == 5:
            lsb = 0x00
        elif VRange == 10:
            lsb = 0x01
        else:
            lsb = 0x00
            
        SPIBytes = [AD5422.CMD_CONTROL,onoff,lsb]
        self.spi(SPIBytes)

    def reset_DAC(self):
        """ reset the dac """
	SPIBytes = [AD5422.CMD_RESET, 0x00, 0x01]
        self.spi(SPIBytes)
        
    def IO(self,data,**kwargs):
        """ This function writes to the AD5422 DAC
            (read does not work yet)
        arguments:
           data: a integer number between 0 and 65535 (16 bit)
        optional
           cmd = DATA_CMD: set the cmd register
           readlen = 0: read readlen bytes back (not functional)
        """
        
        """ The AD5422 expects 16bit data, convert to int, set defaults """
        data = int(data)
        if data <0:
            data = 0
        elif data > 0xffff: # > 16bit 
            data = 0xffff
            
        cmd = kwargs.get("cmd",AD5422.CMD_DATA)
        readlen = kwargs.get("readlen",0)
        
        lsb =  data     & 0xff
        msb = (data>>8) & 0xff
        SPIBytes = [cmd, msb, lsb]
        return list(self.spi(SPIBytes,readlen=readlen))

    def get_state(self):
        """ FIXME: this does not work yet """
        data = 0b00
        print self.IO(data,cmd=AD5422.CMD_READBACK)
        #print self.IO(data,cmd=0,readlen=3)
        return self.IO(0,cmd=AD5422.CMD_NOP,readlen=3)

if __name__ == "__main__":
    """ init ftdi chip with USB(vendor,product,interface), port """
    DAC = AD5422(0x403, 0x8011, 1)
    DAC.reset_DAC()
    DAC.config_DAC(on=True,VRange=5)

    time.sleep(0.1)
    DAC.IO(100)
    time.sleep(0.2)
    
    for code in xrange (0,0xffff,1000):
        print code
        DAC.IO(code)
        time.sleep(0.5)
    
    print DAC.get_state()
    #DAC.reset_DAC()
