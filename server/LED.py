import RPi.GPIO as GPIO
import time


def FunctionLedOn(Led, Pin):
	GPIO.output(Pin, GPIO.HIGH)
	LedVar = 1
	print(LedVar)
	Led.set_value(LedVar)

def FunctionLedOff(Led, Pin):
	GPIO.output(Pin, GPIO.LOW)
	LedVar = 0
	print(LedVar)
	Led.set_value(LedVar)

def FunctionLedOnOff(Led, Pin):
	GPIO.output(Pin, GPIO.HIGH)
	LedVar = 1
	print(LedVar)
	Led.set_value(LedVar)
	time.sleep(2)
   
	GPIO.output(Pin, GPIO.LOW)
	LedVar = 0
	print(LedVar)
	Led.set_value(LedVar)
