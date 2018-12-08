import asyncio
from conf import twitch_instance
from twitch_chat import tokenize, is_mod

# config ze bot!
twitch_bot = twitch_instance
 
# ze globals
squad_count = 0
troll_count = 0
troll_bans = 0
troll_timeouts = 0
probation_timer = {}
strike_list = {}

@twitch_bot.command('trolls')
async def trolls(message):
    troll_status = "We've seen {} squads, {} shit-tier trolls, and have banned {} lame trolls tonight".format(
        squad_count, troll_count, troll_bans
    )
    await twitch_bot.say(message.channel, troll_status)

@twitch_bot.command('troll')
async def troll(message):
    global squad_count
    global troll_count
    global troll_bans
    global troll_timeouts
    
    token = tokenize(message, 3)
    print(token)

    doin_it_wrong = 'Usage: !troll pban/squad/shitlord. '

    if len(token) == 1:
        await twitch_bot.say(message.channel, doin_it_wrong)
        await asyncio.sleep(3)
        await twitch_bot.say(message.channel, 'Mods, be sure to ban trolls before giving them any \"attention\"')
        return

    if token[1] == 'squad':
        squad_count += 1
        response = 'Shitsquad registered. Whelp. Color-me surprised, we\'ve seen {} tonight.'.format(squad_count)
        await twitch_bot.say(message.channel, response)

    elif token[1] == 'shitlords':
        try:
            troll_count += int(token[2])
            response = 'Shit-tier troll(s) registered. {} so far this stream. We are unimpressed.'.format(troll_count)
            await twitch_bot.say(message.channel, response)
            return
        except:
            usage = '!troll shitlord [qty] when u witnerss sub-par trolling. Git gudder, scrubs.'
            await twitch_bot.say(message.channel, doin_it_wrong + usage)
            return

    elif token[1] == 'timeout':
        if is_mod(message):
            try:
                user = token[2]
                ban_command = '/timeout {} 60'.format(user)
                confirm = 'No problemo, @{}.'.format(message.author.name)
                troll_bans += 1
                await twitch_bot.say(message.channel, confirm)
                if len(token) == 4:
                    ban_reason = token[3]
                    ban_warning = 'Timing out @{} for 1 min. Cuz {}. Say your last words, chump.'.format(user, ban_reason)
                else:
                    ban_warning = 'Timing out @{} in 10s. Say your last words, chump.'.format(user)
                await twitch_bot.say(message.channel, ban_warning)
                await asyncio.sleep(10)
                await twitch_bot.say(message.channel, ban_command)
                rest_in_pepperonis = 'The problem has been taken care of, m\'lady. {} bans so far.'.format(troll_bans)
                await twitch_bot.say(message.channel, rest_in_pepperonis)
                await asyncio.sleep(4)
                memes = '/me tips fedora'
                await twitch_bot.say(message.channel, memes)
                return
            except:
                usage = 'ie, !troll ban [username]. Mods only, meatbags.'
                await twitch_bot.say(message.channel, doin_it_wrong + usage)
                return
        else:
            msg = 'Nice try, chump.'
            await twitch_bot.say(message.channel, msg)
            
    elif token[1] == 'ban':
        if is_mod(message):
            try:
                user = token[2]
                ban_command = '/ban {}'.format(user)
                confirm = 'No problemo, @{}.'.format(message.author.name)
                troll_bans += 1
                await twitch_bot.say(message.channel, confirm)
                if len(token) == 4:
                    ban_reason = token[3]
                    ban_warning = 'Banning @{} in 10s. Cuz {}. Say your last words, chump.'.format(user, ban_reason)
                else:
                    ban_warning = 'Banning @{} in 10s. Say your last words, chump.'.format(user)
                await twitch_bot.say(message.channel, ban_warning)
                await asyncio.sleep(10)
                await twitch_bot.say(message.channel, ban_command)
                rest_in_pepperonis = 'The problem has been taken care of, m\'lady. {} bans so far.'.format(troll_bans)
                await twitch_bot.say(message.channel, rest_in_pepperonis)
                await asyncio.sleep(4)
                memes = '/me tips fedora'
                await twitch_bot.say(message.channel, memes)
                return
            except:
                usage = 'ie, !troll ban [username]. Mods only, meatbags.'
                await twitch_bot.say(message.channel, doin_it_wrong + usage)
                return
        else:
            msg = 'Nice try, chump.'
            await twitch_bot.say(message.channel, msg)


@twitch_bot.command('strike')
async def strike(message):
    """
    Command looks like..??? ==> !strike <user> <reason>
    """

    global probation_timer
    global strike_list
    
    # check for permissions
    if not is_mod(message):
        return

    # tokenize™
    token = tokenize(message, 2)

    # handle incorrect usages/token-lengths

    # check if on probation
        # ban them if they are


    # check if they have any strikes
    if token[1] in strike_list:
        strikes = strike_list[token[1]]
        stroken_user = token[1]
        msg = 'user=' + stroken_user + ' | strikes=' + strikes
        print(msg)
        await twitch_bot.say(message.channel, msg)
    else:
        strike_list.update({'token[1]' : 1})
        msg = 'not on striked. put on striked nao. current stroktders = {}'.format(strike_list.keys())
        print(msg)
        await twitch_bot.say(message.channel, msg)
        return


    # check strikes
        # if strike 2
            # record strike
            # report to chat
        # elif strike 3
            # ban user
            # report to chat
        # else
            # add to probation_list & record 1st strike
            # put on 10m probation
            # report to chat
 
@twitch_bot.command('mybad')
async def mybad(message):
    pass
    # check for permissions
    # tokenize™
    # undo


@twitch_bot.command('stroke')
async def stroke(message):
    global strike_list
    print(strike_list)
    await twitch_bot.say(message.channel, str(strike_list.keys()))
