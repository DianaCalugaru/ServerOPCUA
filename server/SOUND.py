import RPi.GPIO as GPIO
import time

# Funcție pentru tratarea evenimentului de detectare a sunetului
def handle_sound(channel, SOUND_PIN, SoundValue):
    if GPIO.input(SOUND_PIN):
        print("Sunet detectat!")
        SoundValue.set_value(1)  # Setare valoare OPC UA la 1
        time.sleep(1)
    else:
        SoundValue.set_value(0)  # Setare valoare OPC UA la 0
