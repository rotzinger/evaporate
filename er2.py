
#from numpy import arange,delete,append, zeros
# Enthought library imports
#from time import sleep
#from threading import Thread, Lock

#if __name__ == '__main__':
if True:
    # this should always work ;-)
    from lib.er_data import DATA    
    #global data 
    data = DATA()
    
    import lib.er_pidcontrol as er_pid
    data.pid = er_pid.pidcontrol()
    # gui

    from lib.er_gui_controls import ER_State
    ER_State.data = data
    from lib.er_gui_plots import ER_plot_component
    ER_plot_component.data = data
    from lib.er_gui import EvapoRate
    EvapoRate.data = data
    print "main",dir(data)

    # try loading devices ...
    try:
        # import modules
        import lib.er_ratedev as r_dev        
        data.r_dev = r_dev.Rate_Dev()
        
    except:
        print ("ER: Rate dev not found, loading dummy.")
        class Rate_Dev(object):
            def get_Rate(self): return 0
        data.r_dev = Rate_Dev()
    
    try:
        import lib.er_pycomedi as comedi
        data.DAQ_Dev = comedi.IO_Dev()
        
        # for the default NI-DAQ device, this configures AO0 and AO1 output channels (0,1)
        data.DAQ_Dev.configure_ao()
        #data.DAQ_Dev.output(0,float(var))
        #DAQ_Dev.output(1,0)
        #DAQ_Dev.close()
    except:
        print ("ER: comedi DAQ device not loaded, loading dummy.")
        class DAQ_Dev(object):
                    def output(self,channel, value): return 0
        data.DAQ_Dev = DAQ_Dev()
        
    try:
        import lib.er_combivac as combivac
        data.P_Dev = Pressure_Dev()
        #print data.P_Dev.setHV(on=False)
        #print data.P_Dev.getPM()        
    except:
        print ("ER: combivac device not loaded, loading dummy.")
        from random import random
        class P_Dev(object):
            def getPM(self): return random()*1e-5
        data.P_Dev = P_Dev()
        #data.P_Dev.getPM()
    title="EvapoRate v2 HR@KIT/2012"
    ER = EvapoRate(data=data)
    ER.configure_traits()