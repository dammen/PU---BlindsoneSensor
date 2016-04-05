# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

class Sensor():
	def __init__(self, trig, echo):
		self.TRIG = trig
		self.ECHO = echo
	def setup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.TRIG, GPIO.OUT)
		GPIO.setup(self.ECHO, GPIO.IN‬)
		GPIO.output(self.TRIG, False)
		print("Waiting for sensor to settle")
		time.sleep(2)

	def sendActivationPulse(self):
		GPIO.output(self.TRIG, True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG, False)
		while GPIO.input(self.ECHO)==0:
			self.pulse_start=time.time()
		while GPIO.input(self.ECHO)==1:
		self.pulse_end=time.time()

	def getValue(self):
		value = self.pulse_end - self.pulse_start
		self.pulse_end = 0
		self.pulse_start = 0
		return value*17150

	def reset(self):
		GPIO.cleanup()

	def update(self):
		self.sendActivationPulse()


class Led():
	def __init__(self):
		self.leftLed = 8
		self.inputLed = 7
		GPIO.setup(self.inputLed, GPIO.IN)
		GPIO.setup(self.leftLed, GPIO.OUT)

	def on(self):
		GPIO.output(self.leftLed, GPIO.HIGH)

	def off(self):
		GPIO.output(self.leftLed, GPIO.LOW)

	def isOn(self):
		if GPIO.input‬(self.inputLed):
			print("light is on")
			return True
		else:
			print("light is of")
			return False


class Controller():
	def __init__(self):
		‪#‎Sensor‬
		trig1 = 23
		echo1 = 24
		trig2 = 14
		echo2 = 15
		self.sensor1 = Sensor(trig1, echo1)
		self.sensor1.setup()
		self.distance1 = 0
		self.sensor2 = Sensor(trig2, echo2)
		self.sensor2.setup()
		self.distance2 = 0

		‪#‎LED‬
		self.led = Led()

	def getSensorValue(self, sensor):
		return sensor.getValue()

	def getLedStatus(self):
		return self.led.isOn()

	def setLedStatus(self, activate):
		if activate:
			self.led.on()
		else:
			self.led.off()

	def setDistance(self):
		self.distance1 = self.computeDistance(self.getSensorValue(self.sensor1))
		self.distance2 = self.computeDistance(self.getSensorValue(self.sensor2))

	def getDistance(self, string):
		if string:
			return ("Distance sensor 1: " + str(self.distance1) + " cm." + "\n" + "Distance sensor 2: " + str(self.distance2) + " cm.")
		else:
			return (self.distance1, self.distance2)

	def computeDistance(self, value):
		return round(value, 2)

	def update(self):
		self.sensor1.update()
		self.sensor2.update()

class Handler() :
	def __init__(self):
		self.controller = Controller()

	def considerActivation(self):
	‪	#‎legg‬ til algoritme for kalkulering av activation
		if self.getDistance()< 20:
			self.fireAlarm(True)
		else:
			self.fireAlarm(False)

	def considerDeactivation(self):
		if self.getDistance()> 10:
			self.fireAlarm(False)
		else:
			self.fireAlarm(True)

	def getDistance(self):
		self.update()
		v1, v2 = self.controller.getDistance(False)
		print ("Distance 1:" + str(v1))
		print( "distance 2:" + str(v2))
		return(v1 + v2)

	def fireAlarm(self, activate):
		if activate:
			if not(self.controller.getLedStatus()):
				self.controller.setLedStatus(True)
			print("lys")
		else:
			if (self.controller.getLedStatus()):
				self.controller.setLedStatus(False)
			print("mørkt")

	def update(self):
		self.controller.update()
		self.controller.setDistance()

class Main():
	def __init__(self):
		self.c = Handler()
		self.run()

	def run(self):
		active = True
		while active:
			for i in range(10):
				self.c.considerActivation()
				time.sleep(0.5)

			input_var = raw_input("To continue enter <y>. To exit enter <q>")
			print("you entered: "+ input_var)
			while (not input_var == "y") and (not input_var == "q"):
				print("Not valid argument")
				input_var = raw_input("To continue enter <y>. To exit enter <q>")
				print("you entered: "+ input_var)

			if input_var == "y":
				active = True
			else:
				active = False
				
		print("you succesfully exited...")
Main()