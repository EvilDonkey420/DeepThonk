import conf
import integrations.twitch.api_wrapper
from sfx.sfx import play_sfx

# config ze bot!
twitch_bot = conf.twitch_instance

class Rave:

    roles = {
        'dj' : "",
        'bouncer' : "",
        'sound guy/gal/gihrm' : "",
        'go go dancer' : "",
        'Bitchy McSmoochieFace' : "",
        'raver' : [],
        # 'staff' : [],
        # 'fire spinner' : "",
    }
    
    # follow the white rabbit

    def __init__(self):
        # assign roles
        self.assign_roles()
        self.get_guest_list()

    def assign_roles(self):
        chatters = integrations.twitch.api_wrapper.get_chatters()
        for chatter in chatters:
            for key, val in self.roles.items():
                # populate roles with chatter
                if isinstance(val, str) and val == "":
                    self.roles[key] = chatter
                    break
                elif isinstance(val, list):
                    self.roles[key].append(chatter)
                    break
            print(f"{chatter} added as {key}")

    def get_guest_list(self):
        'automatically puts VIPs on the guestlists, they dont have to buy tickets'
        pass

    def get_role(self, message):
        'checks the roles of the person that sent the message'
        pass

@twitch_bot.command('rave')
async def rave(message):
    play_sfx('sfx/hooks/airhorn.ogg')
    rave_party = Rave()
    await twitch_bot.say(message.channel, "k.")
