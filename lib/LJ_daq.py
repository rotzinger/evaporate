#!/usr/bin/env python
# LJ_daq written by HR@KIT March 2011
# this file is a driver for two dasy-chained AD5422 16bit Digital to analog converters
# connected to a LabJack u3 device.

import u3
import time

class LJ_DAQ(object):
    def __init__(self):
        
        self.LJ_device = u3.U3()
        #LJ Pin settings (E0-E3)
        self.MISOPinNum = 8
        self.CLKPinNum  = 9
        self.MOSIPinNum = 10
        self.CSPINNum   = 11

        # AD5422 register addresses addresses
	self.nop      = 0b00000000
        self.data     = 0b00000001
	self.readback = 0b00000010
	self.control  = 0b01010000 #0b01010101
	self.reset    = 0b01010110

    def spi(self,SPIBytes):
        return self.LJ_device.spi(SPIBytes,
                    AutoCS=True,
                    DisableDirConfig = False,
                    SPIMode = 'A',
                    SPIClockFactor = 0,
                    CSPINNum   = self.CSPINNum, 
                    CLKPinNum  = self.CLKPinNum,
                    MISOPinNum = self.MISOPinNum,
                    MOSIPinNum = self.MOSIPinNum)

    def config_DAQ1(self,on=True):
        """         COR OUT SRC  SRS SREN  DASY RANGE
        default = 0b000  1  0000 000  0    1    000 """
        default1 = 0b00010000
        if on:
            onoff = 0b00010000
        else:
            onoff = 0b00000000
        
        default2 = 0b00001000
        SPIBytes = [self.control,onoff,default2]
        self.spi(SPIBytes)

    def config_DAQ2(self):
        """         COR OUT SRC  SRS SREN  DASY RANGE
        default = 0b000  1  0000 000  0    1    000 """
        default1 = 0b00010000
        default2 = 0b00001000
        SPIBytes = [0x00,0x00,0x00,self.control,default1,default2]
        self.spi(SPIBytes)

    def reset_DAQ(self):
        # A list of bytes to write using SPI
	SPIBytes = [self.reset, 0x00, 0x00, self.reset, 0x00, 0x00]
        self.spi(SPIBytes)
        
    def data_to_DAQ1(self,data):
        if data <0:
            data = 0
        elif data > 65535:
            data = 65535
        
        "first daq2 then daq1"
        lsb=data & 0xff
        msb=(data>>8) & 0xff
        SPIBytes = [self.nop, 0x00, 0x00, self.data, msb, lsb]
        self.spi(SPIBytes)



if __name__ == "__main__":
    LJ = LJ_DAQ()
    #LJ.reset_DAQ()
    LJ.config_DAQ1(on=True)
    LJ.data_to_DAQ1(0)
    
    for i in xrange (0,65536,100):
        print i
        LJ.data_to_DAQ1(i)
        time.sleep(0.001)
    
