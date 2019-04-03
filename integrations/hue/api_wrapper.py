# BIG TODO's
#  - Clean this file up a bit
#  - Set up default values for lights in scene
#  - Return lights to default values after reacts
#  - Set up all teh rest of the reacts (hosts, subs, etc)
#  - !rave and other fun command ideas
#  - Reacts when someone wins/loses chat game
#  - Sound reactive stuff? How do?

# WIP's
#  - !rave & !ravebusted
#  - !rave randomizes from a set list of colors

from rgbxy import Converter
from phue import Bridge
import random

import asyncio
import conf

# config ze bot!
twitch_bot = conf.twitch_instance
b = Bridge("192.168.1.136")  # h4ck t3h pl4n3t

# !globals(?)
rave_mode = False  # DEBUG 


def hex(hex_val):
    converter = Converter()
    return list(converter.hex_to_xy(hex_val))


# WIP
class HueLight:
    """Will eventually be a wrapper class that contains the methods to control
    the lights a little more cleanly than the library provides. 
    
    Eventually, this will all be moved to a library I'll write myself once I
    experimennt a little more with how I want to use it. -Bun"""

    color = {
        "test" : hex("ff0000"),
        "orange" : [.75, .5],
        "gold" : [.5, .5],
        "lightblue" : [0, .25],
        "green" : [0, 1],
        "blue" : [0, 0],
        "purple" : [.25, 0],
        "pink" : [.5, 0],
        "magenta" : hex("ff4cce"),
        "red" : [1, 0],
        "aqua" : [0, 0.5],
        "white" : hex("ffffff")
    }

    state = ['off', 'on']


# WIP
class HueScene:
    """Will eventually hold scene data a little clearer."""
    pass


# WIP 
class Settings:
    """Eventually holds bot-specific settings for the integration"""
    
    active_lights = ""
    default_scene = {
        'scene_id' : 'DCnhWvdhx6pIeJt',
        'group_id' : '1'
    }

    default_group = ['bed', 'stairs', 'desk']

    def get_default_scene(self):
        return self.default_scene

    def get_default_group(self):
        return self.default_group

settings = Settings()


class Controller:
    """Controls HueLights & HueScenes via the Bridge object, per Settings"""
    



def setup(pp):
    """If running for the first time, press button on bridge and
    run with b.connect() uncommented"""

    # b.connect()
    pass


async def wee_woo(lights, rate, amount):
    lights_on()
 
    for i in range(amount):
        set_color(['bed', 'desk', 'stairs'], 'red', 254)
        await asyncio.sleep(rate)
        set_color(['bed', 'desk', 'stairs'], 'blue', 254)
        await asyncio.sleep(rate)

    return_to_default()


async def flash(color, rate, lights=settings.get_default_group(), amount=1):
    set_color(lights, color)
    
    for i in range(amount):
        await asyncio.sleep(rate)
        lights_off()
        await asyncio.sleep(rate)
        lights_on()

    return_to_default()


async def flashbang():
    # turn on the lights quikcly and at full brightness, all white (1,1)
    set_color('white', speed=1)
    await asyncio.sleep(1)
    # fade them out slowly
    lights_off(speed=500)
    return_to_default()

    

# WIP -- Needs functionality
def return_to_default():
    'Returns all the lights to their default scene value'
    print("Reaction over. Returning to default settings.")
    settings = Settings()
    set_scene(settings.get_default_scene())
    

def set_color(color, lights=settings.get_default_group(), speed=5):
    lamp = HueLight()
    command = {
        'on' : True,
        'bri' :  254,
        'transitiontime' : speed,
        'xy' : lamp.color[color]
    }
    b.set_light(lights, command)


def set_color_old(b, light, color, bri=254):
    lights = b.get_light_objects('name')  # get dict with name as key
    # lamp = HueLight()
    lights[light].transitiontime = 1
    lights[light].brightness = bri


def lights_on(speed=100):
    lights = b.lights  # get dict with name as key
    for l in lights:
        l.bri = 254
        l.on = True


def lights_off(speed=100):
    lights = b.lights
    for l in lights:
        l.transitiontime = speed
        l.bri = 254
        l.on = False


def set_scene(scene:dict):
    # print(b.get_scene('S Y N T H'))
    b.activate_scene(scene_id=scene['scene_id'], group_id=scene['group_id'])


# WIP -- Need top get around using a while loop.
async def rave_party(message, rate=0.5):

    lights = b.lights

    rave_mode = True

    while rave_mode:
        for light in lights:
            lights_on(1)
            light.xy = [random.random(), random.random()]
            await asyncio.sleep(rate)
            lights_off(1)
            await asyncio.sleep(rate/2)

    await twitch_bot.say(message.channel, "Rave.. BUSTED!")
    
    return_to_default()



    
    
# ANCHOR DEBUG FUNCTIONS
###############################################################################

def toggle_lights():
    lights = b.lights
    for l in lights:
        l.on = not l.on
        print(f"{l.name} switch to {l.on}")


async def hue_task(func):
    twitch_bot.loop.create_task(func())


def list_groups(b):
    for i in range(len(b.get_group())):
        print(f"{i}  {b.get_group(i, 'name')}  {b.get_group(i, 'lights')}")


def list_lights(b):

    lights = b.lights
    for l in lights:
        print(f"{l.light_id}  n={l.name} t={l.transitiontime}")



def test():


    pass

if __name__ == "__main__":
    # setup()
    test()
