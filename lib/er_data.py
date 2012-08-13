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

        # Placeholders for the plot settings and data, pid object
        # Pressure 
        self.P_plot = 0
        self.P_pid = 0
        # Pressure error
        self.PE_plot = 0
        # Pressure correcting output
        self.PO_plot = 0
        
        self.pid = 0
        self.r_dev = 0
        #self.pressure_array = zeros(1000)
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
            self.P_plot._gen_array(m_Pressure)
    def set_P_error(self,P_error):
        #print "P_error"
        with self.lock:
            self.P_error = P_error
            self.PE_plot._gen_array(P_error)
    def set_P_output(self,P_output):
        #print "P_output"
        with self.lock:
            self.P_output = P_output
            self.PO_plot._gen_array(P_output)    
"""
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
"""