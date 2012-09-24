#/usr/bin/env python
# logging module for evaporate

import sys, os, time, errno

class logger(object):
    def __init__(self,logname):
        self.stat =  0
        self.logname = logname
        self.logpath = self.createLogDir()
        self.openFile()
        
    def get_today(self):
        return time.strftime("%Y%m%d")
    def get_now(self):
        return str(int(time.time()*10)/10.)
    
    def createLogDir(self):
        logpath = "logs"+'//'+self.get_today()
        try:
            os.mkdir(logpath)
            return logpath
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
            return logpath
        
    def openFile(self):
        self.logfile = open(self.logpath+'//'+self.logname + '.dat','a')
        
    def closeFile(self):
        if self.logfile:
            self.logfile.close()
    
    def log(self, value):
        if self.logfile:
            self.logfile.write("%s %s %d\n" %(self.get_now(),str(value),self.stat))
            self.logfile.flush()
    def start(self):
        self.stat = 1
    def stop(self):
        self.stat = 0
    """
    def __call__(self,value):
        self.log(value)
    """ 
if __name__ == "__main__":
    os.chdir("..")
    log = logger("penning")
    #log.createLogDir()
    for i in range(12):
        log.log(i*12.3)
        if i%2:
            log.start()
        if not i%2:
            log.stop()
    log.closeFile()
