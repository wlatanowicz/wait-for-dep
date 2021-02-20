import requests


def check(url):
    try:
        response = requests.get(url, allow_redirects=True)
        if 200 <= response.status_code < 300:
            return True
        return False
    except:
        return False
