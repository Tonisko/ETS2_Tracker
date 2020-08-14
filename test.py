import socket
import json
import time
import psutil
import sys
from math import floor
from pypresence import Presence
from threading import Thread
from json import JSONDecodeError
from colorama import Fore, ansi, init

init(autoreset=True)

# "logging in" - for job logging purposes
try:
    f = open('credentials.json', 'r+')
    _f = f.read()
    j = json.loads(_f)
    print('Logged in!')
    time.sleep(2)
except FileNotFoundError:
    us = input('Please type your Discord tag WITHOUT HASHTAG (ex.: Tonisko5799): ') # Database raises error while creation when there is '#'
    na = input('Please put your nick for statistics: ')
    js = {"username": us, "nick": na}
    j = json.dumps(js)
    f = open('credentials.json', 'w+')
    f.write(j)
    f.close()
    print('Credentials saved!')
    time.sleep(1)
    f = open('credentials.json', 'r+')
    _f = f.read()
    j = json.loads(_f)
    print('Logged in!')
    time.sleep(1)

user = j["username"]
_name = j["nick"]
d = {}


def is_running(name): # Checks for running game
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if pinfo["name"] == name:
                return True
    return False


print(Fore.GREEN + f'Welcome, {_name}!')
time.sleep(2)

while True: # Checking which game is running and attempting to connect to the plugin
    if is_running("eurotrucks2.exe"):
        print(ansi.clear_screen())
        print(Fore.GREEN + 'ETS2 detected! Checking plugin...')
        time.sleep(2)
        try:
            s = socket.socket()
            s.connect(('127.0.0.1', 30001))
            data = s.recv(20000).decode('utf-8')[8:]
            d = json.loads(data)
            time.sleep(1)
            break
        except Exception as e:
            print(e)
            print('Plugin not loaded yet, refreshing...')
    elif is_running("amtrucks.exe"):
        print(Fore.GREEN + 'ATS detected! Checking plugin...')
        try:
            s = socket.socket()
            s.connect(('127.0.0.1', 30001))
            data = s.recv(20000).decode('utf-8')[8:]
            d = json.loads(data)
            time.sleep(1)
            break
        except:
            print('Plugin not loaded yet, refreshing...')
    else:
        print(ansi.clear_screen())
        print(Fore.RED + "No game detected /:\\")
        for i in reversed(range(0, 6)):
            time.sleep(1)
            print("Checking again in: " + Fore.YELLOW + str(i))


def refresh(): # Base for getting info from plugin
    global d
    global s
    index = 0
    while True:
        try:
            data = s.recv(20000).decode('utf-8')[8:]
            d = json.loads(data)
            time.sleep(1)
            index = 0
        except JSONDecodeError: # If tracker retrieves incomplete JSON from plugin, tries again, as fast as possible. This somehow makes data corrent again.
            if is_running("eurotrucks2.exe"):
                print('Error. Trying again...')
            elif is_running("amtrucks.exe"):
                print('Error. Trying again...')
            else:
                d = {}
                break


