try:
    from enthought.enable.api import Window, Component, ComponentEditor
    from enthought.traits.api import HasTraits, Instance ,Float, Bool, Button,Event,Str,false
    from enthought.traits.ui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow,ButtonEditor,Handler
    # Chaco imports
    from enthought.chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer
except:
    from enable.api import Window, Component, ComponentEditor
    from traits.api import HasTraits, Instance ,Float,Bool, Button,Event,Str,false
    from traitsui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow, ButtonEditor,Handler
    # Chaco imports
    from chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer

from time import sleep
from threading import Thread, Lock
import lib.er_pidcontrol as er_pid

from lib.er_io_threads import PressureThread

from er_gui_plots import ER_plot_component

class StateHandler(Handler):
    def object_P_event_changed(self, info):
        print "State object: event toggle PP"
	info.object.Pressure_Plot = False
    def object_PE_event_changed(self, info):
	print "State object: event toggle PE"
	info.object.P_error_Plot = False    
    def object_PO_event_changed(self, info):
	print "State object: event toggle PO"
	info.object.P_output_Plot = False
    def object_F_T_event_changed(self, info):
	print "State object: event toggle F_T"
	info.object.F_T_Plot = False    
	
class ER_State(HasTraits):
    # window open/close notification
    P_event = Event
    PE_event = Event
    PO_event = Event
    #Pressure_event = Event

    # Pressure

    Pressure = Float(0)
    Pressure_Plot = Bool(False)

    P_error = Float(0)
    P_error_Plot = Bool(False)
    P_output = Float(0)
    P_output_Plot = Bool(False)    
    
    P_Acquire = Event
    P_Acquire_label = Str("Start")
    P_Acquire_state = Bool(False)
    
    SetPressure = Float(0,desc="set D parameter",auto_set=False, enter_set=True)
    P_Regulate = Button()
    P_Regulate_state = Bool(False)
    
    P_P = Float(0.1,desc="set P parameter",auto_set=False, enter_set=True)
    P_I = Float(0.01,desc="set I parameter",auto_set=False, enter_set=True)
    P_D = Float(0.00,desc="set D parameter",auto_set=False, enter_set=True)
    
    # film
    F_Acquire = Event
    F_Acquire_label = Str("Start")
    F_Acquire_state = Bool(False)
    
    #Rate = Float(0)
    #Thickness = Float(0)
    
    F_T = Float(0)
    F_T_Plot = Bool(False)
    F_R = Float(0)
    F_R_Plot = Bool(False)
    
    F_R_Regulate = Bool(False)
    
    F_R_error = Float(0)
    F_R_error_Plot = Bool(False)
    F_R_output = Float(0)
    F_R_output_Plot = Bool(False)    
    
    Set_F_R = Float(0,desc="set Film rate parameter",auto_set=False, enter_set=True)
    F_P = Float(0.1,desc="set P parameter",auto_set=False, enter_set=True)
    F_I = Float(0.01,desc="set I parameter",auto_set=False, enter_set=True)
    F_D = Float(0.00,desc="set D parameter",auto_set=False, enter_set=True)
    

    # display number format
    readonly_fmt = "%.2g "
    # dummy variable to maintain the threads
    pressure_thread = 0
    film_thread = 0
    # Acquire state
    
    
    view = View(
        HGroup(
        Group(
            VGroup(
                Item('P_Acquire', label="Acquire", editor = ButtonEditor(label_value = 'P_Acquire_label')),
                show_border=True,
                ),
            VGroup(
                HGroup(
                    Item(name='Pressure_Plot',label='Plot',style="custom"),
                    Item(name='Pressure',style="readonly",format_str=readonly_fmt)
                    ),
                #Item(name="Pressure_regul",label="Regulate",style="custom"),
                show_border=True,
                ),
            
            #VGroup(
                #HGroup(Item(name='Thickness_Plot',label='Plot',style="custom"),
                       #Item(name='Thickness',style="readonly",format_str="%.2f "),
                       #),
                #HGroup(Item(name='Rate_Plot',label='Plot',style="custom"),
                       #Item(name='Rate',style="readonly",format_str="%.2f ")),
                #show_border=True,
                #),
            
            VGroup(
                Item(name='SetPressure'),
                Item(name='P_P',label='P'),
                Item(name='P_I',label='I'),
                Item(name='P_D',label='D'),
                Item(name='P_Regulate'),
                HGroup(
                    Item(name='P_error_Plot',label='Plot',style="custom"),
                    Item(name='P_error',style="readonly",format_str=readonly_fmt)
                ),
                HGroup(
                    Item(name='P_output_Plot',label='Plot',style="custom"),
                    Item(name='P_output',style="readonly",format_str=readonly_fmt),
                ),                
                show_border=True,enabled_when='P_Acquire_state',
                ),
            label="Pressure",),
        # =======================================================================
        Group(
            VGroup(
                Item('F_Acquire', label="Acquire", editor = ButtonEditor(label_value = 'F_Acquire_label')),
                show_border=True,
                ),
            VGroup(
                HGroup(
                    Item(name='F_R_Plot',label='Plot',style="custom"),
                    Item(name='F_R',label="Rate",style="readonly",format_str=readonly_fmt)
                    ),
                HGroup(Item(name='F_T_Plot',label='Plot',style="custom"),
                       Item(name='F_T',label='Thickness',style="readonly",format_str=readonly_fmt),
                       ),
                Item(name="F_R_Regulate",label="Regulate",style="custom"),
                show_border=True,
                ),
            VGroup(
                Item(name='Set_F_R'),
                Item(name='F_P',label='P'),
                Item(name='F_I',label='I'),
                Item(name='F_D',label='D'),
                Item(name='F_Regulate'),
                HGroup(
                    Item(name='F_R_error_Plot',label='Plot',style="custom"),
                    Item(name='F_R_error',style="readonly",format_str=readonly_fmt)
                ),
                HGroup(
                    Item(name='F_R_output_Plot',label='Plot',style="custom"),
                    Item(name='F_R_output',style="readonly",format_str=readonly_fmt),
                ),                
                show_border=True,enabled_when='F_Acquire_state',
                ),
            label="Film"), 
        ),handler = StateHandler(),
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

    def _SetPressure_default(self):
        self.data.P_pid = er_pid.pidcontrol()            
        return 1e-7 
    def _P_Regulate_fired(self):
        if self.P_Acquire_state and not self.P_Regulate_state:
            print "Regulate pressure started"
            self.P_Regulate_state = True
            self.data.P_pid.set_P(self.P_P)
            self.data.P_pid.set_I(self.P_I)
            self.data.P_pid.set_D(self.P_D)
            self.data.P_pid.set_ctrl_value(self.SetPressure)
        else:
            print "Regulate pressure fired off"
            self.P_Regulate_state = False
            
    def _P_P_changed(self):
        self.data.P_pid.set_P(self.P_P)
    def _P_I_changed(self):
        self.data.P_pid.set_I(self.P_I)
    def _P_D_changed(self):
        self.data.P_pid.set_D(self.P_D)
    def _SetPressure_changed(self):
        self.data.P_pid.set_ctrl_value(self.SetPressure)
	
    def _Pressure_Plot_changed(self):
	if self.Pressure_Plot:
	    # create plot object
	    self.data.P_plot = ER_plot_component(data=self.data)
	    # define a couple of properties
	    # close hook
	    self.data.P_plot.ctrl_object =  self
	    self.data.P_plot.close_event = "P_event"
	    # title
	    self.data.P_plot.plot_title = "Pressure [mBar]"
	    self.data.P_plot.plot_numpoints = 200
	    # make it visible
	    self.data.P_plot.make_plot()
	    self.data.P_plot.edit_traits(kind="live")	    
	else:
	    "send close event"
	    self.data.P_plot.close = 1


    def _P_error_Plot_changed(self):
	if self.P_error_Plot:
	    # create plot object
	    self.data.PE_plot = ER_plot_component(data=self.data)
	    # define a couple of properties
	    # close hook
	    self.data.PE_plot.ctrl_object =  self
	    self.data.PE_plot.close_event = "PE_event"
	    # title
	    self.data.PE_plot.plot_title = "Pressure [mBar]"
	    self.data.PE_plot.plot_numpoints = 200
	    # make it visible
	    self.data.PE_plot.make_plot()
	    self.data.PE_plot.edit_traits(kind="live")	    
	else:
	    "send close event"
	    self.data.PE_plot.close = 1

    def _P_output_Plot_changed(self):
	if self.P_output_Plot:
	    # create plot object
	    self.data.PO_plot = ER_plot_component(data=self.data)
	    # define a couple of properties
	    # close hook
	    self.data.PO_plot.ctrl_object =  self
	    self.data.PO_plot.close_event = "PO_event"
	    # title
	    self.data.PO_plot.plot_title = "Volt [a.u.]"
	    self.data.PO_plot.plot_numpoints = 200
	    # make it visible
	    self.data.PO_plot.make_plot()
	    self.data.PO_plot.edit_traits(kind="live")	    
	else:
	    "send close event"
	    self.data.PO_plot.close = 1

    # start/check thread
    def _ctrl_pressure_thread(self):
        if self.pressure_thread and self.pressure_thread.isAlive():
            self.pressure_thread.Continuous = False
	    pass
        else:
            self.pressure_thread = PressureThread()
            #self.pressure_thread.Continuous = self.Continuous
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

