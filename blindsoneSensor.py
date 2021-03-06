import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

print "Distance Measurement under progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)

print "Waiting For Sensor..."

time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00002)
GPIO.output(TRIG, False)

while GPIO.input(ECHO)==0:
	pulseStart = time.time()

while GPIO.input(ECHO)==1:
	pulseEnd = time.time()

pulseDuration = pulseEnd - pulseStart

distance = pulseDuration * 17150

distance = round(distance, 2)

print "Distance:",distance,"cm"

GPIO.cleanup()