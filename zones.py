__author__ = 'cook'
from sensor import *


class Zone:
    def __init(self, sensor, zones_dict):
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