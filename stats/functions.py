from django.conf import settings
import discord_notify as dn

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

def send_message_discord(hook_url,message):
    notifier = dn.Notifier(hook_url)
    notifier.send(message,print_message=False)
