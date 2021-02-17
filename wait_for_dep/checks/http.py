import requests


def check(url):
    try:
        requests.get(url)
        return True
    except:
        return False
