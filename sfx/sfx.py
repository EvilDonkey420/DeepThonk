import os, random, time
import contextlib
with contextlib.redirect_stdout(None):
    from pygame import mixer

# internal modules & packages
import conf
import games.raid
from utils.logger import loggyballs as logger

from moderation.permissions import getPermMode

# config ze bot!
twitch_bot = conf.twitch_instance

mixer.init(frequency=44100)
sfx_ch = 0
cheer_ch = 1


def play_sfx(full_file_path, r00d=True, unr00dable=False):
    'Interrupts any sound being played and plays the new one that\'s passed in'

    # prevent trampling over raid routine
    if full_file_path == 'sfx/events/raid_victory.ogg':
        pass

    elif games.raid.start():
        # logger.warning(f'SFX ABORTED {full_file_path}')
        return

    # play the new sound
    try:
        if r00d:
            # stop all sounds playing & load the new file
            mixer.Channel(sfx_ch).stop()
            mixer.Channel(sfx_ch).play(
                mixer.Sound(f"{full_file_path}")
                )
        else: 
            mixer.Channel(sfx_ch).play(
                mixer.Sound(f"{full_file_path}")
                )
            logger.info(f"{full_file_path} was playted")
    except TypeError as e:
        logger.warning(f"TypeError - path not playable. {e}")


def play_developers():

    developers = mixer.Sound('sfx/hardmode.ogg')
    developers.set_volume(0.5)
    developers.play()

    print('DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS ')


def stop_developers():
    mixer.Channel(cheer_ch).stop()


def play_random(folder_path):

    files = []

    for thing in os.listdir(folder_path):
        for thing in os.listdir(f'{folder_path}'):
            # add it to a list
            files.append(thing)

    random_sfx_file = f'{folder_path}{random.choice(files)}'

    play_sfx(random_sfx_file)


###################################################################
# SECTION SFX Generation via folder/file structure bidness
###################################################################

class SoundEffect:
    'Base class for all sound effects.'

    commands = []

    # constructor
    def __init__(self, cmd_name, cmd_path, cmd_timeout=conf.sfx['hooks_timeout']):
        self.name = cmd_name
        self.path = cmd_path
        self.timeout = cmd_timeout
        self.last_used = time.time()
        SoundEffect.commands.append(self) # list of sfx cmds

        # create/register file as command in event-loop
        @twitch_bot.command(self.name, module='SFX', perm=2)
        async def sfx_func(message):

            # if sub+ & they're not sub+
            if getPermMode() is 2 and not message.author.subscriber:
                # give no-perms feedback to chat and exit func/cmd
                msg = f"@{message.author.name}, sfx are for subscribers only \
                    atm. Sorry!"
                await twitch_bot.say(message.channel, msg)
                return
            
            else: # otherwise continue like normal
                # compare last use to this use & timeout var
                if time.time() - self.last_used >= self.timeout:
                    play_sfx(self.path)
                    self.last_used = time.time()


# REVIEW  move into a function later during refactor
path = 'sfx/hooks/'
for file in os.listdir(path):

    # create instance with attributes
    if file.endswith('.ogg'):
        cmd_name = file[:-4]
        cmd_path = path + file
        debug_msg = f'cmd_name={cmd_name} cmd_path={cmd_path}'
        SoundEffect(cmd_name, cmd_path)

# !SECTION


###################################################################
# SECTION Randomized SFX
###################################################################


class RandomSoundEffect:
    """
    Base class for all rando sound effects.

    Eventually looks like ==> RandoSoundEffect(file_name, permission_level, cost, cooldown).
    """

    commands = []

    # constructor
    def __init__(self, folder, files:list, aliases=(), cmd_timeout=conf.sfx['randoms_timeout']):
        self.name = folder
        self.folder = folder
        self.files = files
        self.aliases = aliases
        self.timeout = cmd_timeout
        self.last_used = time.time()

        # create/register file as command in event-loop
        @twitch_bot.command(self.name, alias=self.aliases, unprefixed=True, module='Random SFX', perm=0)
        async def rando_sfx_func(message):
            # compare last use to this use & timeout var
            if time.time() - self.last_used >= self.timeout:
                random_sfx_file = f'sfx/randoms/{self.folder}/{random.choice(self.files)}'
                play_sfx(random_sfx_file)
                # update the last_used thing
                self.last_used = time.time()
            
        # add the command name to a list to be used later for spreadsheet generation
        RandomSoundEffect.commands.append(self)


