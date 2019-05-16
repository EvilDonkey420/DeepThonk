# TODO 
#  - Make cam/source changes work only in certain scenes (to prevent accidental enabling)
#       - raid game maybe?
#       - can't jump scenes in the middle of raids, etc.
#
# DONE
#  - Handle instantiation of the OBSCtrl abs-layer better, (own ws.connect,etc)
#  - Update scene changes control to work with websockets vs advanced scene switcher
#  - Move bot commands to ctrl.py
#  - Make functions for switching scenes with websocket
#  - Or make a way to toggle scene control on/off? Maybe a "privacy/brb" mode? (!faceless)

from obswebsocket import obsws, requests

# config ze bot!
import conf
twitch_bot = conf.twitch_instance

class OBSCtrl:

    # constructor
    def __init__(self, host, port, password):
        self.ws = obsws(host, port, password)
        self.ws.connect()
        self.face_cam_allowed = True
        self.no_permissions_msg = "controlling the camera is a subscriber perk! For more info, send !subperks in chat! :D"
    
    def enableSource(self, source_name, state:bool, scene):
        self.ws.call(requests.SetSceneItemRender(source_name, state, scene_name=scene))

    def switchScene(self, scene):
        self.ws.call(requests.SetCurrentScene(scene))


try:
    obs = OBSCtrl("localhost", 4444, "password") # SECURE AF™
except:
    print("[INFO] [Integrations > OBS ] OBS ISN'T RUNNING!")
