#!/usr/bin/env python
import minimalmodbus
import time

def log(text):
	print text

class arduino:
	def __init__(self, status):
		self.stat = status		
		try:
			self.arduino = minimalmodbus.Instrument('/dev/ttyACM0', 1) # port name, slave address (in decimal)
			self.arduino.serial.baudrate = 115200   # Baud
			self.arduino.serial.bytesize = 8
			self.arduino.serial.stopbits = 1
			self.arduino.serial.timeout  = 0.2   # seconds
		except OSError:
			log("No arduino")
			status['arduino'] = 0	
			time.sleep(0.5)
	def write(self):
		try:
			#array1 = arduino.read_registers(0, 26, 3) # Registernumber, number of decimals
			array = self.arduino.read_registers(26, 26, 3) # Registernumber, number of decimals
			for i in range(26):
				#relays[i+25] = array2[i]
				array[i] = self.stat['relay'][i] 
			time.sleep(0.1)
			self.arduino.write_registers(0, list(array))
			#arduino.write_registers(26, list(array2))
			self.stat['arduino'] = 1	
		except ValueError:
			log("ValueError: checksum")
			self.stat['arduino'] = 0	
			time.sleep(0.5)
		except:
			log("Communication error. no answer")
			self.stat['arduino'] = 0
			time.sleep(0.5)