def generate_random_sfx_commands():

    path = 'sfx/randoms/'

    # get a list of folders in sfx/randoms & create commands for each
    for thing in os.listdir(path):

        # if directory
        if '.' not in thing or not thing.startswith('.'):
            folder = thing
            files = []

            # create a list of mp3s in folders (excluding aliases.txt)
            for file_name in os.listdir(f'{path}{folder}'):
                if file_name.endswith('.ogg'):
                    # add it to a list
                    files.append(file_name)

            # use the above list to create the object thingybob
            RandomSoundEffect(folder, files, get_aliases(folder))


def get_aliases(folder):
    # loads alias file based on folder name
    try:
        with open(f'sfx/randoms/{folder}/aliases.txt', 'r') as f:
            aliases = f.read().splitlines()
        return tuple(aliases)
    except:
        return []

generate_random_sfx_commands()

# !SECTION 


###################################################################
# SECTION Light-reactive SFX
###################################################################

class LEDSoundEffect:
    'Base class for all lighted-reactive sound effects.'

    commands = []

    # constructor
    def __init__(self, cmd_name, cmd_path, cmd_char):
        self.cmd = cmd_name
        self.path = cmd_path
        self.char = cmd_char

        # create/register file as command in event-loop
        @twitch_bot.command(self.cmd, module='LED SFX', perm=2)
        async def led_sfx_func(message):
            if message.author.subscriber or message.author.mod:
                # playsound(self.path + self.cmd + '.ogg') # REVIEW 
                play_sfx(self.path + self.cmd + '.ogg')
        
        # add the command name to a list to be used later for spreadsheet generation
        self.commands.append(self.cmd)


# REVIEW move these to UI or something later, so they don't have to be manually set up
# this is not fun
def setup_led_commands():
    path = 'sfx/ledcmds/'
    # LEDSoundEffect('flashbang', path, 'f')
    LEDSoundEffect('weewoo', path, 'w')

setup_led_commands()

# !SECTION 


###################################################################
# SECTION HELP Function
###################################################################


# REVIEW function these out in a refactor
@twitch_bot.command('sfx', module='Help', perm=0)
async def sfx(message):
    'Spits out a list of SFX commands. Pretty simple at the moment.'

    
    msg = 'SFX can be used freely by subscribers! :D !bigups, '

    # for every item in an enumerated list of commands
    for cmd in SoundEffect.commands:
        cmd_name = f'!{cmd.name}'  # add the !

        # get the length of the string & compare it to teh length it would be if it added the new command
        if (len(msg) + len(cmd_name) + 2) >= 500:
            # send message and start over
            await twitch_bot.say(message.channel, msg)
            msg = ''
        else:
            # add to msg
            if len(msg) is 0:
                msg += cmd_name
            else:
                msg += f', {cmd_name}'
    
    # then send the rest
    # playsound('sfx/sfx.ogg')
    play_sfx('sfx/sfx.ogg')
    await twitch_bot.say(message.channel, msg)


# REVIEW function these out in a refactor
@twitch_bot.command('randomsfx', module='Help', perm=0)
async def randomsfx(message):
    'Spits out a list of RANDOM SFX commands. Pretty simple at the moment.'

    
    msg = 'SFX can be used freely by subscribers! :D '

    # for every item in an enumerated list of commands
    for cmd in RandomSoundEffect.commands:
        cmd_name = f'{cmd.name}'  # add the !

        # get the length of the string & compare it to teh length it would be if it added the new command
        if (len(msg) + len(cmd_name) + 2) >= 500:
            # send message and start over
            msg = ''
        else:
            # add to msg
            if len(msg) is 0:
                msg += cmd_name
            else:
                msg += f', {cmd_name}'
    
    # then send the rest
    play_sfx('sfx/sfx.ogg')
    await twitch_bot.say(message.channel, msg)


# REVIEW function these out in a refactor
@twitch_bot.command('ledsfx', module='Help', perm=0)
async def ledsfx(message):
    'Spits out a list of all the LED-enabled SFX'

    
    msg = 'SFX can be used freely by subscribers! :D '

    # for every item in an enumerated list of commands
    for cmd in LEDSoundEffect.commands:
        cmd = f'!{cmd}' # add the !

        # get the length of the string & compare it to teh length it would be if it added the new command
        if (len(msg) + len(cmd) + 2) >= 500:
            # send message and start over
            msg = ''
        else:
            # add to msg
            if len(msg) is 0:
                msg += cmd
            else:
                msg += f', {cmd}'
    
    # then send the rest
    await twitch_bot.say(message.channel, msg)

# !SECTION