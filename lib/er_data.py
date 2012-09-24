from numpy import arange,delete,append, zeros
from threading import Thread, Lock
from chaco.api import ArrayPlotData
from er_log import logger

# plot class
class PLOT_DATA (object):
    
    debug = False
    
    last_value = 0
    values_array = 0
    values_array_pd = 0
    P_plot = 0
    event_name   = "Pl_event"
    # plot related
    x_axis = ""
    y_axis = ""
    title = ""
    unit = ""
    numpoints = 200
    # window position
    x_pos = 0.1
    y_pos = 0.1
    # window size
    x_size = 300
    y_size = 300
    
    log = 0
    
    def update_value(self,value):
	pass

class PID_DATA(object):
  
    def set_func(self,value):
	pass
    def get_func(self):
	pass
    P = 0
    I = 0
    D = 0
    input_devices = [] #{} #{0:"Penning",1:"Ionivac"}
    
class SHUTTER_DATA(object):
    timeout = 3600 # 1h in seconds
    thickness = 20 # nm
    
    def open_func(self):
	pass
    def close_func(self):
	pass
    
# data share
class DATA(object):
    "data object"    
    def __init__(self):
        self.debug = False
        
        # define operational variables
	# settings for the
        # Pressure
	# list of Pressure devices
	self.P_Devs = []	
	self.PP = [0,0]
	
	#penning
        self.PP[0] = PLOT_DATA()
        self.PP[0].values_array = zeros(self.PP[0].numpoints)
	self.PP[0].y_axis       = "Pressure [mBar]"
	self.PP[0].x_axis       = "time [s]"
	self.PP[0].plot_title   = "Pressure (penning)"	
	self.PP[0].unit         = "mBar"
	self.PP[0].x_pos        = 0.0
	self.PP[0].y_pos        = 0.025
	
		    
	# register update func
	self.PP[0].update_value = self.set_Pressure
	
	# attach logger
	self.PP[0].log = logger("penning")
	
	#ionivac
        self.PP[1] = PLOT_DATA()
        self.PP[1].values_array = zeros(self.PP[0].numpoints)
	self.PP[1].y_axis       = "Pressure [mBar]"
	self.PP[1].x_axis       = "time [s]"
	self.PP[1].plot_title   = "Pressure (ionivac)"	
	self.PP[1].unit         = "mBar"
	self.PP[1].x_pos        = 0.0
	self.PP[1].y_pos        = 0.025	
	
	# define update func
 
	# register update func
	self.PP[1].update_value = self.set_Pressure_1
	
	# attach logger
        self.PP[1].log = logger("ionivac")
	
        # Pressure error
        self.PE = PLOT_DATA()
        self.PE.values_array = zeros(self.PE.numpoints)
	self.PE.x_axis       = "time [s]"
	self.PE.y_axis       = "Error [mBar]"
	self.PE.plot_title   = "Pressure Error"	
	self.PE.unit         = "mBar"
	self.PE.x_pos        = 0.0
	self.PE.y_pos        = 0.5
	
        
        # Pressure correcting output
        self.PO = PLOT_DATA()
        self.PO.values_array = zeros(self.PO.numpoints)        
	self.PO.x_axis       = "time [s]"
	self.PO.y_axis       = "Output [Volt]"
	self.PO.plot_title   = "Output / Pressure"	
	self.PO.unit         = "Volt"
	self.PO.x_pos        = 0.28
	self.PO.y_pos        = 0.025

    
        # rate 
        self.FR = PLOT_DATA()
        self.FR.values_array = zeros(self.FR.numpoints)        
	self.FR.x_axis       = "time [s]"
	self.FR.y_axis       = "Rate [nm/s]"
	self.FR.plot_title   = "Rate"	
	self.FR.unit         = "nm/s"
	self.FR.x_pos        = 0.28
	self.FR.y_pos        = 0.5
	
	# attach logger
        self.FR.log = logger("rate")	
        
        # Thickness
        self.FT = PLOT_DATA()
        self.FT.values_array = zeros(self.FT.numpoints)        
	self.FT.x_axis       = "time [s]"
	self.FT.y_axis       = "Thickness [nm]"
	self.FT.plot_title   = "Thickness"	
	self.FT.unit         = "nm"
	self.FT.x_pos        = 0.56
	self.FT.y_pos        = 0.5
	
	# attach logger
        self.FT.log = logger("thickness")	
        
        self.pid = 0
        self.r_dev = 0
        self.lock = Lock()

	# ----------------------------------------------------
	self.PID_P = PID_DATA()
	#self.P_PID.input_devices = {0:"Penning",
	#                            1:"Ionivac"}
	self.PID_P.input_devices = ["Penning",
	                            "Ionivac"]	
	# self.P_PID.set_func(self,value)
	# self.P_PID.get_func(self) # unused
	self.PID_P.P = 4.2
	self.PID_P.I = 0.076
	self.PID_P.D = 0
	

        
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


    # define update funcs
    def set_Pressure(self,m_Pressure):
	with self.lock:
	    self.PP[0].last_value = m_Pressure
	    self.PP[0].values_array = self._update_array(self.PP[0].last_value, self.PP[0].values_array)
	    if self.PP[0].values_array_pd:
		self.PP[0].values_array_pd.set_data("P_data",self.PP[0].values_array)
    
    def set_Pressure_1(self,m_Pressure):
	with self.lock:
	    self.PP[1].last_value = m_Pressure
	    self.PP[1].values_array = self._update_array(self.PP[1].last_value, self.PP[1].values_array)
	    if self.PP[1].values_array_pd:
		self.PP[1].values_array_pd.set_data("P_data",self.PP[1].values_array)


    def set_P_error(self,P_error):
        #print "P_error"
        with self.lock:
            #self.P_error = P_error
            self.PE.last_value = P_error
            self.PE.values_array = self._update_array(self.PE.last_value, self.PE.values_array)
            if self.PE.values_array_pd:
                self.PE.values_array_pd.set_data("P_data",self.PE.values_array)            

    def set_P_output(self,P_output):
        #print "P_output"
        with self.lock:
            #self.P_error = P_error
            self.PO.last_value = P_output
            self.PO.values_array = self._update_array(self.PO.last_value, self.PO.values_array)
            if self.PO.values_array_pd:
                self.PO.values_array_pd.set_data("P_data",self.PO.values_array)

    def set_F_rate(self,F_rate):
        with self.lock:
            self.FR.last_value = F_rate
            self.FR.values_array = self._update_array(self.FR.last_value, self.FR.values_array)
            if self.FR.values_array_pd:
                self.FR.values_array_pd.set_data("P_data",self.FR.values_array)
		
    def set_F_thickness(self,F_thickness):
        with self.lock:
            self.FT.last_value = F_thickness
            self.FT.values_array = self._update_array(self.FT.last_value, self.FT.values_array)
            if self.FT.values_array_pd:
                self.FT.values_array_pd.set_data("P_data",self.FT.values_array)
            
    def _update_array(self, m_value, data_array):
        #print "_generate array called"
        data_array = delete(
            append(data_array,m_value),0)
        return data_array

