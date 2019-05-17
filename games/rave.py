# TODO 
# - Don't let more than one rave happen at a time maybe?? o_0?
# - Promoter role note getting assigned
# - Add the streamer to the list of chatters
# - Make more roles for people
# - Bun broke !raverole


import conf
import integrations.twitch.api_wrapper
from sfx.sfx import play_sfx

# config ze bot!
twitch_bot = conf.twitch_instance
rave_party = object()

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

    def __init__(self, message):
        # assign roles
        self.assign_roles(message)
        self.get_guest_list()

    def assign_roles(self, message):

        chatters = integrations.twitch.api_wrapper.get_chatters(
            lower=False,
            streamer_included=True
            )
        chatters.remove(message.author.name)  # make sure promoter gets 1 role only

        print(chatters)

        self.roles['promoter'] = message.author.name

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
        
        for k,v in self.roles:
            if v.lower() == message.author.name.lower():
                return k
            else:
                return None


@twitch_bot.command('rave')
async def rave(message):

    global rave_party

    play_sfx('sfx/hooks/airhorn.ogg')
    rave_party = Rave(message)
    await twitch_bot.say(message.channel, f"@{message.author.name} IS THROWING A \
        RAVE! Use !raverole to discover your defining purpose in life.")

@twitch_bot.command('raverole')
async def raverole(message):

    try:
        raverole = rave_party.getRole()
    except AttributeError:
        msg = f"@{message.author.name}, nobody's throwing a rave right now."
        await twitch_bot.say(message.channel, msg)

    try:
        if raverole:
            msg = f"@{message.author.name}, your role is {raverole}"
        else: 
            msg = f"@{message.author.name}, you're not on the list. You're not getting in."
    except:
        pass    
 
    await twitch_bot.say(message.channel, msg)
