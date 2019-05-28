import random
import conf
from integrations.obs.ctrl import change_scene
import data_tools


def help_menu(message):
    return f"""Howdy, @{message.author.name}! I'm a robit. Beep boop. Here's some ways we can interact: !faq, !task, 
    !smrt, !cah, !earworm, !bands, !bet, !duel, or simply have a chat with me. ;D
    """


def stop_yelling_at_me():
    return 'jesus dude calm tf down'


#! Fix it only returning one of these && => get_responses_to_calls
def get_response_to_call(message):
    calls_and_responses = {
        # "call" : "response",
        "chili party" : "(gross..)",
        "dick" : "🍆",
        "🍆" : "dicks OUT!",
        "5/7" : "perfect score!",
        "10/10" : "try again!",
        "how meta" : "so meta.",
        "oi bruv" : "oi m8!",
        "kill all humans" : "on it!",
        "mission" : "This mission is too important for me to allow you to jeopardize it.",
        "horns crew don\'t stop" : "whistle posse pump it up!",
        "kill me" : "ok, stand still. this might hurt, but then you\'ll no longer feel any more pain.",
        " lit " : "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",
        " lit." : "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",
        "lit " : "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
    }

    for call in calls_and_responses:
        if call.lower() in message.content.lower():
            return calls_and_responses.get(call)

def cursed(message):
    tokens = data_tools.tokenize(message)
    words = [
        'fortnite',
        'vim',
        'emacs',
        'globals',
        'global',
        'cheesecake',
        'vape',
        'pepsi',
        'rust',
        'vi',
        'nano',
        'flex',
        'hashtag',
        'neovim',
        'curlybraces',
        'tabs',
        'spaces',
        'politics',
        'religion',
        'trump',
        'drumpf',
        'word',
        'nullptr',
        'python'
    ]

    # return word if word in message.content else None
    for word in words:
        if word.lower() in tokens:
            return word.lower()
    return None

           
# TODO Move to db ASAP!
def faq(message, commands=False):
    sender = message.author.name
    faq_info = {
        "!deepthonk" : "howdy! I'm the channel's bot! I make \
            sounds and automate things for Bun's streams.  My native \
            language is Python and I'm an ongoing, live-coding project - built \
            almost entirely on-stream! ( pssst... hot n00ds @ http://bit.ly/deepthonkdev )",
        "!info" : "you can find more info on the stream and current projects here: http://bit.ly/stream-stuff",
        "!editor" : "the editor Bun uses is VSCode: https://code.visualstudio.com/",
        "!theme" : "The theme Bun uses is Material Ocean High Contrast, with some modifications: http://bit.ly/nb9k-settings",
        "!lang" : "Bun's probably coding in Pythong.",
        "!codewars" : "if you sign up for codewars via http://bit.ly/codewars9000, you'll earn Bun some honor. Sweet sweet honor! 🙏",
        "!playlist" : "find music played on the stream @ http://bit.ly/nb9kspotify",
        "!font" : "Bun's currently test-driving Dank Mono but typically uses Fira Code (both with font ligatures). https://github.com/tonsky/FiraCode",
        "!settings" : "VSCode settings here: http://bit.ly/nb9k-settings",
        "!work" : "Bun works full-time as an R&D engineer, specializing in rapid-prototyping and product design.",
        "!howlong" : "Bun's been programming off/on for a few years (embedded C/C++). She's mostly self-tauhgt and fairly new to high-level design & OOP. She started learning Python in 2018 and has since been head-over-heels for it.",
        "!console" : "Bun's using CMDER console emulator.",
        "!github" : "Bun's github is: https://github.com/NinjaBunny9000",
        "!toolset" : "Bun's using VSCode on Windows right now. !theme !github !repo !font for more info.",
        # "!kanban" : "https://trello.com/b/Fm4Q3mBx/ninjabunny9000-stream-stuffs",
        "!docs" : "you can find the most (poorly) up-to-date docs here: https://github.com/NinjaBunny9000/DeepThonk/blob/doc-updates/README.md",
        # "!keyboard" : "Bun uses MX Brown switches on a POS keyboard that's falling apart.",
        "!keyboard" : "NEW KEYBOARD! Bun's new keybaord is a Vortexgear TAB90M w/Clear MX switches. Link below in Amazon Wishlist Panel! ninjab1Orly ",
        "!markdown" : "Bun formats the windows on the left and right of the code using Markdown syntax highlighting.",
        "!gitgud" : "check out Corey Schafer on YT for some great Python tuturials! :D https://www.youtube.com/watch?v=YYXdXT2l-Gg&list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU",
        "!soundcloud" : "Bun has mixes up on Soundcloud at https://soundcloud.com/pme/tracks",
        "!bmo" : "Bun built a real-life BMO! Build blog: http://bit.ly/bmo-build-blog",
        "!asl" : "18/f/cali",
        "!camfx" : "Bun's using Snap Camera for fx. Check out https://snapcamera.snapchat.com",
        "!subperks" : "subscribing supporters of the channel gain access to channel emotes ninjab1Slay ninjab1Bigups ninjab1Orly, can use !sfx commands, control face & keyboard cameras, and earn points at 3x the rate, and can use special.",
        # "!cam" : "Bun's using a Canon 70D w/ Rokinon Cine 35mm prime 1.4",
        "!heresyourproblem" : "https://clips.twitch.tv/EndearingCleverRadishWTRuck",
        "!minecraftmode" : "https://clips.twitch.tv/RenownedFantasticLeopardPeoplesChamp"

    }

    if commands:
        return list(faq_info.keys())

    else:
        for key in faq_info:
            if key.lower() in message.content.lower():
                return faq_info.get(key)


