from threading import Thread, Lock
from time import sleep, time, localtime, strftime

class PressureThread(Thread):
    
    def check_valid_pressure(self,m_Pressure,m_Pressure_tmp,plo):
	# -------------------------
	# this section is a hack to go around the penning reading problems.
	if m_Pressure >1.5*m_Pressure_tmp and m_Pressure_tmp:
	    m_Pressure = m_Pressure_tmp
	    plo.dev_bad_reading = True
	    return m_Pressure, m_Pressure_tmp
	    # bad_reading_count +=1
	    # if bad_reading_count == 5:
	    #  print "bad reading count reached (5), resetting last value:"
	    #  m_Pressure_tmp = m_Pressure
        else:
            return m_Pressure, m_Pressure_tmp
	# -------------------------
    def run(self):
	continue_loop =  False
	m_Pressure = [0.,0.]
        #m_Pressure = 0
	
	#m_Pressure_tmp = 0
	m_Pressure_tmp = [0.,0.]
	bad_reading_count = 0
        #SetPressure = self.ER.SetPressure
        # this is also kindof a hack
        plot_devs = [self.ER.pressure_plot, 
                     self.ER.P_IV_plot] 
        while self.ER.P_Acquire_state:
            sleep(.5)
	    
	    m_Pressure_tmp[0] = m_Pressure[0]
	    m_Pressure_tmp[1] = m_Pressure[1]
	    #self.ER.pressure_plot.dev_bad_reading = False
	    #self.ER.P_IV_plot.dev_bad_reading = False
	    
	    "get Pressure from gauges"
	    # save the data to the data
	    for i in range(2): # penning , ionivac
		try:
                    plot_devs[i].dev_bad_reading = False
		    m_Pressure[i] = self.ER.data.P_Devs[i].getUHV()
		    if m_Pressure[i]:
			#pass
			m_Pressure[i],m_Pressure_tmp[i] = self.check_valid_pressure(m_Pressure[i],m_Pressure_tmp[i],plot_devs[i])
		    else:
			print "Pressure: (None) Bad return from device", i
			m_Pressure[i] = m_Pressure_tmp[i]
			continue_loop =  True
			
		except TypeError as e:
		    print "Pressure: (TypeError) Bad return from device"
		    print e,i
		    self.ER.pressure_plot.dev_bad_reading = True
		    # the next reading should have a valid before
		    m_Pressure = m_Pressure_tmp
		    continue
		except:
		    print "Pressure: no Pressure measurement taken"
		    raise		
	    # penning
	    self.ER.pressure_plot.dev_reading = m_Pressure[0]
	    self.ER.data.PP[0].update_value(m_Pressure[0])
	    self.ER.data.PP[0].log.log(m_Pressure[0])
	    # ionivac
	    self.ER.P_IV_plot.dev_reading = m_Pressure[1]
	    self.ER.data.PP[1].update_value(m_Pressure[1])
	    self.ER.data.PP[1].log.log(m_Pressure[1])
	    
	    bad_reading_count = 0		

	    if continue_loop:
		continue_loop = False
		continue

    
                
	    if self.ER.pressure_pid.Regulate_state:
		#print "Thread enters regulation ..."
		# calculate new output value
		o_new_val, error = self.ER.data.P_pid.get_correcting_value(m_Pressure[0])
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
		self.ER.data.set_F_thickness(m_Thickness)
		self.ER.data.FT.log.log(m_Thickness)
		
		m_Rate = self.ER.data.R_Dev.getRate(nm=True)
		self.ER.F_rate_plot.dev_reading = m_Rate
		self.ER.data.set_F_rate(m_Rate)
		self.ER.data.FR.log.log(m_Rate)
	    except:
		print "no Film measurement taken"
		raise    
                
    print "Exit Film monitor thread"


class StopThread(Thread):
    
    def run(self):
	# change the log status
	# note that the logger is saving data in any case
        self.ER.data.PP[0].log.start()
        self.ER.data.PP[1].log.start()
        self.ER.data.FR.log.start()
        self.ER.data.FT.log.start()

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
	# stop the log status 
	self.ER.data.PP[0].log.stop()
        self.ER.data.PP[1].log.stop()
	self.ER.data.FR.log.stop()
	self.ER.data.FT.log.stop()

    print "Exit Start/Stop time thread"
    
class Resistance(object):
    
    def __init__(self):
        pass
    def get_save_resistance(self):
        #switch off sputter power supply
        self.ER.data.SP_Dev.setStatus(False)
        self.ER.data.Res_Dev.getR()
        self.ER.data.SP_Dev.setStatus(False)
        print("gsr")

    
    
