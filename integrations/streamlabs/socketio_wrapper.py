import asyncio
import socketio
import pprint
import logging
import json

import data_tools
import conf
from conf import streamlabs_socketio_token as sio_token

from sfx.sfx import play_developers
from sfx.sfx import stop_developers

from integrations.hue.api_wrapper import controller as hue

# config ze bot!
twitch_bot = conf.twitch_instance

pp = pprint.PrettyPrinter(indent=2)

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()

logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)

@sio.on('connect')
async def on_connect():
    print('[INFO] [Integrations > Streamlabs] Socket.io Server... CONNECTERD!!')


async def set_hardmode(truthiness):
    
    # load the json file to an object
    with open('C:/Users/Bun/AppData/Roaming/Code/User/settings.json') as f:
        vsc_settings = json.load(f)
    
    # ENABLE HARDMODE
    vsc_settings["powermode.enabled"] = truthiness
    
    # rewrite/encode the file
    with open('C:/Users/Bun/AppData/Roaming/Code/User/settings.json', 'w') as outfile:
        json.dump(vsc_settings, outfile, indent=4)


# NOTE Move this outside of the rapper in future refactor
async def hardmode_task(sender, seconds):

    sender = data_tools.ats_or_nah(sender)

    # on 
    await set_hardmode(True)
    play_developers()
    msg = f"@{sender} #HardM0de [ENGAGED] for {seconds} seconds."
    await twitch_bot.say('ninjabunny9000', msg)

    # hardmode timer
    await asyncio.sleep(int(seconds))  # timer value (secs)

    # off
    await set_hardmode(False)
    stop_developers()
    await twitch_bot.say('ninjabunny9000', "#HardM0de [DISENGAGED]")


@sio.on('event')
async def on_event(event):
    if event['type'] == 'bits':
        twitch_bot.loop.create_task(hue.flash('green', attack=1, release=1, sustain=.1, times=8))

    if event['type'] == 'bits' and int(event['message'][0]['amount']) >= 60:
        seconds = event['message'][0]['amount']
        sender = event['message'][0]['name']

        twitch_bot.loop.create_task(hardmode_task(sender, seconds))
    
    if event['type'] == 'follow':
        twitch_bot.loop.create_task(hue.flash('purple', times=4))

    if event['type'] == 'subscription':
        twitch_bot.loop.create_task(hue.flash('lightblue', times=4))
        
    if event['type'] == 'donation':
        twitch_bot.loop.create_task(hue.flash('yellow', times=4))

    if event['type'] == 'host':
        twitch_bot.loop.create_task(hue.flash('red', times=10))

    if event['type'] == 'raid':
        twitch_bot.loop.create_task(hue.flash('red', times=10))


@sio.on('disconnect')
async def on_disconnect():
    print(f"y u disconnect?")
    

async def listen_streamlabs():
    await sio.connect(f"https://sockets.streamlabs.com?token={sio_token}")
    await sio.wait()


if __name__ == '__main__':
    loop.run_until_complete(listen_streamlabs())