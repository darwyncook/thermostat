__author__ = 'cook'
from sensor import *

# sensor is a string with the file name for the sensor from modprobe
# zones_dict has sensor as a key, the value is a list with a zone desciption string and the GPIO pin the zone is
# connected to.
class Zone:
    def __init__(self, sensor, zones_dict):
        self.GPIO = zones_dict[sensor][1]
        self.switch = None
        self.temp = Temperature(sensor, zones_dict)
        self.goal = self.read_goal()

    def get_current_temp(self):
        self.temp.read_temp()

    def thermostat(self):
        if self.temp > self.goal:
            self.set_zone('off')
        else:
            self.set_zone('on')

    def read_goal(self):
        return 0

    def set_zone(self, OnOff):
        pass