import serial

class Lakeshore_340:
    def __init__(self):
        
        self.con = serial.Serial(port='/dev/ttyUSB5', baudrate=9600, 
	#parity=serial.PARITY_ODD, 
	#stopbits=serial.STOPBITS_ONE, 
	#bytesize=serial.SEVENBITS, 
	timeout=1)
        self.channel_names = ['A','B'] 

    def get_temps(self):
	for chan in self.channel_names:
		self.con.write('KRDG? %s\r\n'%(chan))
		print(self.con.readline())
		self.con.write('SRDG? %s\r\n'%(chan))
		print(self.con.readline())


if __name__ == "__main__":
	tc =Lakeshore_340()
	tc.get_temps()
