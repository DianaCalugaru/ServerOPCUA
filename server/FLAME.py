import RPi.GPIO as GPIO


def FunctionFlameSenzor(FLAME_SENSOR_PIN, FlameValue):
    if GPIO.input(FLAME_SENSOR_PIN):
        print("Nicio flacară detectată")
        FlameValue.set_value(0)
    else:
        print("Flacară detectată!")
        FlameValue.set_value(1)
