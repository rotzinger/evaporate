# Frequency counter DEV version 0.1 written by HR@KIT 2014
# 
import time,sys
import atexit
try:
    import Gpib
except:
    print "GPIB not found, starting dummy ..."
    class Gpib(object):
         pass


class Frequency_Counter_Dev(object): 

    def __init__(self):


        GPIB_ID = 2
        GPIB_ID = "HP_FC"	
        self.FC = self._std_open(GPIB_ID)

        #atexit.register(self.FC.ce)
            
        self.StartFrequency=0
        self.thickness_per_f=20./400.

        self.lasttime=0
        self.lastthickness=0
       
    def setThickness_per_F(self,th_p_f):
        self.thickness_per_f = th_p_f

    def setStartFrequency(self,sf=None):
        if not sf:
            self.StartFrequency = self.getFrequency()
        else:
            self.StartFrequency  = sf
    
    def _std_open(self,GPIB_ID):
        FC = Gpib.Gpib(GPIB_ID)
        return FC

    def remote_cmd(self,cmd):
        #cmd+="\n"

        # send command
        self.FC.write(cmd)
        # wait until data is processed
        time.sleep(0.1)
        # read back
        #value = self.FC.read()
        
        #return value.strip()
    def remote_ask(self,cmd):
       #cmd+="\n"
       # send command
       self.FC.write(cmd)
       # wait until data is processed
       time.sleep(0.1)
       # read back
       message = ""
       CR = False
       for i in range (500):
           value = self.FC.read(1)
           if value == "\r":
                CR=True
           if CR and value == "\n":
                break
           message+=value
       return message.strip()

    def remote_read(self):
       message = "" 
       CR = False
       for i in range (100):
       	   value = self.FC.read(1)
           if value == "\r":
		CR=True
	   if CR and value == "\n":
                break
           message+=value
       return message.strip()

    def _setup_device(self):
        self.remote_cmd("RESET")
        self.remote_cmd("CLR")
        self.remote_cmd("INIT")
        
	self.remote_cmd("HIGHZ")
        self.remote_cmd("RESOL,0")
        self.remote_cmd("HIRESOL,ON")

    def getMe(self):
        print self.remote_ask("ID?")

    def getSetup(self):
	print self.remote_ask("SET?")

    def getFrequency(self):
        return float(self.remote_read())
    def getRate(self,nm=True):
        # we have to calculate the rate ourselves
        if not self.lasttime:
          self.lasttime =  time.time()
          return 0
        if not self.lastthickness:
          self.lastthickness = self.getThickness(nm=True)
          return 0
        delta_thickness = self.getThickness(nm=True)-self.lastthickness
        return delta_thickness/(time.time()-self.lasttime)

    def getThickness(self,nm=True):
        return (self.getFrequency()-self.StartFrequency)*self.thickness_per_f
        

    # print 'Rate:',data.R_Dev.getRate(nm=True)
    # print 'Thickness:',data.R_Dev.getThickness(nm=True)

if __name__ == "__main__":
    p1 = Frequency_Counter_Dev()
    #p1._setup_device()
    p1.getMe()
    #p1.getSetup()
    print "Thickness:",p1.getThickness(nm=True)
    for i in range(10):
       print "Frequency:",p1.getFrequency()
       print "Rate:",p1.getRate(nm=True)
