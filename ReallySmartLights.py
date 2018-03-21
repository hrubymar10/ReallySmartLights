#!/usr/bin/env python3
"""
ReallySmartLights.py
"""

from datetime import datetime, timedelta
import ephem
import json
from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json
import socket
import sys
import time
import uuid

__author__ = "Martin Hrubý (hrubymar10)"
__copyright__ = "Copyright 2017-2018, Martin Hrubý (hrubymar10)"
__credits__ = [""]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Martin Hrubý (hrubymar10)"
__status__ = "Beta"

######################### CONFIG #########################
__DEBUG__ = True
__verbosity__ = 2

time_diff = 102 # Default: 102
min_light = 4540 # Default: 4540
max_light = 2500 # Default: 2500

city = "" # Enter here name of city where do you live.

force_RSL_values = False # Do you want force RSL values during day and night?

bulbs = [1, 2] # id or ids of bulbs

IP = "" # IP address of your IKEA Trådfri gateway
key = "" # Security key of your IKEA Trådfri gateway

#### Fill these informations after first run ####
identity = ""
psk = ""
#### /Fill these informations after first run ####

######################### /CONFIG #########################

observer = ephem.Observer()
observer.lon = ephem.city(city).lon
observer.lat = ephem.city(city).lat

expected_state = {}
last_expected_state_problem = datetime.today() - timedelta(days=1)


def is_valid_ip_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return is_valid_ipv6_address(address)

    return True

def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True

def convert_to_temp(temp_value):
    return (((102 - (temp_value - 250)) + 102) + 250) * 10

def convert_to_temp_value(temp):
    #TODO: make this work
    return 0

def genPSK():
    identity = uuid.uuid4().hex

    try:
        psk = APIFactory(host=IP, psk_id=identity).generate_psk(key)
        print('Generated identity: ', identity)
        print('Generated PSK: ', psk)
        print('Please add these to your config...')
    except AttributeError:
        raise PytradfriError("You provided bad key")
    sys.exit()

def initialize():
    if len(key) != 16:
        raise PytradfriError("Invalid Security Code 'key' provided.")
    
    if not is_valid_ip_address(IP):
        raise PytradfriError("Invalid IP Address 'IP' provided.")

    if identity == "" or psk == "":
        genPSK()

    for bulb in bulbs:
        expected_state[bulb] = {"temp":250, "brightness":10}

def change_temp(api, lights, bulb, diff):
    value = int(454 - (diff * (204 / time_diff)))
    if __DEBUG__:
        print("DEBUG: diff:", diff, " ; expected_value:",expected_state[bulb]["temp"], " ; new_value:", value)
        print("Setting temp to: ", int(convert_to_temp(value)), "K")
    expected_state[bulb] = {"temp":value}
    api(lights[bulb].light_control.set_color_temp(value))

def main():
    if __DEBUG__:
        print("")
        print("#####")
        print("")
    api = APIFactory(host=IP, psk_id=identity, psk=psk).request
    gateway = Gateway()

    #TODO: Add simulation option
    #devices_commands = ""
    #devices = ""
    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)

    lights = [dev for dev in devices if dev.has_light_control]

    #TODO: Add simulation option
    time_now = datetime.now()
    #time_now = datetime(2018, 3, 12, 15, 0, 0)
    observer.date = time_now
    sunrise = observer.previous_rising(ephem.Sun())
    sunset = observer.next_setting(ephem.Sun())

    if sunrise < observer.date and not observer.next_rising(ephem.Sun()) > sunset:
        sunrise = observer.next_rising(ephem.Sun())
        if __DEBUG__:
            print("Corrected sunrise")

    while True:
        #TODO: Add simulation option
        time_now = datetime.now()
        observer.date = time_now

        if __DEBUG__:
            print("time: ", time_now)
            print("sunrise: ", sunrise.datetime())
            print("sunset: ", sunset.datetime())
            print("")

        if sunrise <= observer.date <= sunset:
            sunrise_minutes_diff = int((time_now - sunrise.datetime()).seconds / 60)
            sunset_minutes_diff = int((sunset.datetime() - time_now).seconds / 60)

            if sunrise_minutes_diff <= time_diff:
                if __DEBUG__:
                    print("it's sunrise now")
                    print("")
                for bulb in bulbs:
                    change_temp(api, lights, bulb, sunrise_minutes_diff)
            elif sunset_minutes_diff <= time_diff:
                if __DEBUG__:
                    print("it's sunset now")
                    print("")
                for bulb in bulbs:
                    change_temp(api, lights, bulb, sunset_minutes_diff)
            else:
                if __DEBUG__:
                    print("it's day now")
                    print("")
                if force_RSL_values:
                    for bulb in bulbs:
                        change_temp(api, lights, bulb, time_diff)
        else:
            if __DEBUG__:
                print("it's night now")
            if force_RSL_values:
                for bulb in bulbs:
                    #TODO:
                    change_temp(api, lights, bulb, 0)
            sunrise = observer.next_rising(ephem.Sun())
            sunset = observer.next_setting(ephem.Sun())
        
        if __DEBUG__:
            print("")
            print("#####")
            print("")

        #TODO: Add simulation option
        #time_now = time_now + timedelta(minutes=1)
        time.sleep(5)

initialize()
main()
