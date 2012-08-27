#try:
    #from enthought.enable.api import Window, Component, ComponentEditor
    #from enthought.traits.api import HasTraits, Instance ,Float, Bool, Button,Event,Str,false
    #from enthought.traits.ui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow,ButtonEditor,Handler
    ## Chaco imports
    #from enthought.chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer
#except:
if 1:
    from enable.api import Window, Component, ComponentEditor
    from traits.api import HasTraits, Instance ,Float,Bool, Button,Event,Str,false
    from traitsui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow, ButtonEditor,Handler
    # Chaco imports
    from chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer

from time import sleep
from threading import Thread, Lock
#import lib.er_pidcontrol as er_pid

from lib.er_io_threads import PressureThread, FilmThread, StopThread
from lib.er_gui_ctrl_plot import CtrlPlot,CtrlPID

from er_gui_plots import ER_plot_component


class ER_State(HasTraits):
    P_Acquire = Event
    P_Acquire_label = Str("Start")
    P_Acquire_state = Bool(False)
        
    # film
    F_Acquire = Event
    F_Acquire_label = Str("Start")
    F_Acquire_state = Bool(False)    

    # display number format
    readonly_fmt = "%.2g "
    # dummy variable to maintain the threads
    pressure_thread = 0
    film_thread = 0
    stop_thread = 0
    # the references to the ui plot objects    
    pressure_plot  = Instance(CtrlPlot)
    P_error_plot   = Instance(CtrlPlot)
    P_output_plot  = Instance(CtrlPlot)    
    F_thickness_plot = Instance(CtrlPlot)
    F_rate_plot      = Instance(CtrlPlot)

    pressure_pid   = Instance(CtrlPID)
    # stop clock
    stop_time = Str("")
    stop_label = Str("Start")
    stop_event = Event 
    stop_state = Bool(False)
    
    view = View(
        HGroup(
        Group(
            VGroup(
                Item('P_Acquire', label="Acquire", editor = ButtonEditor(label_value = 'P_Acquire_label')),
                show_border=True,
                ),
            Group(
                Group(
                    Item(name='pressure_plot',style='custom',show_label=False),
                    ),
                label="Pressure",show_border=True,
                ),
            Group(
                Group(
                    Item(name='pressure_pid',style='custom',show_label=False),
                    ),
                Group(
                    Group(
                        Item(name='P_error_plot',style='custom',show_label=False),
                        ),
                    label="P_error",show_border=True,
                    ),
                Group(
                    Group(
                        Item(name='P_output_plot',style='custom',show_label=False),
                        ),
                    label="P_output",show_border=True,
                    ),
                label="Control",show_border=True,
                ),
            label="Pressure",),
        # =======================================================================
        Group(
            VGroup(
                Item('F_Acquire', label="Acquire", editor = ButtonEditor(label_value = 'F_Acquire_label')),
                show_border=True,
                ),
            VGroup(
                Group(
                    Group(
                        Item(name='F_rate_plot',style='custom',show_label=False),
                        ),
                    label="Rate",show_border=True,
                    ),
                Group(
                    Group(
                        Item(name='F_thickness_plot',style='custom',show_label=False),
                        ),
                    label="Thickness",show_border=True,
                    ),                
                ),
            VGroup(
                Group(
                    Group(
                        Item('stop_event', label="start/stop", editor = ButtonEditor(label_value = 'stop_label'))," ",
                        Item(name='stop_time',style="readonly",label="Time:"),
                        ),
                    label="time",show_border=True,
                    ),                
                #show_border=True,enabled_when='F_Acquire_state',
                ),
            label="Film"), 
        ),#handler = StateHandler(),
    )

    
    # some important actions 
    # Pressure
    def _P_Acquire_fired(self):
        if not self.P_Acquire_state:
	    self.P_Acquire_label = 'Stop'
            #self.Continuous = True
            self.P_Acquire_state = True
            self.P_regulate_state = False
            aq = self._ctrl_pressure_thread()
            print "P_Aquire fired, thread started"            
        else:
	    self.P_Acquire_label = 'Start'
            #self.Continuous = False
            self.P_Acquire_state = False
            self.P_regulate_state = False
            print "P_Aquire fired, thread stopped"
    
    def _pressure_plot_default(self):
	pressure_plot = CtrlPlot(p_obj=self.data.PP)
	return pressure_plot
    
    def _P_error_plot_default(self):
	P_error_plot = CtrlPlot(p_obj=self.data.PE)
	return P_error_plot
    
    def _P_output_plot_default(self):
	P_output_plot = CtrlPlot(p_obj=self.data.PO)
	return P_output_plot    

    def _F_rate_plot_default(self):
	F_rate_plot = CtrlPlot(p_obj=self.data.FR)
	return 	F_rate_plot    

    def _F_thickness_plot_default(self):
	F_thickness_plot = CtrlPlot(p_obj=self.data.FT)
	return 	F_thickness_plot
    
    def _pressure_pid_default(self):
	pressure_pid = CtrlPID(data=self.data,er_state=self)
	#pressure_pid.P_Acquire_state = self.P_Acquire_state
	return pressure_pid

    # start/check thread
    def _ctrl_pressure_thread(self):
        if self.pressure_thread and self.pressure_thread.isAlive():
            self.pressure_thread.Continuous = False
	    pass
        else:
            self.pressure_thread = PressureThread()
            self.pressure_thread.ER = self
            self.pressure_thread.start()

	    
    # <========================================================================>
    # Film
    def _F_Acquire_fired(self):
        if not self.F_Acquire_state:
	    self.F_Acquire_label = 'Stop'
            self.F_Acquire_state = True
            self.F_regulate_state = False
            aq = self._ctrl_film_thread()
            print "P_Aquire fired, thread started"            
        else:
	    self.F_Acquire_label = 'Start'
            self.F_Acquire_state = False
            self.F_regulate_state = False
            print "P_Aquire fired, thread stopped"

    def _SetFilmRate_default(self):
        self.data.F_R_pid = er_pid.pidcontrol()            
        return 1e-7 
    def _F_R_Regulate_fired(self):
	# film rate 
        if self.F_Acquire_state and not self.F_R_regulate_state:
            print "Regulate film rate started"
            self.F_R_regulate_state = True
            self.data.F_R_pid.set_P(self.F_P)
            self.data.F_R_pid.set_I(self.F_I)
            self.data.F_R_pid.set_D(self.F_D)
            self.data.F_R_pid.set_ctrl_value(self.SetFilmRate)
        else:
            print "Regulate film rate stopped"
            self.F_regulate_state = False
            
    def _F_P_changed(self):
        self.data.P_pid.set_P(self.P)
    def _F_I_changed(self):
        self.data.P_pid.set_I(self.I)
    def _F_D_changed(self):
        self.data.P_pid.set_D(self.D)
    def _SetFilmRate_changed(self):
        self.data.F_pid.set_ctrl_value(self.SetFilmRate)
	
    def _F_T_Plot_changed(self):
	# film thickness
	if self.F_T_Plot:
	    # create plot object
	    self.data.F_T_plot = ER_plot_component(data=self.data)
	    # define a couple of properties
	    # close hook
	    self.data.F_T_plot.ctrl_object =  self
	    self.data.F_T_plot.close_event = "F_T_event"
	    # title
	    self.data.F_T_plot.plot_title = "Thickness [nm]"
	    self.data.F_T_plot.title = "Thickness"
	    self.data.F_T_plot.plot_numpoints = 200
	    # make it visible
	    self.data.F_T_plot.make_plot()
	    self.data.F_T_plot.edit_traits(kind="live")	    
	else:
	    "send close event"
	    self.data.F_T_plot.close = 1
    
    # start/check thread
    def _ctrl_film_thread(self):
        if self.film_thread and self.film_thread.isAlive():
            #self.pressure_thread.Continuous = False
	    pass
        else:
            self.film_thread = FilmThread()
            #self.pressure_thread.Continuous = self.Continuous
            self.film_thread.ER = self
            self.film_thread.start()

    # start/check thread
    def _ctrl_stop_thread(self):
        if self.stop_thread and self.stop_thread.isAlive():
            #self.stop_thread.Continuous = False
	    pass
        else:
            self.stop_thread = StopThread()
            self.stop_thread.ER = self
            self.stop_thread.start()
	    
    def _stop_event_fired(self):
        if not self.stop_state:
	    self.stop_label = 'Stop'
            self.stop_state = True
            aq = self._ctrl_stop_thread()
            print "stop time fired, thread started"            
        else:
	    self.stop_label = 'Start'
            #self.Continuous = False
            self.stop_state = False
            print "stop time fired, thread stopped"