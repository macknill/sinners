def log(text):
	print text

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    log("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
import time


class RPi:	
	def __init__(self, status_class):
		self.status = status_class
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		log("Init Rsapberry Pi inputs")
		for i in range(1,27):
			GPIO.setup(i, GPIO.IN)
			self.status["rpi"][i-1] = GPIO.input(i)
		log("Raspberry Pi2 inputs init")
	def read(self):
		try:
			for i in range(1,27):
				self.status["rpi"][i-1] = GPIO.input(i)
		except IOError:
			 log("RPi inputs read error")

