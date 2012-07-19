# IO DEV version 0.1 written by HR@KIT 2012

try:
  from pycomedi.device import Device
  from pycomedi.channel import AnalogChannel
  from pycomedi.constant import SUBDEVICE_TYPE, AREF, UNIT
except:
  print("pycomedi failed to load")

class IO_Dev(object):
  def __init__(self):
    self.device = Device('/dev/comedi0')
    self.device.open()

  def close(self):
    # Close the device when you're done.
    self.device.close()

  def configure_ai(self):
    """
    Get your I/O subdevice (alternatively, use `device.subdevice()` to
    select the subdevice directly by index).
    """
    subdevice = self.device.find_subdevice_by_type(SUBDEVICE_TYPE.ai)
    # Generate a list of channels you wish to control.

    channels = [subdevice.channel(i, factory=AnalogChannel, aref=AREF.diff) for i in (0, 1, 2, 3)]

    # Configure the channels.

    for chan in channels:
      chan.range = chan.find_range(unit=UNIT.volt, min=0, max=5)

    self.ai_converters = [c.get_converter() for c in channels]
    
  def configure_ao(self):
     """
     Get your I/O subdevice (alternatively, use `device.subdevice()` to
     select the subdevice directly by index).
     """
     self.ao_subdevice = self.device.find_subdevice_by_type(SUBDEVICE_TYPE.ao)
     # Generate a list of channels you wish to control.

     self.ao_channels = [self.ao_subdevice.channel(i, factory=AnalogChannel, aref=AREF.diff) for i in (0, 1)]
     #for chan in channels: print chan
     # Configure the channels.

     for chan in self.ao_channels:
       chan.range = chan.find_range(unit=UNIT.volt, min=0, max=5)
      
  def output(self,channel,volt_output_signal):
     channel = self.ao_channels[channel]
     ao_converter = channel.get_converter()
     channel.data_write(ao_converter.from_physical(volt_output_signal))
    
  def input(self,channel):
    # Read/write sequentially.

    value = channel.data_read_delayed(nano_sec=1e3)
    print value  
    # Use a converter to convert these to physical values

    return self.ai_converters[channel].to_physical(value)
    # print [c.to_physical(v) for c,v in zip(converters, value)]  # doctest: +SKIP
    # [5.0, 1.787136644541085, 0.0, 0.0]
    # print [c.range.unit for c in channels]
    # [<_NamedInt volt>, <_NamedInt volt>, <_NamedInt volt>, <_NamedInt volt>]



if __name__== '__main__':
   import sys
   # sys.argv[1]
   iod = IO_Dev()
   iod.configure_ao()
   iod.output(0,float(sys.argv[1]))
   #iod.output(1,0)
   iod.close()
    


"""
As a more elaborate test, we can cable AO0 into AI0 and sweep the
voltage.

>>> from numpy import linspace
>>> from scipy.stats import linregress
>>> device.open()
>>> ai_subdevice = device.find_subdevice_by_type(SUBDEVICE_TYPE.ai)
>>> ao_subdevice = device.find_subdevice_by_type(SUBDEVICE_TYPE.ao)
>>> ai_channel = ai_subdevice.channel(0, factory=AnalogChannel, aref=AREF.diff)
>>> ao_channel = ao_subdevice.channel(0, factory=AnalogChannel, aref=AREF.diff)
>>> ai_channel.range = ai_channel.find_range(unit=UNIT.volt, min=0, max=10)
>>> ai_channel.range
<Range unit:volt min:0.0 max:10.0>
>>> ao_channel.range = ao_channel.find_range(unit=UNIT.volt, min=0, max=10)
>>> ao_channel.range
<Range unit:volt min:0.0 max:10.0>
>>> ao_maxdata = ao_channel.get_maxdata()
>>> ai_maxdata = ai_channel.get_maxdata()
>>> ao_start = 0.3 * ao_maxdata
>>> ao_stop = 0.7 * ao_maxdata
>>> points = 10
>>> ao_data = linspace(ao_start, ao_stop, points)
>>> ai_data = []
>>> for i in range(points):
...     ao_channel.data_write(ao_data[i])
...     ai_data.append(ai_channel.data_read_delayed(nano_sec=10e3))
>>> ao_converter = ao_channel.get_converter()
>>> ai_converter = ai_channel.get_converter()
>>> ao_data = ao_converter.to_physical(ao_data)
>>> ai_data = ao_converter.to_physical(ai_data)
>>> ao_data
array([ 2.9999237 ,  3.44441901,  3.88876173,  4.33325704,  4.77775235,
        5.22209506,  5.66659037,  6.11108568,  6.5554284 ,  6.9999237 ])
>>> ai_data  # doctest: +SKIP
array([ 3.0156405 ,  3.46089876,  3.90630961,  4.35156786,  4.79682612,
        5.24238956,  5.687953  ,  6.13351644,  6.57862211,  7.02433814])
>>> scaled_ao_data = [d/float(ao_maxdata) for d in ao_data]
>>> scaled_ai_data = [d/float(ai_maxdata) for d in ai_data]
>>> gradient,intercept,r_value,p_value,std_err = linregress(
...     scaled_ao_data, scaled_ai_data)
>>> abs(gradient - 1.0) < 0.01
True
>>> abs(intercept) < 0.001
True
>>> r_value > 0.999
True
>>> p_value < 1e-14
True
>>> std_err < 1e-4
True
>>> device.close()
"""
