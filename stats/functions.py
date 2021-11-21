import requests
# import re
from django.conf import settings

def get_steamid64(steamid):
    try:
        x , y , z = steamid.split(':')
        return int(z) * int(2) + int(y) + 76561197960265728
    except:
        return None

def get_steamid(sid):
    if len(str(sid)) != 17:
        return None
    try:
        y = int(sid) - 76561197960265728
    except:
        return None
    x = y % 2 
    return "STEAM_1:{}:{}".format(x, (y - x) // 2)

def get_profile(steamid64):
    r = requests.get(f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={settings.STEAM_WEB_API_KEY}&steamids={steamid64}')
    data = r.json()
    if data.get('response',None) == None:
        return None
    else:
        return data['response']['players'][0]

# def clean_name(name):
    # return re.sub(r"[^\\u0000-\\uFFFF]", "",name)