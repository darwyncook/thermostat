__author__ = 'cook'
import os
import datetime


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


class TemperatureReadError(ValueError):
    pass


class Temperature:
    """ __init__ will attempt to read the temperature sensor for half an hour, then it raises an error
    """
    def __init__(self, temp_sensor, zones):  # start_time should be the time in seconds
        self.celcius = -90
        self.fahrenheit = -90
        self.time = ''
        self.sensor = temp_sensor
        try:
            self.sensor_location = zones[self.sensor][0]
            self.read_temp()
        except KeyError:
            raise TemperatureReadError

    def read_temp(self):
        try:
            sensor_file = 'sys/bus/w1/devices/' + self.sensor + '/w1_slave'
            with open(sensor_file, 'r+', encoding='utf-8') as temp_sensor:
                temps = temp_sensor.readlines()
                print('In the read_temp procedure\n', temps)
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
                # value error if the temp can't be converted to float, index error if the read file
                # didn't read enough lines from the file, IOError and FileNotFoundError are the same
                # but for different versions of Python
        except (ValueError, IndexError, IOError):
                print('There was a problem with the file\n')
                raise TemperatureReadError

    def __str__(self):
        return 'The temperature in ' + self.sensor_location + ' at ' + str(self.time) + ' was ' +\
               str(self.fahrenheit)

    def write_temp(self, db):
        pass  # write the temp out to a database
