try:
    from enthought.enable.api import Window, Component, ComponentEditor
    from enthought.traits.api import HasTraits, Instance ,Float, Button,false
    from enthought.traits.ui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow
    # Chaco imports
    from enthought.chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer
except:
    from enable.api import Window, Component, ComponentEditor
    from traits.api import HasTraits, Instance ,Float, Button,false
    from traitsui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow
    # Chaco imports
    from chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer

from time import sleep
from threading import Thread, Lock
import lib.er_pidcontrol as er_pid



class ER_State(HasTraits):
    SetPressure = Float(0,desc="set D parameter",auto_set=False, enter_set=True)
    Pressure = Float()
    Rate = Float(0)
    Thickness = Float(0)
    Regulate = Button()
    Acquire = Button()
    P = Float(0.1,desc="set P parameter",auto_set=False, enter_set=True)
    I = Float(0.01,desc="set I parameter",auto_set=False, enter_set=True)
    D = Float(0.00,desc="set D parameter",auto_set=False, enter_set=True)
    inout_thread = ""
    P_acquire = False
    view = View(
        Group(
            VGroup(
                Item(name='Acquire'),
                Item(name='Pressure',style="readonly"),
                show_border=True,
                ),
            VGroup(
                Item(name='Thickness',style="readonly"),
                Item(name='Rate',style="readonly"),
                show_border=True,
                ),

            VGroup(
                Item(name='SetPressure'),
                show_border=True,
                ),
            VGroup(
                Item(name='P'),
                Item(name='I'),
                Item(name='D'),
                Item(name='Regulate'),show_border=True,
                )
            )
        )
    
    # some important actions
    def _Acquire_fired(self):
        if not self.P_acquire: 
            self.Continuous = True
            self.P_acquire = True
            self.P_regulate = False
            aq = self.inout_data()
            print "Aquire fired, thread started"            
        else:
            self.Continuous = False
            self.P_acquire = False
            self.P_regulate = False
            print "Aquire fired, thread stopped"

    def _SetPressure_default(self):
        self.data.press_pid = er_pid.pidcontrol()            
        return 1e-7 
    def _Regulate_fired(self):
        if self.P_acquire and not self.P_regulate:
            print "Regulate pressure started"
            self.P_regulate = True
            #self.data.press_pid = er_pid.pidcontrol()
            self.data.press_pid.set_P(self.P)
            self.data.press_pid.set_I(self.I)
            self.data.press_pid.set_D(self.D)
            self.data.press_pid.set_ctrl_value(self.SetPressure)
        else:
            print "Regulate pressure fired off"
            self.P_regulate = False
            
    def _P_changed(self):
        self.data.press_pid.set_P(self.P)
    def _I_changed(self):
        self.data.press_pid.set_I(self.I)
    def _D_changed(self):
        self.data.press_pid.set_D(self.D)
    def _SetPressure_changed(self):
        self.data.press_pid.set_ctrl_value(self.SetPressure)
        
    # check thread
    def inout_data(self):
        if self.inout_thread and self.inout_thread.isAlive():
            self.inout_thread.Continuous = False
            #self.ER.Continuous = False
        else:
            self.inout_thread = InOutThread()
            self.inout_thread.Continuous = self.Continuous
            self.inout_thread.ER = self
            self.inout_thread.start()


class InOutThread(Thread):
    "Remote operations"
    def run(self):
        m_Pressure = 0
        SetPressure = self.ER.SetPressure
        
        while self.ER.P_acquire:
            sleep(.5)
            if self.ER.P_acquire:
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
		    self.ER.Rate = self.ER.data.R_Dev.getRate(nm=True)
		    self.ER.Thickness = self.ER.data.R_Dev.getThickness(nm=True)
		    
                except:
                    print "no Pressure measurement taken"
                    raise    
                
                if self.ER.P_regulate:
                    # calculate new output value
                    o_new_val, error = self.ER.data.press_pid.get_correcting_value(m_Pressure)
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
                    #data.set_pidE(error)
        #f.close()
        print "Exit pressure monitor thread"
