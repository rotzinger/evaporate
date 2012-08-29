from threading import Thread, Lock
from time import sleep, time, localtime, strftime

class PressureThread(Thread):
    "Remote operations"
    def run(self):
        m_Pressure = 0
	m_Pressure_tmp = 0
        #SetPressure = self.ER.SetPressure
        
        while self.ER.P_Acquire_state:
            sleep(.5)
	    try:
		m_Pressure_tmp = m_Pressure
		self.ER.pressure_plot.dev_bad_reading = False
		"get Pressure from gauge"
		m_Pressure = self.ER.data.P_Dev.getPM()
		# save the data to the data
		if m_Pressure:
		    if m_Pressure >1.5*m_Pressure_tmp and m_Pressure_tmp:
			m_Pressure = m_Pressure_tmp
			self.ER.pressure_plot.dev_bad_reading = True
		    self.ER.pressure_plot.dev_reading = m_Pressure
		    self.ER.data.set_Pressure(m_Pressure)
	    except TypeError:
		print "Pressure: (TypeError) Bad return from device"
		self.ER.pressure_plot.dev_bad_reading = True
		# the next reading should have a valid before
		m_Pressure = m_Pressure_tmp
		continue
	    except:
		print "Pressure: no Pressure measurement taken"
		raise    
                
	    if self.ER.pressure_pid.Regulate_state:
		#print "Thread enters regulation ..."
		# calculate new output value
		o_new_val, error = self.ER.data.P_pid.get_correcting_value(m_Pressure)
		self.ER.P_error_plot.dev_reading = error
		# scale to reasonable voltages
		o_new_val= o_new_val*1e3
		self.ER.P_output_plot.dev_reading = o_new_val
		print 'V output value:', o_new_val, 'error:', error ,'unscaled output:', o_new_val/1e3 
		if o_new_val>1: o_new_val = 1 
		if o_new_val<0.0001: o_new_val = 0.05
		# the DAQ generates a voltage, the MFC generates a mass flow from this.
		self.ER.data.DAQ_Dev.output(0,o_new_val)
		# save the error and output
		self.ER.data.set_P_error(error)
		self.ER.data.set_P_output(o_new_val)
		#print o_new_val, error
		
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
		#self.ER.F_R = self.ER.data.R_Dev.getRate(nm=True)
		#self.ER.F_T = self.ER.data.R_Dev.getThickness(nm=True)
		m_Thickness = self.ER.data.R_Dev.getThickness(nm=True)
		self.ER.F_thickness_plot.dev_reading = m_Thickness
		self.ER.data.set_F_thickness(m_Rate)
		m_Rate = self.ER.data.R_Dev.getRate(nm=True)
		self.ER.F_rate_plot.dev_reading = m_Rate
		self.ER.data.set_F_rate(m_Rate)
	    except:
		print "no Film measurement taken"
		raise    
                
    print "Exit Film monitor thread"


class StopThread(Thread):
    
    def run(self):
        t  = time()
	dt = self.ER.stop_dtime
	t= t-dt
	ts = ""
        while self.ER.stop_state:
	    dt = time()-t
	    ts = strftime("%Mm %Ss",localtime(dt))
	    self.ER.stop_time = ts
	    sleep(1)
	self.ER.stop_dtime = dt
    print "Exit Start/Stop time thread"