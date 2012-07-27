from numpy import arange,delete,append, zeros
from threading import Thread, Lock
# data share
class DATA(object):
    "data object"
    def __init__(self):
        # define operational variables
        self.m_thickness = 0
        self.m_rate    = 0
        self.m_time    = 0
        self.m_error   = 0
        self.o_new_val = 0
        # not used anymore
        #self.pid_P = 0
        #self.pid_I = 0
        #self.pid_D = 0

        self.pid = 0
        self.r_dev = 0
        self.pressure_array = zeros(1000)
        self.lock = Lock()
        
    def get_thickness(self):
        return self.m_thickness
    def set_thickness(self,tn):
        with self.lock:
            self.m_thickness = tn
        
    def get_rate(self):
        return self.m_rate
    def set_rate(self,rt):
        with self.lock:
            self.m_rate = rt

    def set_Pressure(self,m_Pressure):
        with self.lock:
            self.m_pressure = m_Pressure
            self.pressure_array= delete(
                append(self.pressure_array,m_Pressure),0)
            
    # not sure if this is really needed
    def set_pid_p(self,P):
        with self.lock:
            self.pid.set_P(P)
    def set_pid_i(self,I):
        with self.lock:
            self.pid.set_I(I)
    def set_pid_d(self,D):
        with self.lock:
            self.pid.set_D(D)