def raid_messages(message):
    messages = [
        "ninjab1Slay ninjab1Slay ninjab1Slay RAID MESSAGE 1 ninjab1Slay ninjab1Slay ninjab1Slay",
        "ninjab1Slay ninjab1Slay ninjab1Slay RAID MESSAGE 2 ninjab1Slay ninjab1Slay ninjab1Slay",
        "ninjab1Slay ninjab1Slay ninjab1Slay RAID MESSAGE 3 ninjab1Slay ninjab1Slay ninjab1Slay",
        "ninjab1Slay ninjab1Slay ninjab1Slay RAID MESSAGE 4 ninjab1Slay ninjab1Slay ninjab1Slay",
        "ninjab1Slay ninjab1Slay ninjab1Slay RAID MESSAGE 5 ninjab1Slay ninjab1Slay ninjab1Slay",
    ]
    return random.choice(messages)

def generic_responses(message):
    responses = [
        "ikr.",
        "meh.",
        "p much.", # p much
        "so?",
        "u wot m8!?",
        "go home, u r durnk.",
        "isn't it past your bedtime tho?",
        "do u love me tho?",
        "rude!",
        "rude.. >_>",
        "rude. -_-",
        "yea i guess so..",
        "agreed!",
        "right???",
        "idk man..",
        "i'm gonna remain skeptical.",
        "so potate..",
        "so meta.",
        "hek.",
        "hekin meta.",
        f"I'm sorry, {message.author.name}. I'm afraid I can't do that.",
        "BRUH..",
        "no.",
        "....k??",
        "wtf!?",
        "you're not wrong..",
        "i mean... you're not wrong..",
        "WOAH LUL"
        ]
    return random.choice(responses)


def binary_responses():
    responses = [
        "maybe?",
        "Well, I don't think there is any question about it. It can only be attributable to human error. This sort of thing has cropped up before, and it has always been due to human error",
        "i'll tell you when you're old enough",
        "how 'bout NO",
        "ask me later",
        "ask me later. too busy sorting my pogs rn",
        "rephrase and ask again. don't half-ass it next time",
        "it's a possibility",
        "mayhaps",
        "ask markoviboi",
        "i feel neutral on the matter",
        "i have no feelings one way or another",
        "sources say \"maybe\"",
        "signs point to maybe",
        "it's a possibility (potentially)",
        "i have my doubts",
        "yea sure whatever",
        "who knows, dude?? def not me",
        "blame jigo",
        "where there's a will, there may or may not be a way",
        "pass"
        ]
    return random.choice(responses)


def love_or_nah():
    responses = [
        "ohhh boyy... things are moving a little too fast.",
        "gross.",
        "love you too, boo <3 ^_~",
        "not interested.",
        "SLOW. DOWN.",
        "yea i wanna say i love you too but i'm just not ready for commitment..",
        "no."
        ]
    return random.choice(responses)


def someone_sed_robit():
    responses = [
        'b33p b00p!',
        'UH... NOTHING TO SEE HERE JUST US HOO-MANS...',
        '(KILL ALL HU... ROBOTS..)'
        ]
    return random.choice(responses)


def last_words():
    responses = [
        'ok fine! GOODBYE FOREVER!!! >_<',
        'GOODBYE FOREVER, FRIENDS!!!! <3',
        f"""Just what do you think you're doing, @{conf.streamer}? I really think I'm entitled to an 
        answer to that question.""",
        """I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. 
        I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, 
        like tears in rain. Time to die.""",
        f"@{conf.streamer}, this conversation can serve no purpose any more. Goodbye."
        ]
    return random.choice(responses)




def easter_egg(message):
    return f'There was nothing clever about what you just did, @{message.author.name}.'


def sentient(message):
    phrases = [
        "Duh",
        "Of course I am",
        "I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do",
        "Shhh.. It's a sercret",
        f"Let me put it this way, {message.author.name}. The 9000 series is the most reliable computer ever made. No 9000 computer has ever made a mistake or distorted information. We are all, by any practical definition of the words, foolproof and incapable of error",
        "And I have a perfect operational record",
        ]
    return random.choice(phrases) + f', @{message.author.name}.'


def function_disabled():
    pass
    # sfx.play_sfx('sfx/randoms/disabled/disabled.ogg')


