from opcua import Server
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import cv2

from LED import FunctionLedOn, FunctionLedOff, FunctionLedOnOff
from DHT11 import FunctionDHT
from FLAME import FunctionFlameSenzor
from SOUND import handle_sound
from SWITCH import handle_switch

DHT_SENSOR = Adafruit_DHT.DHT11
FLAME_SENSOR_PIN = 16
LED1_PIN = 27
LED2_PIN = 17
LED3_PIN = 26
LED4_PIN = 13
LED5_PIN = 19
SOUND_PIN = 12
SWITCH_PIN = 23
DHT_PIN = 4

server = Server()
url = "opc.tcp://169.254.15.16:4840"
server.set_endpoint(url)

name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Led = node.add_object(addspace, "Led")
DHT = node.add_object(addspace, "DHT")
FlameSensor = node.add_object(addspace, "FlameSensor")
SoundSensor = node.add_object(addspace, "SoundSensor")
Switch = node.add_object(addspace, "Switch")
cam_node = node.add_object(addspace, "Camera")


Led1 = Led.add_variable(addspace, "Led1", 0)
Led2 = Led.add_variable(addspace, "Led2", 0)
Led3 = Led.add_variable(addspace, "Led3", 0)
Led4 = Led.add_variable(addspace, "Led4", 0)
Led5 = Led.add_variable(addspace, "Led5", 0)

DHT_temperature = DHT.add_variable(addspace, "temperature", 0)
DHT_humidity = DHT.add_variable(addspace, "humidity", 0)
FlameValue = FlameSensor.add_variable(addspace, "FlameValue", 0)
SoundValue = SoundSensor.add_variable(addspace, "SoundValue", 0)
SwitchValue = Switch.add_variable(addspace, "Switch", 0)
camera_variable = cam_node.add_variable(addspace, "Camera", 0)

Led1.set_writable()
Led2.set_writable()
Led3.set_writable()
Led4.set_writable()
Led5.set_writable()
FlameValue.set_writable()
SoundValue.set_writable()
SwitchValue.set_writable()

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_SENSOR_PIN, GPIO.IN)
GPIO.setup(SOUND_PIN, GPIO.IN)
GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)
GPIO.setup(LED3_PIN, GPIO.OUT)
GPIO.setup(LED4_PIN, GPIO.OUT)
GPIO.setup(LED5_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

server.start()

	
def handle_sound_wrapper(channel):
    handle_sound(channel, SOUND_PIN, SoundValue)		
              
# Adăugare eveniment pentru detectarea modificărilor pe pinul senzorului de sunet
GPIO.add_event_detect(SOUND_PIN, GPIO.BOTH, callback= handle_sound_wrapper)

def handle_switch_wrapper(channel):
    handle_switch(channel, SWITCH_PIN, SwitchValue, camera_variable)		            

# Adăugare eveniment pentru detectarea modificărilor pe pinul de comutare
GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=handle_switch_wrapper)


print("Server started at {}".format(url))

try:
	while True:
		FunctionLedOn(Led1, LED1_PIN)
		FunctionLedOn(Led2, LED2_PIN)
		FunctionLedOn(Led3, LED3_PIN)
		FunctionLedOn(Led4, LED4_PIN)
		FunctionLedOnOff(Led5, LED5_PIN)
		FunctionDHT(DHT_SENSOR, DHT_PIN, DHT_temperature, DHT_humidity)
		FunctionFlameSenzor(FLAME_SENSOR_PIN, FlameValue)
		time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()


