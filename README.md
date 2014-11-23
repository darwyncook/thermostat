thermostat
==========

The code implements a class for a temperature reading from a DS18B20. Instantiating the class will read a temperature from the sensor. If the read fails it will continue trying to read the sensor until it reaches a timeout, which is set as a class attribute in the TemperatureReadError class.

The sensors are listed as directories. Currently there is one sensor listed as thermo1. You will have to go to your sys/bus/w1/devices/ directory to find the name of your sensors. A dictionary of rooms with the sensors as keys is maintained.

The temperature class records the sensor, the time, and the temperature in celsius and fahrenheit.
