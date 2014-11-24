__author__ = 'cook'
import time
from zones import *


thermo1 = '28-0000065bb6cd'

# The second entry in the value list should be the GPIO pin the zone is connected to
zones = {thermo1: ['whole house', 10]}
time_out = 30*60  # half an hour in seconds
zone = {}

# If there is an error reading the temperature send an error message.
def send_error(sensor,zones):
    print('There was an error in ' + zones[sensor][0])

for sensor in zones:
    zone[sensor] = Zone(sensor, zones)

while True:
    try:
        for sensor in zones:
            zone[sensor].get_current_temp()
            zone[sensor].write_temp_db()
            print(zone[sensor].temp)
        time.sleep(60)
    except TemperatureReadError:
        send_error(TemperatureReadError.sensor,zones)
        time.sleep(0.2)