def tracker(): # Complete base for job checking and sending
    global d
    while True:
        try:
            while True:
                if d["data"]["jobData"]["status"] is 0:
                    time.sleep(3)
                    print(ansi.clear_screen())
                    print('No job detected, refreshing...')
                if d["data"]["jobData"]["status"] is 1:
                    print(Fore.GREEN + 'Job found!')
                    break

            while True:
                if d["data"]["jobData"]["status"] is 1:
                    time.sleep(3)
                    print(ansi.clear_screen())
                    print('On job, refreshing...')
                if d["data"]["jobData"]["status"] is 2:
                    print(Fore.GREEN + 'Job finished! Sending to API...')
                    timetaken = d["data"]["jobData"]["realTimeTaken"]
                    _time = (timetaken / (1000 * 60)) % 60
                    hrs = (timetaken / (1000 * 60 * 60))
                    _timee = floor(_time)
                    _hrs = floor(hrs)
                    distance = d["data"]["jobData"]["distanceDriven"]
                    cargo = d["data"]["jobData"]["cargo"]
                    source = d["data"]["jobData"]["sourceCity"]
                    sourcec = d["data"]["jobData"]["sourceCompany"]
                    destination = d["data"]["jobData"]["destinationCity"]
                    destinationc = d["data"]["jobData"]["destinationCompany"]
                    g = d["data"]["telemetry"]["game"]["isMultiplayer"]
                    if g is True:
                        game = "Multiplayer"
                    else:
                        game = "Singleplayer"
                    mass = d["data"]["jobData"]["trailerMass"]
                    _mass = round(mass)
                    brand = d["data"]["jobData"]["truckMake"]
                    model = d["data"]["jobData"]["truckModel"]
                    fuel = d["data"]["jobData"]["fuelBurned"]
                    consumption = d["data"]["jobData"]["fuelBurned"] * 100 / distance
                    _distance = round(distance, 1)
                    _consumption = round(consumption, 2)
                    _fuel = round(fuel, 0)
                    wr = {"user": user, "name": _name, "cargo": cargo, "source": "{}, {}".format(source, sourcec),
                          "destination": "{}, {}".format(destination, destinationc),
                          "fuel": _fuel, "consumption": _consumption, "Hours": _hrs, "Minutes": _timee,
                          "distance": _distance,
                          "Game": game, "mass": mass, "Truck": "{} {}".format(brand, model)}
                    w = json.dumps(wr)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(('ip_address', 4564))
                    sock.send(w.encode())
                    sock.close()
                    break

                if d["data"]["jobData"]["status"] is 3:
                    print(Fore.GREEN + 'Job cancelled! Sending to API...')
                    timetaken = d["data"]["jobData"]["realTimeTaken"]
                    _time = (timetaken / (1000 * 60)) % 60
                    hrs = (timetaken / (1000 * 60 * 60))
                    _timee = floor(_time)
                    _hrs = floor(hrs)
                    distance = d["data"]["jobData"]["distanceDriven"]
                    cargo = d["data"]["jobData"]["cargo"]
                    source = d["data"]["jobData"]["sourceCity"]
                    sourcec = d["data"]["jobData"]["sourceCompany"]
                    destination = d["data"]["jobData"]["destinationCity"]
                    destinationc = d["data"]["jobData"]["destinationCompany"]
                    g = d["data"]["telemetry"]["game"]["isMultiplayer"]
                    if g is True:
                        game = "Multiplayer"
                    else:
                        game = "Singleplayer"
                    mass = d["data"]["jobData"]["trailerMass"]
                    _mass = round(mass)
                    brand = d["data"]["jobData"]["truckMake"]
                    model = d["data"]["jobData"]["truckModel"]
                    fuel = d["data"]["jobData"]["fuelBurned"]
                    consumption = d["data"]["jobData"]["fuelBurned"] * 100 / distance
                    _distance = round(distance, 1)
                    _consumption = round(consumption, 2)
                    _fuel = round(fuel, 0)
                    wr = {"user": user, "name": _name, "cargo": cargo, "source": "{}, {}".format(source, sourcec),
                          "destination": "{}, {}".format(destination, destinationc),
                          "fuel": _fuel, "consumption": _consumption, "Hours": _hrs, "Minutes": _timee,
                          "distance": _distance,
                          "Game": game, "mass": mass, "Truck": "{} {}".format(brand, model)}
                    w = json.dumps(wr)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(('ip_address', 4564))
                    sock.send(w.encode())
                    sock.close()
                    break

            while True:
                print(ansi.clear_screen())
                if d["data"]["jobData"]["status"] is 2:
                    print('Waiting for another job...')
                    time.sleep(3)
                if d["data"]["jobData"]["status"] is 3:
                    print('Waiting for another job...')
                    time.sleep(3)
                if d["data"]["jobData"]["status"] is 1:
                    break
        except Exception as e:
            print(e)
            break


class base:
    start_time = int(time.time())


def rich_presence(): # Discord Rich Presence
    global rpc, d
    if is_running("eurotrucks2.exe"):
        rpc = Presence("731909306256982028")
        large_image = 'untitled-1'
        rpc.connect()
        mult = 3.6
        sp, _sp = 'km/h', 'km'
    elif is_running("amtrucks.exe"):
        rpc = Presence("743029516083134494")
        large_image = 'untitled-3'
        rpc.connect()
        mult = 2.24
        sp, _sp = 'mph', 'mi'
    while True:
        try:
            speed = round(d["data"]["telemetry"]["truck"]["speed"] * mult)
            if d["data"]["telemetry"]["job"]["onJob"] is False:
                details = "🚚 Freeroaming"
            elif d["data"]["telemetry"]["job"]["onJob"] is True:
                details = "🚚 {} -> {} | {} km left".format(d["data"]["jobData"]["sourceCity"],
                                                            d["data"]["jobData"]["destinationCity"],
                                                            round(d["data"]["telemetry"]["navigation"][
                                                                      "distance"] / 1000))
            if d["data"]["telemetry"]["game"]["isMultiplayer"] is True:
                state = "🌐 Multiplayer | {} {}".format(speed, sp)
            elif d["data"]["telemetry"]["game"]["isMultiplayer"] is False:
                state = "🌐 Singleplayer | {} {}".format(speed, sp)
            start = base.start_time
            small_text = "{} {} | {} {}".format(d["data"]["telemetry"]["truck"]["make"],
                                                d["data"]["telemetry"]["truck"]["model"],
                                                round(d["data"]["telemetry"]["truck"]["odometer"], 1),
                                                _sp)
            small_image = 'untitled-2'
            rpc.update(details=details, state=state, start=start, small_text=small_text, small_image=small_image,
                       large_image=large_image)
            time.sleep(5)
        except Exception as e:
            print(e)
            break


t = Thread(target=refresh)
_t = Thread(target=tracker)
t.start()
t.join(timeout=1)
time.sleep(2)
_t.start()
_t.join(timeout=1)
time.sleep(1)
rich_presence()
print(Fore.RED + 'Unable to communicate with plugin, shutting down...')
rpc.close()
time.sleep(3)
sys.exit(1)
