#/usr/bin/env python
from random import random
from math import sin
from time import time

if __name__ == '__main__':
    # this should always work ;-)
    from lib.er_data import DATA 
    data = DATA()
    
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
    except Exception as e:
        print ("<<<==============================================")        
        print ("ER: Rate dev not found, loading dummy.")
        print (e)
        print ("==============================================>>>")
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
    except Exception as e:
        print ("<<<==============================================")
        print ("ER: comedi DAQ device not loaded, loading dummy.")
        print (e)
        print ("==============================================>>>")
        class DAQ_Dev(object):
                    def output(self,channel, value): return 0
        data.DAQ_Dev = DAQ_Dev()
        
    try:    
        import lib.er_combivac as combivac
        data.P_Devs.append(combivac.Pressure_Dev())
        #print data.P_Dev.setHV(on=False)
        #print data.P_Dev.getPM()        
    except Exception as e:
        print ("<<<==============================================")
        print ("ER: combivac device not loaded, loading dummy.")
        print (e)
        print ("==============================================>>>")
        class P_Dev(object):
            def getUHV(self): return 1.5e-4+1e-4*sin(time())+random()*3e-5
        data.P_Devs.append(P_Dev())
        
        #data.P_Dev.getPM()
    try:    
        import lib.er_ionivac as ionivac
        data.P_Devs.append(ionivac.Pressure_Dev())
        data.P_Devs[-1].getUHV()
        #print data.P_Dev.setHV(on=False)
        #print data.P_Dev.getPM()
    except Exception as e:
        print ("<<<==============================================")
        print ("ER: ionivac device not loaded, loading dummy.")
        print (e)
        print ("==============================================>>>")
        #except IOError:
        class IP_Dev(object):
            def getUHV(self): return 1.5e-4+1e-4*sin(time())+random()*3e-5
        #data.IP_Dev = IP_Dev()
        # puuuh what a bad hack
        if len(data.P_Devs) == 2:
	    data.P_Devs[1] = IP_Dev()
        else:
            data.P_Devs.append(IP_Dev())
    try:
        import lib.er_ratedev as ratedev
        data.R_Dev=ratedev.Rate_Dev()
        #print rd.getHello()
        #print 'Rate:',rd.getRate()/10
        #print 'Thickness:',rd.getThickness()*100        
    except Exception as e:
        print ("<<<==============================================")
        print ("ER: inficon ratedev device not loaded, loading dummy.")
        print (e)
        print ("==============================================>>>")
        class Rate_Dev(object):
                    def getRate(self,nm=False): return random()*10
                    def getThickness(self,nm=False): return random()*100
        data.R_Dev = Rate_Dev()
        # print 'Rate:',data.R_Dev.getRate(nm=True)
        # print 'Thickness:',data.R_Dev.getThickness(nm=True) 
       
    try:
        import lib.er_HP_5350 as ratedev
        data.R_Dev = ratedev.Frequency_Counter_Dev()
        print "HP 5350 frequency counter loaded"
    except Exception as e:
        print ("<<<==============================================")
        print ("ER: HP5350 Frequency counter device not loaded, loading dummy.")
        print (e)
        print ("==============================================>>>")
        class Rate_Dev(object):
                    def getRate(self,nm=False): return random()*10
                    def getThickness(self,nm=False): return random()*100
        data.R_Dev = Rate_Dev()

    try:
        import lib.er_lakeshore as resdev
        data.Res_Dev = resdev.Lakeshore_340()
        print "HP 5350 frequency counter loaded"
    except Exception as e:
        print ("<<<==============================================")
        print ("ER: Lakeshore 340 device not loaded, loading dummy.")
        print (e)
        print ("==============================================>>>")
        class Res_Dev(object):
                    def getR(self,chan="A"): print("getR"); return random()*10
                    def getT(self,chan="A"): return random()*100
        data.Res_Dev = Res_Dev()
    try:
        import lib.er_aja_dcxs750 as spdev
        data.SP_Dev = spdev.DCXS_Dev()
        print "AJA DCXS750 sputter power supply loaded"
    except Exception as e:
        print ("<<<==============================================")
        print ("ER: AJA DCXS750 sputter device not loaded, loading dummy.")
        print (e)
        print ("==============================================>>>")
        class SP_Dev(object):
                    def setStatus(self,status=True): print(status); return True
        data.SP_Dev = SP_Dev()

    ER = EvapoRate(data=data)

    #ER.edit_traits(view='plots_view')
    ER.configure_traits()
