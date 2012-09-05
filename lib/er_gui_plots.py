from numpy import arange,zeros,delete, append

#try:
    #from enthought.enable.api import Window, Component, ComponentEditor
    #from enthought.traits.api import HasTraits, Instance ,Float, Button,Array,false,on_trait_change, Event
    #from enthought.traits.ui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow, Handler
    ## Chaco imports
    #from enthought.chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer, PlotAxis
    #from enthought.chaco.scales.formatters import BasicFormatter
    #from enthought.chaco.scales_tick_generator  import ScalesTickGenerator
    #from enthought.chaco.scales.api import DefaultScale, LogScale, ScaleSystem
#except:
if 1:
    from enable.api import Window, Component, ComponentEditor
    from traits.api import HasTraits, Instance ,Float, Button,Array,false,on_trait_change, Event
    from traitsui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow, Handler
    # Chaco imports
    from chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer, PlotAxis
    from chaco.scales.formatters import BasicFormatter
    from chaco.scales_tick_generator  import ScalesTickGenerator
    from chaco.scales.api import DefaultScale, LogScale, ScaleSystem


class PlotHandler(Handler):
    def close(self, info, isok):
	info.object.closing = True
	# hook for the pressed window destroy button
	if info.object.p_obj.debug:
	    print "Plot close called by window button", info.object.p_obj.event_name
	# send an event to the ctrl object "info.object.ctrl_object" with the 
	# event name "info.object.p_obj.event_name" (str)
	setattr(info.object.ctrl_object, info.object.p_obj.event_name, 1)
	return True
    def init(self, info):
	# position the windows
	info.ui.view.x = info.object.p_obj.x_pos
	info.ui.view.y = info.object.p_obj.y_pos
	info.ui.view.height = info.object.p_obj.y_size
	info.ui.view.width  = info.object.p_obj.x_size
	return True

class ER_plot_component(HasTraits):
    close = Event
    closing = False
    title = ""
    #view = View( Group(Item(name='container',editor=ComponentEditor(),show_label=False)))
    view = View( 
        Group(
            Item(name='plot_ren',editor=ComponentEditor(size=(100,100)),show_label=False)
        ),
        handler=PlotHandler(),resizable=True,
    )
    
    def __init__(self,p_obj, **traits):
        HasTraits.__init__(self, **traits)
	self.x =0.2
	self.p_obj = p_obj
	
    def make_plot(self):
        # ==============================
        #self.pd = ArrayPlotData(P_data=self.data.m_Pressures_array)
	
	# we store the array plotdata in the data object and update it there 
	self.p_obj.values_array_pd = ArrayPlotData(P_data=self.p_obj.values_array)
	self.plot_ren = Plot(self.p_obj.values_array_pd)
        
	self.plot_ren.padding_left = 70 #80
	self.plot_ren.padding_right = 5
	self.plot_ren.padding_top = 5
	self.plot_ren.padding_bottom = 40
	self.plot_ren.x_axis.title = self.p_obj.x_axis
	self.plot_ren.y_axis.visible = False
	self.plot_ren.plot(("P_data"),type="line", color="blue",render_style='connectedhold')
	tick_gen = ScalesTickGenerator(scale=DefaultScale())
	y_axis = PlotAxis(orientation='left',
	                  title=self.p_obj.y_axis,
	                  mapper=self.plot_ren.value_mapper,
	                  component=self.plot_ren,
	                  tick_generator = tick_gen)
	self.plot_ren.underlays.append(y_axis)
	# ============================= <- this was some work due to lack of documentation or finding it.

#===============================================================================

