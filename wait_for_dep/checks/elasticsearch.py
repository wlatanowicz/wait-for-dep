from .http import check as http_check


def check(url):
    url = "http" + url[len("elasticsearch") :]
    return http_check(url)
