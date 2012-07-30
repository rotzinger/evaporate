from numpy import arange,zeros,delete, append

try:
    from enthought.enable.api import Window, Component, ComponentEditor
    from enthought.traits.api import HasTraits, Instance ,Float, Button,Array,false,on_trait_change
    from enthought.traits.ui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow
    # Chaco imports
    from enthought.chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer
except:
    from enable.api import Window, Component, ComponentEditor
    from traits.api import HasTraits, Instance ,Float, Button,Array,false,on_trait_change
    from traitsui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow
    # Chaco imports
    from chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer

class ER_plot_component(HasTraits):
    view = View( Group(Item(name='container',editor=ComponentEditor(),show_label=False)))
    def __init__(self,data, **traits):
        HasTraits.__init__(self, **traits)
        numpoints = 20
        self.pressure_array = zeros(numpoints)
        self.P_error_array = zeros(numpoints)
        self.P_output_array = zeros(numpoints)
        
        # Create the index
        #numpoints = 1000
        #x = arange(numpoints)
        #plotdata = ArrayPlotData(x=x, y1=x, y2=x**2)

        
        self.pressure_pd = ArrayPlotData(pressure=self.pressure_array)
        self.pressure_plot = Plot(self.pressure_pd)
        self.pressure_plot.y_axis.title = "Pressure [mBar]"
        self.pressure_plot.value_scale = "log"
        #self.pressure_plot.ticks.log_auto_ticks(1e-7, 1e-4, 'auto', 'auto', 'auto')
	self.pressure_plot.plot(("pressure"),type="line", color="blue") 


        self.P_error_pd = ArrayPlotData(P_error=self.P_error_array)
        self.P_errror_plot = Plot(self.P_error_pd)
        self.P_errror_plot.index_range = self.pressure_plot.index_range
        self.P_errror_plot.y_axis.title = "Error [mBar]"
        self.P_errror_plot.plot(("P_error"),type="line", color="blue")
        
        self.P_output_pd = ArrayPlotData(P_output=self.P_output_array)
        self.P_output_plot = Plot(self.P_output_pd)
        self.P_output_plot.index_range = self.pressure_plot.index_range
        self.P_output_plot.y_axis.title = "P_output [V]"
        self.P_output_plot.plot(("P_output"),type="line", color="blue")        
        
        self.container = VPlotContainer(stack_order="top_to_bottom",background="lightgray")
        self.container.spacing = 0
        self.P_output_plot.padding_top = self.pressure_plot.padding_bottom
        
        
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
