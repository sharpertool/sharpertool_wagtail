import requests


def get_my_ip():
    res = requests.get('http://checkip.amazonaws.com')
    if res.status_code == 200:
        return res.text.strip()

    return None
