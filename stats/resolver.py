from requests import get as request_get
from django.conf import settings

STEAM_API_KEY = settings.STEAM_WEB_API_KEY

def get_playerinfo(profile_url):
        try:
            player_info_url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={profile_url}'
            r = request_get(player_info_url,timeout=1)
            response_json = r.json()
            return response_json['response']['players'][0]

        except:
            pass


        steamid = profile_url.split('/')
        if steamid[-1] == '':
            to_resolve = steamid[-2]
        else:
            to_resolve = steamid[-1]
            

        # Try to get player info assuming steamid64 was input
        player_info_url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={to_resolve}'
        r = request_get(player_info_url,timeout=1)
        response_json = r.json()
        
        if len(response_json['response']['players']) == 0:
            # Try to get player info assuming vanity id was input
            vanity_url = f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={to_resolve}'
            r = request_get(vanity_url,timeout=1)
            response = r.json()
            response_json = response['response']
            if response_json['success'] == 1:
                player_info_url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={response_json["steamid"]}'
                r = request_get(player_info_url,timeout=1)
                response_json = r.json()
                return response_json['response']['players'][0]
            else:
                return None
        else:
            return response_json['response']['players'][0]

def get_playerinfo_s64(steamid64):
    player_info_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'
    url = player_info_url.format(STEAM_API_KEY,steamid64)
    response = request_get(url,timeout=1)
    response = response.json()
    return response['response']['players'][0]
    

def convert_to_steamid(steamid64):
    y = int(steamid64) - 76561197960265728
    x = y % 2 
    return "STEAM_1:{}:{}".format(x, (y - x) // 2)
    