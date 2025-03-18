import socket
from urllib.parse import urlparse


def check(url):
    parsed_url = urlparse(url)
    try:
        if not parsed_url.port:
            return False

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((parsed_url.hostname, parsed_url.port))
        return True
    except:
        return False
