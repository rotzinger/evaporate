# RATE DEV version 0.1 written by HR@KIT 2012
# updates 05/2017 (JB)

import time,sys
import atexit

class Rate_Dev(object):
    class inficon_cmds(object):
        ack="\x06"
        #ack=" \x06"
        get_hello="H"+ack
        get_rate="S 1"+ack
        get_thickness="S 2"+ack
        get_time="S 3"+ack
        get_film="S 4"+ack
        get_xtal_live="S 5"+ack
        set_thickness_zero = "R 4"+ack
        set_timer_zero = "R 5"+ack
        
    def __init__(self,device="/dev/ttyUSB6"):
        # open serial port, 9600, 8,N,1, timeout 1s
        #device="/dev/tty.usbserial"
        baudrate = 9600
        timeout = 0.1
        self.ack = "\x06"

        # Port A on the USB_to_serial converter, Port B ends with K
        #device = "/dev/tty.usbserial-FTB4J8SC"
        #device = "/dev/ttyUSB0" 
        self.ser = self._std_open(device,baudrate,timeout)
        atexit.register(self.ser.close)
        '''
        """ does not work !!!"""
        # the pyftdi emulation
        #device="/dev/tty.usbserial"
        device = 'ftdi:///0'
        self.ser = self._pyftdi_open(device,baudrate,timeout)
        '''
        
        # load inficon comands
        self.cmds = self.inficon_cmds()
        
    def _std_open(self,device,baudrate,timeout):
        import serial
        return serial.Serial(device, baudrate, timeout=timeout)
        
    def _pyftdi_open(self,device, baudrate,timeout):
        """Open the serial communication port in the pyserial emulation"""
        # function taken from pyftdi sources
        from pyftdi.serialext import SerialExpander
        serialclass = SerialExpander.serialclass(device)
        import serial
        try:
            port = serialclass(port=device,
                               baudrate=baudrate,
                               timeout=timeout)
            if not port.isOpen():
                port.open()
            if not port.isOpen():
                raise AssertionError('Cannot open port "%s"' % device)
            port.setRTS(1)
            port.setDTR(1)
            port.timeout = timeout
            return port
        except serial.serialutil.SerialException, e:
            raise AssertionError(str(e))
        
    def remote_cmd(self,cmd):
        self.ser.write(cmd)
        
        time.sleep(0.1)
        #value = self.ser.readline().strip("\x06")
        rem_char = self.ser.inWaiting()
        
        value = self.ser.read(rem_char).strip(self.ack)
        #print "##"+value+"##"+value.strip()+"###"
        return value #value.strip()
    
    def getHello(self):
        return self.remote_cmd(self.cmds.get_hello)
    def getRate(self, nm=False):
        rate = float(self.remote_cmd(self.cmds.get_rate))
        if nm:
            #return rate in nm
            return rate/10.
        else:
            # return rate in A (10^-10m)
            return rate

    def getThickness(self, nm=False):
        thickness = float(self.remote_cmd(self.cmds.get_thickness))
        if nm:
            # return thickness in nm
            return thickness*100.
        else:
            # return thickness in kA (10^-7m)
            return thickness
        
if __name__ == "__main__":
    rd=Rate_Dev()
    #print rd.getHello()
    print 'Rate:',rd.getRate()
    print 'Thickness:',rd.getThickness()
