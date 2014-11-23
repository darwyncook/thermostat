__author__ = 'cook'
import os
import time
import datetime

thermo1 = 'sys/bus/w1/devices/28-0000065bb6cd/w1_slave'
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

rooms = {thermo1: 'living room'}


class TemperatureReadError(ValueError):
    time_out = 60*30  # half an hour in seconds.
    pass


class Temperature:
    """ __init__ will attempt to read the temperature sensor for half an hour, then it raises an error
    """
    def __init__(self, temp_sensor, start_time):  # start_time should be the time in seconds
        global rooms
        self.celcius = -90
        self.fahrenheit = -90
        self.time = ''
        self.sensor = temp_sensor
        self.sensor_location = rooms[self.sensor]
        try:
            self.read_temp()
        except TemperatureReadError:
            current_time = time.clock()
            if current_time - start_time > TemperatureReadError.time_out:  # half an hour
                raise TemperatureReadError
            else:
                self.read_temp()

    def read_temp(self):
        try:
            with open(self.sensor, 'r+', encoding='utf-8') as temp_sensor:
                temps = temp_sensor.readlines()
                temps[0] = temps[0].rstrip('\r\n')
                temps[1] = temps[1].rstrip('\r\n')
                if 'YES' not in temps[0]:
                    raise TemperatureReadError
                temps[1] = temps[1].strip()
                temp_position = temps[1].find('t=')
                if temp_position != -1:  # string not found
                    self.celcius = float(temps[1][temp_position+2:])/1000
                    self.fahrenheit = self.celcius*9/5+32.0
                    self.time = datetime.datetime.now()
                else:
                    raise TemperatureReadError
        except:
                raise TemperatureReadError

    def __str__(self):
        return 'The temperature in ' + self.sensor_location + ' at ' + self.time + ' was ' + str(self.fahrenheit)

    def write_temp(self, db):
        pass  # write the temp out to a database


def send_error():
    pass

while True:
    try:
        current_temp = Temperature(thermo1)
        print(current_temp)
    except TemperatureReadError:
        send_error()
