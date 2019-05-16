from integrations.obs.websocket import obs
from utils.logger import loggyballs as log

# config ze bot!
import conf
twitch_bot = conf.twitch_instance


# ANCHOR Utilities

# disables switching to facecam until it's toggled back off - privacy stuff w/e
@twitch_bot.command('faceless')
async def faceless(message):
    if message.author.mod or message.author.name == conf.streamer:
        obs.face_cam_allowed = not obs.face_cam_allowed
        if obs.face_cam_allowed:
            obs.enableSource('CAM - Face', True, '[SC] Cams (with frame)')
            msg = "facecam back online!"
        else:
            obs.enableSource('CAM - Face', False, '[SC] Cams (with frame)')
            msg = "facecam offline for an minuto. brb!"

        await twitch_bot.say(message.channel, msg)


# ANCHOR Source Control

# Swaps to face cam (SUB-only)
@twitch_bot.command('face')
async def face(message):

    if not obs.face_cam_allowed:
        msg = f"@{message.author.name}, facecam is disabled for a min. BRB. <3"
    elif message.author.subscriber or message.author.mod or message.author.name == conf.streamer:
        obs.enableSource('CAM - Face', True, '[SC] Cams (with frame)')
        msg = 'Face cam is back!'
    else:
        msg = f"@{message.author.name}, {obs.no_permissions_msg}"

    await twitch_bot.say(message.channel,msg)


# Swaps to kb cam (SUB-only)
@twitch_bot.command('kb')
async def kb(message):

    if message.author.subscriber or message.author.mod or message.author.name == conf.streamer:
        obs.enableSource('CAM - Face', False, '[SC] Cams (with frame)')
        msg = 'Clickity-clack time!!'
    else:
        msg = f"@{message.author.name}, {obs.no_permissions_msg}"

    await twitch_bot.say(message.channel, msg)


# ANCHOR Scene Control

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



# ANCHOR OBS Scene Control - OLD METHOD

def change_scene(scene):
    """
    **Requires 'Advance Scene Switcher' plug-in**
    Swap scenes in OBS studio by writing the scene name to a file.
    """
    log.debug(f'Scene changed to {scene}')
    f = open('data\\scene_next.txt', 'w+')
    f.write(scene)
    f.close()


def get_scene():
    """
    **Requires 'Advance Scene Switcher' plug-in**
    Read current scene from OBS studio, which is writing scene names 
    to a .txt file.
    """
    f = open('data\\scene_current.txt', 'r+')
    scene = f.readline()
    f.close()
    return scene
