__author__ = 'cook'

from zones import *

GPIO = 1
thermo1 = '28-0000065bb6cd'

# The second entry in the value list should be the GPIO pin the zone is connected to
zones = {thermo1: ['whole house', 10]}
time_out = 30*60  # half an hour in seconds


# If there is an error reading the temperature send an error message.
def send_error():
    pass


zone1 = Zone(thermo1, zones[thermo1][GPIO], zones)
while True:
    start_attempt_time = time.time()
    try:
        zone1.get_current_temp()
        print(zone1.temp)
    except TemperatureReadError:
        time.sleep(0.2)
        print("In the while loop - read error occured")