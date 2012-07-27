from numpy import arange

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

class ER_plot_component(HasTraits):
    view = View( Group(Item(name='container',editor=ComponentEditor(),show_label=False)))
    def __init__(self,data, **traits):
        HasTraits.__init__(self, **traits)
        
        # Create the index
        numpoints = 1000
        low = -5
        high = 15.0
        x = arange(low, high, (high-low)/numpoints)
        plotdata = ArrayPlotData(x=x, y1=x, y2=x**2)

        rate_plot = Plot(plotdata)
        rate_plot.y_axis.title = "rate [nm/s]"
        renderer = rate_plot.plot(("x", "y1"), type="line", color="blue", width=2.0)[0]
        
        thickness_plot = Plot(plotdata)
        thickness_plot.index_range = rate_plot.index_range
        thickness_plot.y_axis.title = "thickness [nm]"
        thickness_plot.plot(("x", "y2"),type="line", color="blue")
        thickness_plot.x_axis.title = "time"
        
        
        current_plot = Plot(plotdata)
        current_plot.index_range = rate_plot.index_range
        current_plot.y_axis.title = "Current [A]"
        current_plot.plot(("x", "y2"),type="line", color="blue")
    
        print "hallo" #data.pressure_array
        #pressure_pd = ArrayPlotData(x=x, y1=data.pressure_array)
        pressure_plot = Plot(plotdata)
        pressure_plot.index_range = rate_plot.index_range
        pressure_plot.y_axis.title = "Current [A]"
        pressure_plot.plot(("x", "y2"),type="line", color="blue")    


        self.rate_plot = rate_plot
        self.pressure_plot = pressure_plot
        self.thickness_plot = thickness_plot
        self.pressure_plot = pressure_plot
        self.current_plot  = current_plot
        container = VPlotContainer(stack_order="top_to_bottom",background="lightgray")
        container.spacing = 0
        self.current_plot.padding_top = self.rate_plot.padding_bottom
        
        
        container.add(self.rate_plot)
        #container.add(self.current_plot)
        container.add(self.pressure_plot)
        container.add(self.thickness_plot)
        container.add(self.pressure_plot)
        self.container = container
        #self.view = View( Group(Item(name='self.container',editor=ComponentEditor(),show_label=False)))

#===============================================================================
