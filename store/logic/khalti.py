from django.conf import settings
from requests import post

def verify_khalti(payload):
    key = settings.KHALTI_API_SECRET_KEY_TEST
    url = 'https://khalti.com/api/v2/payment/verify/'
    headers = {"Authorization": f"Key {key}"}
    r = post(url,payload,headers=headers,timeout=3)
    r = r.json()
    response = {}
    if r.get('validation_error',None):
        response['success'] = False
        response['data'] = r
    else:
        response['success'] = True
        response['data'] = r
    return response