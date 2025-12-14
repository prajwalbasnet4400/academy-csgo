import logging
from requests import get as request_get
from requests.exceptions import RequestException
from django.conf import settings
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

STEAM_API_KEY = settings.STEAM_WEB_API_KEY


def identify_steamid_type(profile_url:str) -> dict:
    if not profile_url:
        logger.error("Empty profile_url provided")
        raise ValidationError("Steam profile URL is required")

    profile_url = str(profile_url).strip()

    # Check if it's a raw 17-digit steamid64
    if profile_url.isdigit() and len(profile_url) == 17:
        return {'type':'profiles','data':profile_url}

    profile_url = profile_url.strip('/')
    data = profile_url.split('/')

    # Filter out empty strings from split
    data = [d for d in data if d]

    if len(data) < 3:
        logger.error(f"Invalid profile URL format (too short): {profile_url}")
        raise ValidationError(f'Invalid profile URL: {profile_url}')

    # Check for steamcommunity.com domain
    if 'steamcommunity.com' not in profile_url:
        logger.error(f"Invalid profile URL (not steamcommunity.com): {profile_url}")
        raise ValidationError(f'Invalid profile URL: {profile_url}')

    url_type = data[-2] if len(data) >= 2 else None
    url_value = data[-1] if len(data) >= 1 else None

    if not url_value:
        logger.error(f"No steamid found in URL: {profile_url}")
        raise ValidationError(f'No Steam ID found in URL: {profile_url}')

    if url_type == 'id':
        return {'type':'id','data':url_value}
    elif url_type == 'profiles':
        if not url_value.isdigit() or len(url_value) != 17:
            logger.error(f"Invalid steamid64 in URL: {url_value}")
            raise ValidationError(f'Invalid Steam ID: {url_value}')
        return {'type':'profiles','data':url_value}
    else:
        logger.error(f"Unknown URL type '{url_type}' in: {profile_url}")
        raise ValidationError(f'Invalid profile URL format: {profile_url}')

def resolve_vanity_name(vanity_name:str) -> str:
    if not STEAM_API_KEY:
        logger.error("STEAM_API_KEY is not configured")
        raise ValidationError("Steam API key not configured")

    vanity_url = f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={vanity_name}'
    try:
        r = request_get(vanity_url, timeout=5)
        r.raise_for_status()
        response = r.json()
        response_json = response.get('response', {})

        if response_json.get('success') != 1:
            logger.error(f"Steam API error resolving vanity name '{vanity_name}': {response_json}")
            raise ValidationError(f"Could not resolve Steam vanity name: {vanity_name}")

        return response_json['steamid']
    except RequestException as e:
        logger.error(f"Request error resolving vanity name '{vanity_name}': {e}")
        raise ValidationError(f"Error connecting to Steam API: {e}")

def get_playerinfo(profile_url):
    if not STEAM_API_KEY:
        logger.error("STEAM_API_KEY is not configured")
        raise ValidationError("Steam API key not configured")

    player_info_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'

    try:
        data = identify_steamid_type(profile_url)

        if data.get('type') == 'id':
            steamid64 = resolve_vanity_name(data.get('data'))
        elif data.get('type') == 'profiles':
            steamid64 = data.get('data')
        else:
            logger.error(f"Unknown steamid type for profile_url: {profile_url}")
            return None

        url = player_info_url.format(STEAM_API_KEY, steamid64)
        response = request_get(url, timeout=5)
        response.raise_for_status()
        response_data = response.json()

        players = response_data.get('response', {}).get('players', [])
        if not players:
            logger.error(f"No player found for steamid64: {steamid64}")
            return None

        return players[0]
    except ValidationError:
        raise
    except RequestException as e:
        logger.error(f"Request error fetching player info for '{profile_url}': {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching player info for '{profile_url}': {e}")
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