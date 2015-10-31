def log(text):
	print text

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    log("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
import time


class RPiO:
	def read(self, inputs):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		log("Init Rsapberry Pi inputs")
		for i in range(1,26):
			GPIO.setup(i, GPIO.IN)
			inputs[i-1] = GPIO.input(i)
		log("Start read inputs state")
		while True:
			try:
				for i in range(1,26):
					inputs[i-1] = GPIO.input(i)
			except IOError:
				 log("File error")
			time.sleep(0.2)

