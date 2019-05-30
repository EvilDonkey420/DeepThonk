
# internal modules & packages
import conf
import data_tools
# from sfx.sfx import play_sfx
import sfx

# config ze bot!
twitch_bot = conf.twitch_instance

###############################################################################
# SECTION Reward System
###############################################################################


@twitch_bot.command('bigups', module='Utils', perm=0)
async def bigups(message):
    """
    Rewards followers/subs with whatever reward currnetly is for the strem.

    !bigups - list of folks getting rewards
    !bigups <user> - adds someone to reward queue
    !bigups qty - # of ppl on queue
    !bigups clear - rekt
    """

    # TODO Validation for members in the room

    sfx.sfx.play_sfx('sfx/hooks/bigups.ogg')

    # global dict for rewards
    # reward_register = data_tools.txt_to_list('data/', 'reward_list.txt')
    
    token = data_tools.tokenize(message, 2, lower_case=False)
    
    # if just `!reward`, list people in teh rewards
    # if len(token) is 1:
    #     if len(reward_register) >= 1:
    #         # list peeps in the cue
    #         rewardees = data_tools.stringify_list(reward_register, '@')
    #         msg = f'@{message.author.name}, these rad folks are qeueued for \
    #         rewards! {rewardees}'
    #         return
    #         await twitch_bot.say(message.channel, msg)

    # if not privilege.is_mod(message):
        # TODO Drop this into a function that spits out a standard response for lack of priveglage
        
    try:
        user = token[1]
        user = data_tools.ats_or_nah(user)

        msg = f"ninjab1Bigups BIGUPS to @{user}!!! Keep it rad, dude! \
            ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay ninjab1Bigups \
            ninjab1Slay ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay \
            ninjab1Slay ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay "
        await twitch_bot.say(message.channel, msg)
    
    except IndexError:
        msg = f"BIGUPS!!! ninjab1Bigups ninjab1Bigups ninjab1Bigups ninjab1Bigups"
        await twitch_bot.say(message.channel, msg)
            
        # return

    # subcommand = token[1]

    # # spit out how many peeps in teh queue
    # if subcommand == 'qty':
    #     msg = f'{len(reward_register)} rad dudes in teh queue'
    #     await twitch_bot.say(message.channel, msg)
    #     return

    #     '!bigups @<user>'

    # # clear the list if rewards rewarded
    # if subcommand == 'clear':
    #     data_tools.clear_txt('data/', 'reward_list.txt')
    #     msg = f'Rewards delivered!!! @{message.author.name} cleared the list. \
    #     Thx for bein rad, dudes!'
    #     await twitch_bot.say(message.channel, msg)
    #     return
    

    # # add the person to the list
    # else:
    #     user = token[1]
    #     user = data_tools.ats_or_nah(user)

    #     data_tools.add_to_txt('data/', 'reward_list.txt', token[1])  # new hotness
    #     # reward_register.append(token[1]) # old and busted
    #     msg = f'ninjab1Bigups for @{user}! What a champ! I\'ve added them to the reward \
    #     cue! :D'
    #     await twitch_bot.say(message.channel, msg)
    #     msg = f'ninjab1Slay ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay \
    #     ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay \
    #     ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay \
    #     ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay \
    #     ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay \
    #     ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay'
    #     await twitch_bot.say(message.channel, msg)

# !SECTION 
