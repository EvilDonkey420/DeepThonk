import conf

# config ze bot!
twitch_bot = conf.twitch_instance

permissions_mode = 2

def getPermMode():
    return permissions_mode

# TODO IDEA! Add timer to follower-only mode.
@twitch_bot.command('swapmodes', module='debug', alias=['👯'])
async def swapmodes(message):

    if message.author.mod or message.author.name == conf.streamer:

        global permissions_mode

        if permissions_mode is 1:
            permissions_mode = 2
            msg = f"@{message.author.name}, sound effects, cam, & scene control is \
                back in Subscriber-only mode."
        
        elif permissions_mode is 2:
            permissions_mode = 1
            msg = f"@{message.author.name}, sound effects, cam, & scene control are \
                in Follower-only mode for a bit!"

    else:
        msg = f"@{message.author.name}, this command is for mods+."

    await twitch_bot.say(message.channel, msg)