import random
import os

# internal modules & packages
import conf
import data_tools
from integrations.twitch.privilege import is_bot, is_mod

# # config ze bot!
twitch_bot = conf.twitch_instance

@twitch_bot.command('counter')
async def counter(message):
    pass
    """
    !counter <create/reset> <name>


    """