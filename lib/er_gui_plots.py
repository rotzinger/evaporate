from numpy import arange,zeros,delete, append

try:
    from enthought.enable.api import Window, Component, ComponentEditor
    from enthought.traits.api import HasTraits, Instance ,Float, Button,Array,false,on_trait_change
    from enthought.traits.ui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow
    # Chaco imports
    from enthought.chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer, PlotAxis
    from enthought.chaco.scales.formatters import BasicFormatter
    from enthought.chaco.scales_tick_generator  import ScalesTickGenerator
    from enthought.chaco.scales.api import DefaultScale, LogScale, ScaleSystem
except:
    from enable.api import Window, Component, ComponentEditor
    from traits.api import HasTraits, Instance ,Float, Button,Array,false,on_trait_change
    from traitsui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow
    # Chaco imports
    from chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer, PlotAxis
    from chaco.scales.formatters import BasicFormatter
    from chaco.scales_tick_generator  import ScalesTickGenerator
    from chaco.scales.api import DefaultScale, LogScale, ScaleSystem

class ER_plot_component(HasTraits):
    view = View( Group(Item(name='container',editor=ComponentEditor(),show_label=False)))
    def __init__(self,data, **traits):
        HasTraits.__init__(self, **traits)
        numpoints = 100
        self.pressure_array = zeros(numpoints)
        self.P_error_array = zeros(numpoints)
        self.P_output_array = zeros(numpoints)
        # ==============================
        self.pressure_pd = ArrayPlotData(pressure=self.pressure_array)
        self.pressure_plot = Plot(self.pressure_pd)
        #self.pressure_plot.y_axis.title = "Pressure [mBar]"
	self.pressure_plot.padding_left = 80
	self.pressure_plot.y_axis.visible = False
	self.pressure_plot.plot(("pressure"),type="line", color="blue",render_style='connectedhold')
	tick_gen = ScalesTickGenerator(scale=DefaultScale())
	y_axis = PlotAxis(orientation='left',
	                  title="Pressure [mBar]",
	                  mapper=self.pressure_plot.value_mapper,
	                  component=self.pressure_plot,
	                  tick_generator = tick_gen)
	self.pressure_plot.underlays.append(y_axis)
	# ============================= <- this was some work due to lack of documentation or finding it.
	
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
        
    def _gen_pressure_array(self, m_Pressure):
        #print "_generate array called"
        self.pressure_array= delete(
            append(self.pressure_array,m_Pressure),0)
        self.pressure_pd.set_data("pressure",self.pressure_array)
        
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
#===============================================================================
