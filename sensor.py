import RPi.GPIO as GPIO
import time

class Sensor():

    def __init__(self):
        self.TRIG = 23
        self.ECHO = 24

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
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


class Controller():

    def __init__(self):
        self.sensor = Sensor()
        self.sensor.__init__()
        self.sensor.setup()
        self.distance = 0

    def getSensorValue(self):
        return self.sensor.getValue()

    def getLedStatus(self):
        pass

    def setLedStatus(self):
        pass

    def setDistance(self):
        self.distance = self.computeDistance(self.getSensorValue())

    def getDistance(self):
        return "Distance: " + str(self.distance) + " cm."

    def computeDistance(self, value):
        return round(value, 2)

    def update(self):
        self.sensor.update()

c = Controller()
for i in range(10):
    c.update()
    c.setDistance()
    print(c.getDistance())
    time.sleep(0.5)
