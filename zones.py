__author__ = 'cook'
from sensor import *
import RPIO as GPIO

# sensor is a string with the file name for the sensor from modprobe
# zones_dict has sensor as a key, the value is a list with a zone desciption string and the GPIO pin the zone is
# connected to.
class Zone:
    def __init__(self, sensor, zones_dict):
        try:
            self.sensor = sensor
            self.zone_name = zones_dict[sensor][0]
            self.GPIO = zones_dict[self.sensor][1]
            self.switch = None
            self.temp = Temperature(sensor)
            self.goal = self.read_goal()
            GPIO.setup(self.GPIO, GPIO.OUT)
        except KeyError:
            raise TemperatureReadError

    def __str__(self):
        return self.zone_name + ' was ' + str(self.temp) + ' at ' + str(self.temp.time)

    def get_current_temp(self):
        self.temp.read_temp()

    def thermostat(self):
        self.get_current_temp()
        try:
            self.goal = self.read_goal()
        except TemperatureReadError:
            raise
        if self.temp > self.goal: # this could be more complicated
            self.set_zone('off')
        else:
            self.set_zone('on')

    def set_zone(self, onoff):
        if onoff == 'on':
            GPIO.output(self.GPIO,1)
        else:
            GPIO.output(self.GPIO,0)

    def read_goal(self):
        with open(self.sensor+'.txt', 'r', encoding='utf-8') as f:
            try:
                temp = f.readline()
                temp = temp.rstrip('\r\n')
                return float(temp)
            except ValueError:
                raise TemperatureReadError

    def write_temp_db(self, db):
        ##    tdate - datetime
        ##    ttime - datetime
        ##    sensor - which is a string
        ##    zone - string
        ##    celcius - Number
        ##    fahrenheit - Number
        cursor = db.cnx.cursor()
        add_temp = ("INSERT INTO temps " "(tdate, ttime, sensor, zone, celcius, fahrenheit)"
                    "VALUES(%s, %s, $s, %s, %s, %s)")
        temp_data = (self.temp.time.date, self.temp.time.time, self.sensor, self.sensor_location,
                     self.temp.celcius, self.temp.fahrenheit)
        cursor.execute(add_temp, temp_data)