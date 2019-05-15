# TODO 
#  - Move bot commands to ctrl.py
#  - Update scene changes control to work with websockets vs advanced scene switcher
#  - Make cam/source changes work only in certain scenes (to prevent accidental enabling)
#  - Handle instantiation of the OBSCtrl abs-layer better, (own ws.connect,etc)
#
# DONE
#  - Make functions for switching scenes with websocket
#  - Or make a way to toggle scene control on/off? Maybe a "privacy/brb" mode? (!faceless)

import sys
import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket import obsws, requests

import conf
# config ze bot!
twitch_bot = conf.twitch_instance

host = "localhost"
port = 4444
password = "password" # SECURE AF™

ws = obsws(host, port, password)
no_permissions_msg = "controlling the camera is a subscriber perk! For more info, send !subperks in chat! :D"
face_cam_allowed = True

class OBSCtrl:

    def __init__(self):
        pass
    
    def enableSource(self, source_name, state:bool, scene):
        ws.call(requests.SetSceneItemRender(source_name, state, scene_name=scene))

    def switchScene(self, scene):
        ws.call(requests.SetCurrentScene(scene))

try:
    ws.connect()
    obs = OBSCtrl()
except:
    print("[INFO] [Integrations > OBS ] OBS ISN'T RUNNING!")


# Swaps to face cam (SUB-only)
@twitch_bot.command('face')
async def face(message):

    if not face_cam_allowed:
        msg = f"@{message.author.name}, facecam is disabled for a min. BRB. <3"
    elif message.author.subscriber or message.author.mod or message.author.name == conf.streamer:
        obs.enableSource('CAM - Face', True, '[SC] Cams (with frame)')
        # ws.call(requests.SetSceneItemRender('CAM - Face', True, scene_name='[SC] Cams (with frame)'))
        msg = 'Face cam is back!'
    else:
        msg = f"@{message.author.name}, {no_permissions_msg}"

    await twitch_bot.say(message.channel,msg)


# Swaps to kb cam (SUB-only)
@twitch_bot.command('kb')
async def kb(message):

    if message.author.subscriber or message.author.mod or message.author.name == conf.streamer:
        obs.enableSource('CAM - Face', False, '[SC] Cams (with frame)')
        msg = 'Clickity-clack time!!'
    else:
        msg = f"@{message.author.name}, {no_permissions_msg}"

    await twitch_bot.say(message.channel, msg)

# disables switching to facecam until it's toggled back off - privacy stuff w/e
@twitch_bot.command('faceless')
async def faceless(message):
    if message.author.mod or message.author.name == conf.streamer:
        global face_cam_allowed
        face_cam_allowed = not face_cam_allowed
        if face_cam_allowed:
            obs.enableSource('CAM - Face', True, '[SC] Cams (with frame)')
            msg = "facecam back online!"
        else:
            obs.enableSource('CAM - Face', False, '[SC] Cams (with frame)')
            msg = "facecam offline for an minuto. brb!"

        await twitch_bot.say(message.channel, msg)


# switches scene to chatting
@twitch_bot.command('chat')
async def chat(message):
    obs.switchScene('Chatting')
    msg = f"@{message.author.name} switched the scene to Chatting."
    await twitch_bot.say(message.channel, msg)


# switches scene to live coding
@twitch_bot.command('code')
async def code(message):
    obs.switchScene('Live Coding')
    msg = f"@{message.author.name} switched the scene to Live Coding."
    await twitch_bot.say(message.channel, msg)
