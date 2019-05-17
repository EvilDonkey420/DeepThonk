# TODO
# - Why isn't streamer included in chatters response?

import requests
from conf import streamer

def get_chatters(lower=True, streamer_included=False):
    r = requests.get('https://tmi.twitch.tv/group/user/ninjabunny9000/chatters')
    r = r.json()
    chatters = r['chatters']['viewers']
    chatters.extend(r['chatters']['moderators'])
    chatters.extend(r['chatters']['staff'])
    chatters.extend(r['chatters']['admins'])
    chatters.extend(r['chatters']['vips'])

    if lower is True:
        for member in chatters:
            member.lower()

    if not streamer_included:
        chatters.append(streamer)

    return chatters


def get_mods():
    r = requests.get('https://tmi.twitch.tv/group/user/ninjabunny9000/chatters')
    r = r.json()
    mods = r['chatters']['moderators']
    mods.extend(r['chatters']['admins'])

    for member in mods:
        member.lower()

    return mods

