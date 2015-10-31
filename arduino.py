#!/usr/bin/env python
import minimalmodbus
import time

class arduino:
	def modbus(self, relays, cmd):
		while True:
			try:
				arduino = minimalmodbus.Instrument('/dev/ttyACM0', 1) # port name, slave address (in decimal)
				arduino.serial.baudrate = 115200   # Baud
				arduino.serial.bytesize = 8
				arduino.serial.stopbits = 1
				arduino.serial.timeout  = 0.2   # seconds

				while True:
					try:
						array1 = arduino.read_registers(0, 25, 3) # Registernumber, number of decimals
						array2 = arduino.read_registers(25, 25, 3) # Registernumber, number of decimals
						for i in range(25):
							relays[i+25] = array2[i]
							array1[i] = relays[i] 
						time.sleep(0.1)
						arduino.write_registers(0, list(array1))
						arduino.write_registers(25, list(array2))
						time.sleep(0.2)
						cmd[1] = True	
					except IOError:
						print ("Communication error. no answer")
						cmd[1] = False	
						time.sleep(0.5)
					except ValueError:
						print "ValueError: checksum"
						cmd[1] = False			
						time.sleep(0.5)
			except OSError:
				print "No arduino"
				cmd[1] = False	
				time.sleep(0.5)
