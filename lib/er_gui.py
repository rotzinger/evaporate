# main gui object -> called by __main__
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

from er_gui_controls import ER_State
from er_gui_plots import ER_plot_component

class EvapoRate(HasTraits):
    " Bring up the whole mess"

    er_plots = Instance(ER_plot_component)
    er_state = Instance(ER_State)
    
    traits_view = View(HSplit(
            Item('er_plots', style='custom',show_label=False,width=0.7),
            Item('er_state',style='custom',show_label=False,label='State'),
        ),
        resizable=True, 
        height=0.7, width=0.6,
        title='EvapoRate v2 HR@KIT2012'
      )

    def _er_plots_default(self):
        er_plots = ER_plot_component(data=self.data)
        self.data.er_plots = er_plots
        return er_plots
    
    def _er_state_default(self):
        er_state = ER_State(data=self.data)
        self.data.er_state = er_state
        return er_state 
    