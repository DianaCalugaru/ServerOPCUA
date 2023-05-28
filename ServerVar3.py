
from opcua import Server
import RPi.GPIO as GPIO
import Adafruit_DHT
from random import randint
import datetime
import time

DHT_SENSOR = Adafruit_DHT.DHT11
FLAME_SENSOR_PIN = 16
DHT_PIN = 4
LED1_PIN = 27
LED2_PIN = 17
LED3_PIN = 26
LED4_PIN = 13
LED5_PIN = 19


server = Server()
url = "opc.tcp://169.254.15.16:4840"
server.set_endpoint(url)

name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Led = node.add_object(addspace, "Led")
Led1 = Led.add_variable(addspace, "Led1", 0)
Led2 = Led.add_variable(addspace, "Led2", 0)
Led3 = Led.add_variable(addspace, "Led3", 0)
Led4 = Led.add_variable(addspace, "Led4", 0)
Led5 = Led.add_variable(addspace, "Led5", 0)

DHT = node.add_object(addspace, "DHT")
DHT_temperature = DHT.add_variable(addspace, "temperature", 0)
DHT_humidity = DHT.add_variable(addspace, "humidity", 0)

Led1.set_writable()
Led2.set_writable()
Led3.set_writable()
Led4.set_writable()
Led5.set_writable()


GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_SENSOR_PIN, GPIO.IN)
GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)
GPIO.setup(LED3_PIN, GPIO.OUT)
GPIO.setup(LED4_PIN, GPIO.OUT)
GPIO.setup(LED5_PIN, GPIO.OUT)


server.start()

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
    time.sleep(4)
    GPIO.output(Pin, GPIO.LOW)
    LedVar = 0
    print(LedVar)
    Led.set_value(LedVar)
    time.sleep(4)
def FunctionFlameSenzor(FLAME_SENSOR_PIN):
    if GPIO.input(FLAME_SENSOR_PIN):
        print("Nicio flacara detectata")
    else:
        print("Flacara detectata!")

    # Asteapta 0.1 secunde pana la urmatoarea citire
    time.sleep(0.1)
    
def FunctionDHT(DHT_SENSOR, DHT_PIN):
	humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN);
	if humidity is not None and temperature is not None:
		DHT_temperature.set_value(temperature);
		DHT_humidity.set_value(humidity);
		print("Temperature: {:.2f} C, Humidity: {:.2f} %".format(temperature, humidity))
	else:
		print("Failed to read data from DHT11 sensor")
	time.sleep(1)  # Așteaptă 5 secunde înainte de a citi din nou valorile
    


print("Server started at {}".format(url))

try:
    while True:
        FunctionLedOnOff(Led1, LED1_PIN);
        FunctionLedOnOff(Led2, LED2_PIN);
        FunctionLedOn(Led3, LED3_PIN);
        FunctionLedOn(Led4, LED4_PIN);
        FunctionLedOn(Led5, LED5_PIN);
        FunctionDHT(DHT_SENSOR, DHT_PIN);
        FunctionFlameSenzor(FLAME_SENSOR_PIN)
except KeyboardInterrupt:
    GPIO.cleanup()

