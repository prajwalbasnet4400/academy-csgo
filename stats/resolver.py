import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_playerinfo(profile_url):
        api_key = os.environ.get('STEAM_API_KEY')
        try:
            player_info_url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={profile_url}'
            r = requests.get(player_info_url,timeout=1)
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
        player_info_url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={to_resolve}'
        r = requests.get(player_info_url,timeout=1)
        response_json = r.json()
        
        if len(response_json['response']['players']) == 0:
            # Try to get player info assuming vanity id was input
            vanity_url = f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={api_key}&vanityurl={to_resolve}'
            r = requests.get(vanity_url,timeout=1)
            response = r.json()
            response_json = response['response']
            if response_json['success'] == 1:
                player_info_url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={response_json["steamid"]}'
                r = requests.get(player_info_url,timeout=1)
                response_json = r.json()
                return response_json['response']['players'][0]
            else:
                return None
        else:
            return response_json['response']['players'][0]

def convert_to_steamid(steamid64):
    y = int(steamid64) - 76561197960265728
    x = y % 2 
    return "STEAM_1:{}:{}".format(x, (y - x) // 2)
    