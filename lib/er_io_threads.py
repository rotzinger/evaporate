from threading import Thread, Lock
from time import sleep

class PressureThread(Thread):
    "Remote operations"
    def run(self):
        m_Pressure = 0
        SetPressure = self.ER.SetPressure
        
        while self.ER.P_Acquire_state:
            sleep(.5)
	    try:
		"get Pressure from gauge"
		m_Pressure_tmp = self.ER.data.P_Dev.getPM()
		# save the data to the data
		if m_Pressure_tmp:
		    m_Pressure = m_Pressure_tmp	
		    self.ER.Pressure = m_Pressure_tmp
		    self.ER.data.set_Pressure(m_Pressure)
		    #f = open('log_pressure.dat','a')
		    #f.write(str(m_Pressure))
	  	    #f.write('\n')
		    
		# for now we get Rate and Thickness also in this thread
		#self.ER.Rate = self.ER.data.R_Dev.getRate(nm=True)
		#self.ER.Thickness = self.ER.data.R_Dev.getThickness(nm=True)
		    
	    except:
		print "no Pressure measurement taken"
		raise    
                
	    if self.ER.P_Regulate_state:
		print "Thread enters regulation ..."
		# calculate new output value
		o_new_val, error = self.ER.data.P_pid.get_correcting_value(m_Pressure)
		# scale to reasonable voltages
		o_new_val= o_new_val*1e6
		    
		print 'V output value, error', o_new_val, error
		if o_new_val>1: o_new_val = 1 
		if o_new_val<0.0001: o_new_val = 0.05
		# the DAQ generates a voltage, the MFC generates a mass flow from this.
		self.ER.data.DAQ_Dev.output(0,o_new_val)
		# save the error and output
		self.ER.data.set_P_error(error)
		self.ER.data.set_P_output(o_new_val)
		print o_new_val, error
		
    print "Exit pressure monitor thread"
    

class FilmThread(Thread):
    "Remote operations"
    def run(self):
        m_Rate = 0
	m_Thickness = 0
	# for now we get Rate and Thickness also in this thread
	#self.ER.Rate = self.ER.data.R_Dev.getRate(nm=True)
	#self.ER.Thickness = self.ER.data.R_Dev.getThickness(nm=True)
        
        while self.ER.F_Acquire_state:
            sleep(.5)
	    try:
		# for now we get Rate and Thickness also in this thread
		self.ER.F_R = self.ER.data.R_Dev.getRate(nm=True)
		self.ER.F_T = self.ER.data.R_Dev.getThickness(nm=True)
		    
	    except:
		print "no Film measurement taken"
		raise    
                
    print "Exit Film monitor thread"