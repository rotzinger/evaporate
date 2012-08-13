from numpy import arange,zeros,delete, append

try:
    from enthought.enable.api import Window, Component, ComponentEditor
    from enthought.traits.api import HasTraits, Instance ,Float, Button,Array,false,on_trait_change, Event
    from enthought.traits.ui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow, Handler
    # Chaco imports
    from enthought.chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer, PlotAxis
    from enthought.chaco.scales.formatters import BasicFormatter
    from enthought.chaco.scales_tick_generator  import ScalesTickGenerator
    from enthought.chaco.scales.api import DefaultScale, LogScale, ScaleSystem
except:
    from enable.api import Window, Component, ComponentEditor
    from traits.api import HasTraits, Instance ,Float, Button,Array,false,on_trait_changem, Event
    from traitsui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow, Handler
    # Chaco imports
    from chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer, PlotAxis
    from chaco.scales.formatters import BasicFormatter
    from chaco.scales_tick_generator  import ScalesTickGenerator
    from chaco.scales.api import DefaultScale, LogScale, ScaleSystem


class PlotHandler(Handler):
    def object_close_changed(self, info):
	# external event closes window
        print "Plot object closed by event"
	if not info.object.closing:
	    info.ui.owner.close()
    def close(self, info, isok):
	info.object.closing = True
	# hook for the pressed window destroy button 
	print "Plot close called by window button", info.object.close_event
	# send an event to the ctrl object "info.object.ctrl_object" with the 
	# event name "info.object.close_event" (str)
	setattr(info.object.ctrl_object, info.object.close_event, 1)
	return True

class ER_plot_component(HasTraits):
    close = Event
    closing = False
    #view = View( Group(Item(name='container',editor=ComponentEditor(),show_label=False)))
    view = View( 
        Group(
            Item(name='plot_ren',editor=ComponentEditor(),show_label=False)
        ),
        handler=PlotHandler(),x=0.1,y=0.1
    )
    
    def __init__(self,data, **traits):
        HasTraits.__init__(self, **traits)
	self.plot_title = "none"
	self.plot_numpoints = 100
	
    def make_plot(self):
        self.P_data_array = zeros(self.plot_numpoints)
        # ==============================
        self.pd = ArrayPlotData(P_data=self.P_data_array)
        self.plot_ren = Plot(self.pd)
        #self.pressure_plot.y_axis.title = "Pressure [mBar]"
	self.plot_ren.padding_left = 80
	self.plot_ren.y_axis.visible = False
	self.plot_ren.plot(("P_data"),type="line", color="blue",render_style='connectedhold')
	tick_gen = ScalesTickGenerator(scale=DefaultScale())
	y_axis = PlotAxis(orientation='left',
	                  title=self.plot_title,
	                  mapper=self.plot_ren.value_mapper,
	                  component=self.plot_ren,
	                  tick_generator = tick_gen)
	self.plot_ren.underlays.append(y_axis)
	# ============================= <- this was some work due to lack of documentation or finding it.

    def _gen_array(self, m_Pressure):
        #print "_generate array called"
        self.P_data_array= delete(
            append(self.P_data_array,m_Pressure),0)
        self.pd.set_data("P_data",self.P_data_array)
    """
    def _gen_P_error_array(self, P_error):
        #print "_generate array called"
        self.P_error_array = delete(
            append(self.P_error_array,P_error),0)
        self.P_error_pd.set_data("P_error",self.P_error_array)    

    def _gen_P_output_array(self, P_output):
	#print "_generate array called"
	self.P_output_array = delete(
	    append(self.P_output_array,P_output),0)
	self.P_output_pd.set_data("P_output",self.P_output_array)
    """
#===============================================================================
"""
self.P_error_pd = ArrayPlotData(P_error=self.P_error_array)
self.P_errror_plot = Plot(self.P_error_pd)
self.P_errror_plot.index_range = self.pressure_plot.index_range
self.P_errror_plot.y_axis.title = "Error [mBar]"
self.P_errror_plot.plot(("P_error"),type="line", color="blue")
self.P_errror_plot.padding_left = 80        
self.P_output_pd = ArrayPlotData(P_output=self.P_output_array)
self.P_output_plot = Plot(self.P_output_pd)
self.P_output_plot.index_range = self.pressure_plot.index_range
self.P_output_plot.y_axis.title = "P_output [V]"
self.P_output_plot.plot(("P_output"),type="line", color="blue")        
self.P_output_plot.padding_left = 80

self.container = VPlotContainer(stack_order="top_to_bottom",background="lightgray")
self.container.spacing = -75
#self.P_output_plot.padding_top = self.pressure_plot.padding_bottom


self.container.add(self.pressure_plot)
self.container.add(self.P_errror_plot)
self.container.add(self.P_output_plot)
"""
