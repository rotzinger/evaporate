
from numpy import arange

# Enthought library imports
from enthought.enable.api import Window, Component, ComponentEditor
from enthought.traits.api import HasTraits, Instance ,Float, Button,false
from enthought.traits.ui.api import Item, Group,VGroup,HGroup, View, HSplit, VSplit, HFlow
# Chaco imports
from enthought.chaco.api import HPlotContainer, ArrayPlotData, Plot,VPlotContainer

from time import sleep
from threading import Thread, Lock

# import modules
import lib.er_ratedev as r_dev
from lib.er_ftdidev import er_output as o_dev
import lib.tip_pidcontrol as er_pid


# data share
class data(object):
    "data object"
    def __init__(self):
        # define operational variables
        self.m_thickness = 0
        self.m_rate    = 0
        self.m_time    = 0
        self.m_error   = 0
        self.o_new_val = 0
        self.pid_P = 0
        self.pid_I = 0
        self.pid_D = 0

        self.pid = 0
        self.r_dev = 0
        
        self.lock = Lock()
        
    def get_thickness(self):
        return self.m_thickness
    def set_thickness(self,tn):
        with self.lock:
            self.m_thickness = tn
        
    def get_rate(self):
        return self.m_rate
    def set_rate(self,rt):
        with self.lock:
            self.m_rate = rt

    def set_pid_p(self,P):
        with self.lock:
            self.pid_P = P
            
    def set_pid_i(self,I):
        with self.lock:
            self.pid_I = I

    def set_pid_d(self,D):
        with self.lock:
            self.pid_D = D

class ER_plot_component(HasTraits):
    # Create the index
    numpoints = 100
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
    
    container = VPlotContainer(stack_order="top_to_bottom",background="lightgray")
    container.spacing = 0
    current_plot.padding_top = rate_plot.padding_bottom
    
    container.add(rate_plot)
    container.add(current_plot)
    container.add(thickness_plot)
    view = View( Group(Item(name='container',editor=ComponentEditor(),show_label=False)))

#===============================================================================



    
class ER_State(HasTraits):
    SetRate = Float(0.1)
    SetThickness = Float(0.1)
    Regulate = Button()
    Acquire = Button()
    P = Float(0.00,desc="set P parameter",auto_set=False, enter_set=True)
    I = Float(0.00,desc="set I parameter",auto_set=False, enter_set=True)
    D = Float(0.00,desc="set D parameter",auto_set=False, enter_set=True)
    inout_thread = ""
    acquire = False
    
    view = View(
        Group(
            VGroup(
                Item(name='Acquire'),
                show_border=True,
                ),

            VGroup(
                Item(name='SetRate'),
                Item(name='SetThickness'),
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
        self.Continuous = True
        self.acquire = True
        aq = self.inout_data()
        print "Aquire fired, thread started"
        
    def _Regulate_fired(self):
        print "Regulate fired"
        #self.Regulate = True
        
    def _Regulate_default(self):
        pass
    def _Tctrl_changed(self):
        pass

    def _P_changed(self):
        data.set_pid_p(self.P)
    def _I_changed(self):
        data.set_pid_i(self.I)
    def _D_changed(self):
        data.set_pid_d(self.D)
        
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
        m_rate = 0
        SetRate = self.ER.SetRate
        #thickness = self.ER.m_thickness
        # aquire
        # m_rate    = self.ER.m_rate
        #outputCurrent = self.ER.outputCurrent
        #regulateRate  = self.ER.regulateRate
        
        while self.Continuous:
            sleep(0.001)
            if self.ER.acquire:
                try:
                    "get Rate from xal"
                    m_rate = data.r_dev.getRate()
                    data.set_rate(m_rate)
                except:
                    print "no rate taken"
                # calculate new output value
                o_new_val, error = data.pid.update_Heat(m_rate)
            if self.ER.regulate:
                #out_current = get_current_from_PID()
                # output something
                HT=o_dev.set_output(o_new_val)
                # save the error
                data.set_pidE(error)
                
            if outputCurrent:
                try:
                    pass
                except:
                    print "no current output"


# main object -> called by __main__
class EvapoRate(HasTraits):
    " Bring up the whole mess"
    figure = Instance(ER_plot_component)
    er_state = Instance(ER_State)
    traits_view = View(HSplit(
            Item('figure', style='custom',show_label=False,width=0.7),
            Item('er_state',style='custom',show_label=False,label='State'),
        ),
        resizable=True, 
        height=0.7, width=0.6,
        title='EvapoRate v2 HR@KIT2012'
      )

    def _figure_default(self):
        return ER_plot_component()
    
    def _er_state_default(self):
        return ER_State()


if __name__ == '__main__':
    data = data()
    pid =  er_pid.pidcontrol(data)
    data.pid = pid
    
    try:
        data.r_dev = r_dev.Rate_Dev()
    except:
        print "Rate dev not found"
        class Rate_Dev(object):
            def get_Rate(self): return 0
        data.r_dev = Rate_Dev()
        
    title="EvapoRate v2 HR@KIT/2012"
    ER = EvapoRate()
    ER.configure_traits()



"""
#update the values in the storage
            
            self.DATA.set_last_Res(R)
            T = self.RBR.get_T_from_R(R)
            self.DATA.set_Temp(T)
            ## for do not heat to much the mixing chamber
            if T > 0.7:
                self.HTR.set_Heat(0)
                self.DATA.set_ctrl_Temp(0)
                
            NHW,error = self.DATA.PID.update_Heat(T)
            # set the new heating power from pid
            HT=self.HTR.set_Heat(NHW)
            self.DATA.set_Heat(HT)
            if self.DATA.debug:
                print "T=%.2fmK R=%.2fOhm Heat %0.4f(V) %.4f(uW)" % (T*1000,R,HT,HT**2/480*1e6)
            self.DATA.set_pidE(error)
"""            
