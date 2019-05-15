import conf
from integrations.hue.api_wrapper import controller as hue
from integrations.hue.api_wrapper import RaveInterrupted
from sfx.sfx import play_sfx

# config ze bot!
twitch_bot = conf.twitch_instance


# ANCHOR Debug/test command
###############################################################################

@twitch_bot.command('debug')
async def debug(message):

    play_sfx('sfx/ledcmds/flashbang.ogg')
    twitch_bot.loop.create_task(hue.flashbang())


# ANCHOR Twitch commands (mostly for debug purposes)
###############################################################################

@twitch_bot.command('flashbang')
async def flashbang(message):
    play_sfx('sfx/ledcmds/flashbang.ogg')
    twitch_bot.loop.create_task(hue.flash('white', attack=1, sustain=.1, release=40))

@twitch_bot.command('weewoo')
async def weewoo(message):

    # gtfo if u dun b-long
    if not message.author.subscriber:
        await twitch_bot.say(message.channel, f"subscribers only, @{message.author.name}")
        return

    play_sfx('sfx/ledcmds/weewoo.ogg')
    twitch_bot.loop.create_task(hue.wee_woo(1, amount=4))


@twitch_bot.command('lightson')
async def lightson(message):
    hue.lights_on(1)

@twitch_bot.command('toggled')
async def toggled(message):
    hue.toggle_lights()

@twitch_bot.command('lightsoff')
async def lightsoff(message):
    hue.lights_off(1)


# # WIP -- Starts but won't cancel.
# @twitch_bot.command('rave')
# async def rave(message):
#     'Starts a rave, flashes a bunch of lights until it gets busted.'

#     rave = twitch_bot.loop.create_task(hue.rave_party(message))
#     await rave


# # WIP -- Not actually canceling the rave.
# @twitch_bot.command('ravebusted')
# async def ravebusted(message):
#     'Eventually a mock rave bust that happens in chat. Can we somehow gamify?'

#     # global rave_mode
#     # rave_mode = False
    
#     await twitch_bot.say(message.channel, "OPEN UP IT'S DA POLICE")
#     raise RaveInterrupted
#     await hue.bust_the_rave()
#     rave.cancel()
