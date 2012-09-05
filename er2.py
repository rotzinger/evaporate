
#from numpy import arange,delete,append, zeros
# Enthought library imports
#from time import sleep
#from threading import Thread, Lock

#if __name__ == '__main__':
if True:
    # this should always work ;-)
    from lib.er_data import DATA 
    data = DATA()
    
    # create permanent pid object
    #import lib.er_pidcontrol as er_pid
    #data.press_pid = er_pid.pidcontrol()
    # gui

    from lib.er_gui_controls import ER_State
    ER_State.data = data
    from lib.er_gui_plots import ER_plot_component
    ER_plot_component.data = data
    from lib.er_gui import EvapoRate
    EvapoRate.data = data
    
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
        data.P_Devs.append(combivac.Pressure_Dev())
        #print data.P_Dev.setHV(on=False)
        #print data.P_Dev.getPM()        
    except:
        print ("ER: combivac device not loaded, loading dummy.")
        from random import random
        from math import sin
        from time import time
        class P_Dev(object):
            def getUHV(self): return 1.5e-4+1e-4*sin(time())+random()*3e-5
        data.P_Devs.append(P_Dev())
        
        #data.P_Dev.getPM()
    try:    
        import lib.er_ionivac as ionivac
        data.P_Devs.append(ionivac.Pressure_Dev())
        #print data.P_Dev.setHV(on=False)
        #print data.P_Dev.getPM()        
    except:
        print ("ER: ionivac device not loaded, loading dummy.")
        from random import random
        from math import sin
        from time import time
        class IP_Dev(object):
            def getUHV(self): return 1.5e-4+1e-4*sin(time())+random()*3e-5
        #data.IP_Dev = IP_Dev()
        data.P_Devs.append(IP_Dev())
    try:
        import lib.er_ratedev as ratedev
        data.R_Dev=ratedev.Rate_Dev()
        #print rd.getHello()
        #print 'Rate:',rd.getRate()/10
        #print 'Thickness:',rd.getThickness()*100        
    except:
        print ("ER: inficon ratedev device not loaded, loading dummy.")
        from random import random
        class Rate_Dev(object):
                    def getRate(self,nm=False): return random()*10
                    def getThickness(self,nm=False): return random()*100
        data.R_Dev = Rate_Dev()
        # print 'Rate:',data.R_Dev.getRate(nm=True)
        # print 'Thickness:',data.R_Dev.getThickness(nm=True)        
        

    title="EvapoRate v3 HR@KIT/2012"
    ER = EvapoRate(data=data)

    #ER.edit_traits(view='plots_view')
    ER.configure_traits()
