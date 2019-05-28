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
# import time 
import random
import asyncio
import conf

# config ze bot!
twitch_bot = conf.twitch_instance


def hex(hex_val):
    converter = Converter()
    return list(converter.hex_to_xy(hex_val))

class RaveInterrupted(Exception):
    pass

# WIP
class HueLight:
    """Will eventually be a wrapper class that contains the methods to control
    the lights a little more cleanly than the library provides. 
    
    Eventually, this will all be moved to a library I'll write myself once I
    experimennt a little more with how I want to use it. -Bun"""

    def __init__(self):
        self.state = ['off', 'on']


# WIP
class HueScene:
    """Will eventually hold scene data a little clearer."""
    pass


# WIP 
class HueSettings:
    """Eventually holds bot-specific settings for the integration"""
    
    active_lights = ""
    default_scene = {
        'scene_id' : 'DCnhWvdhx6pIeJt',
        'group_id' : '1'
    }

    default_group = ['bed', 'stairs', 'desk', 'DJ Ambient', 'Behind Desk', 'DJ Face']

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

    def get_default_scene(self):
        return self.default_scene

    def get_default_group(self):
        return self.default_group


class HueController:
    """Controls HueLights & HueScenes via the Bridge object, per Settings"""

    # Constructymajig
    def __init__(self, bridge):
        # TODO Pass in HueLights upon instantiation 
        self.bridge = bridge
        self.scenes = self.bridge.scenes
        self.settings = HueSettings()
        self._define_defaults()
        self.rave_mode = False

    def _define_defaults(self):
        self.default_group = self.settings.get_default_group()

    def toggle_lights(self):
        lights = self.bridge.lights
        for l in lights:
            l.on = not l.on
    
    def list_scenes(self):
        print("group\tlights\tscene_id\tname\t\tlastedited")
        for scene in self.bridge.scenes:
            print(f"{scene.group}\t{scene.lights}\t{scene.scene_id}\t{scene.name}\t{scene.lastupdated}")

    def lights_on(self, speed=100):
        lights = self.bridge.lights  # get dict with name as key
        for l in lights:
            l.bri = 254
            l.on = True

    def lights_off(self, speed=100):
        
        lights = self.bridge.lights
        for l in lights:
            l.transitiontime = speed
            l.bri = 254
            l.on = False

    def set_scene(self, scene_id, group_id=1, speed=1):
        self.bridge.activate_scene(
            scene_id=scene_id, 
            group_id=group_id, 
            transition_time=speed
            )
    
    def set_color(self, color, lights=None, speed=5):
        if lights is None:
            lights = self.default_group
        command = {
            'on' : True,
            'bri' :  254,
            'transitiontime' : speed,
            'xy' : self.settings.color[color]
        }
        self.bridge.set_light(lights, command)
    
    def return_to_default(self):
        'Returns all the lights to their default scene value'
        self.set_scene(
            self.settings.get_default_scene()['scene_id'],
            self.settings.get_default_scene()['group_id']
            )

    # TODO make this asynchronous
    async def flash(self, color, attack=10, sustain=.8, release=10, times=1):
        'Flashes brightly then slowly fades away'
        for i in range(times):
            self.set_color(color, speed=attack)
            await asyncio.sleep(sustain)
            self.lights_off(speed=release)
            await asyncio.sleep(sustain)

        await asyncio.sleep(release/10)
        self.return_to_default()

    async def wee_woo(self, rate, amount, lights=None):
        if lights is None:
            lights = self.settings.get_default_group()

        self.lights_on()

        for i in range(amount):
            self.set_color('red', lights=lights)
            await asyncio.sleep(rate)
            self.set_color('blue', lights=lights)
            await asyncio.sleep(rate)

        self.return_to_default()

    # WIP -- Need top get around using a while loop.
    async def rave_party(self, message, rate=0.5):

        lights = self.default_group
        self.rave_mode = True

        try:
            while True:
                command = {
                        'on' : True,
                        'bri' :  254,
                        'transitiontime' : 1,
                        'xy' : [random.random(), random.random()]
                    }
                self.bridge.set_light(lights, command)
                await asyncio.sleep(rate)
                self.lights_off()
                await asyncio.sleep(rate/2)
        except RaveInterrupted:
            pass

        await twitch_bot.say(message.channel, "Rave.. BUSTED!")
        self.return_to_default()

    async def bust_the_rave(self):
        self.rave_mode = False


controller = HueController(Bridge("192.168.1.136"))
controller.return_to_default()


def setup():
    """If running for the first time, press button on bridge and
    run with b.connect() uncommented"""

    # b.connect()
    pass
    
    
# ANCHOR DEBUG FUNCTIONS
###############################################################################


# async def hue_task(func):
#     twitch_bot.loop.create_task(func())


def list_groups(b):
    for i in range(len(b.get_group())):
        print(f"{i}  {b.get_group(i, 'name')}  {b.get_group(i, 'lights')}")


def list_lights(b):
    lights = b.lights
    for l in lights:
        print(f"{l.light_id}  n={l.name} t={l.transitiontime}")


def test():
    controller = HueController(Bridge("192.168.1.136"))
    # controller.toggle_lights()
    # controller.set_scene("oVlvecRqmwksXbZ", 1)
    # controller.bridge.delete_scene("GTJOhrsw2LyKSK")
    # controller.list_scenes()
    # controller.set_color('red')
    # controller.flash('white', attack=1, sustain=.1, release=40)
    controller.flash('red', times=4)

if __name__ == "__main__":
    # setup()
    test()
