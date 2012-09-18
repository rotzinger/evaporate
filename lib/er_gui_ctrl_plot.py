from traits.api import HasTraits, Instance ,Float,Bool,Range, Button,Event, Str ,  List
from traitsui.api import Item, Group, VGroup, HGroup, View, ButtonEditor,EnumEditor, Handler, Label
from er_gui_plots import ER_plot_component
import lib.er_pidcontrol as er_pid

class SingleStateHandler(Handler):
    def object_Pl_event_changed(self, info):
	if info.object.p_obj.debug:
	    print "State object: event toggle dev_reading_plot"
	info.object.dev_reading_plot_window_closed = True
	info.object.dev_reading_plot = False
	info.object.dev_reading_plot_window_closed = False
	
	
class CtrlPlot(HasTraits):
    # window open/close notification
    Pl_event = Event

    dev_reading = Float(0)
    dev_reading_plot = Bool(False)
    dev_reading_plot_window_closed = False
    dev_bad_reading = Bool(False)
    disp_unit = Str("")
    readonly_fmt = "%.3g "
    
    view = View(
        HGroup(
            Item(name='dev_reading_plot',label='Plot',style="custom"),
            Item(name='dev_reading',show_label=False, style="readonly",width = 60,format_str=readonly_fmt),
            '_',
            Item(name='disp_unit',show_label=False,style="readonly"),
            Item(name='dev_bad_reading',label="bad:",style="simple"),
        ),
        handler = SingleStateHandler(),
    )
    def _create_plot(self):
	# create the plot object
	p_object = ER_plot_component(p_obj=self.p_obj)
	p_object.ctrl_object =  self
	# make it visible
	p_object.make_plot()
	self.ui = p_object.edit_traits(kind="live")
	self.ui.title = self.p_obj.plot_title
	
	
    def _disp_unit_default(self):
	return self.p_obj.unit
	
    def _dev_reading_plot_changed(self):
	if self.dev_reading_plot:
	    self._create_plot()
	else:
	    if self.dev_reading_plot_window_closed:
		if self.p_obj.debug:
		    print "plot window closed!"
		return
	    self.ui.dispose()

class CtrlPID(HasTraits):

    P = Float(0.1,desc="set P parameter",auto_set=False, enter_set=True)
    I = Float(0.01,desc="set I parameter",auto_set=False, enter_set=True)
    D = Float(0.00,desc="set D parameter",auto_set=False, enter_set=True)
    
    SetValue = Float(0,desc="set set value",auto_set=False, enter_set=True)
    ManualOutput = Range(0.0,5.0,0,desc="manually set output",auto_set=False, enter_set=True,mode='text')
    Regulate = Button()
    Regulate_state = Bool(False)
    #RegulateOn = Enum("Penning","Ionivac")
    RegulateOn = List()
    RegulateOn_value = Str()
    view = View(
        VGroup(
            Group(Item(name='ManualOutput'),enabled_when='not Regulate_state',show_border=True),
            Item(name='SetValue'),
            Item(name='P',label='P'),            
            Item(name='I',label='I'),
            Item(name='D',label='D'),
            " ",
            Item(name='RegulateOn_value',label = "Regulate on:",editor=EnumEditor(name='RegulateOn')),
            Item(name='Regulate'),
            ),
        #handler = SingleStateHandler(),
    )
    def _Regulate_fired(self):
	#print self.P_Acquire_state, self.Regulate_state, 
        if self.er_state.P_Acquire_state and not self.Regulate_state:
            print "Regulate pressure started"
            self.Regulate_state = True
            self.data.P_pid.set_P(self.P)
            self.data.P_pid.set_I(self.I)
            self.data.P_pid.set_D(self.D)
            self.data.P_pid.set_ctrl_value(self.SetValue)
        else:
            print "Regulate pressure fired off"
            self.Regulate_state = False
    def _RegulateOn_default(self): 
	return self.data.PID_P.input_devices

	
    def _RegulateOn_value_changed(self):
	what_num = self.data.PID_P.input_devices.index(self.RegulateOn_value)
	print what_num
	"""
        if self.RegulateOn_value == self.data.PID_P.input_devices[0]:
            print "Moving to totally covered position"
        if self.RegulateOn_value == self.data.PID_P.input_devices[1]:
            print "Moving to totally exposed position"

	"""    
    def _P_default(self):
        return self.data.PID_P.P
    def _I_default(self):
        return self.data.PID_P.I
    def _D_default(self):
        return self.data.PID_P.D

    def _P_changed(self):
	self.data.P_pid.set_P(self.P)
    def _I_changed(self):
	self.data.P_pid.set_I(self.I)
    def _D_changed(self):
	self.data.P_pid.set_D(self.D)
	
    def _SetValue_default(self):
	self.data.P_pid = er_pid.pidcontrol()
	return 1e-7    
    def _SetValue_changed(self):
	self.data.P_pid.set_ctrl_value(self.SetValue)
	
    def _ManualOutput_changed(self):
	print self.ManualOutput
	self.data.DAQ_Dev.output(0,self.ManualOutput)
