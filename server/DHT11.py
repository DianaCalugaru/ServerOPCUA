import RPi.GPIO as GPIO
import Adafruit_DHT

def FunctionDHT(DHT_SENSOR, DHT_PIN, DHT_temperature,DHT_humidity):
	humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
	if humidity is not None and temperature is not None:
		DHT_temperature.set_value(temperature)
		DHT_humidity.set_value(humidity)
		print("Temperature: {:.2f} C, Humidity: {:.2f} %".format(temperature, humidity))
	else:
		print("Failed to read data from DHT11 sensor")



