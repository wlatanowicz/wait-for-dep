import socket
from urllib.parse import urlparse


def check(url):
    filename = url[len("unix://") :]
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(filename)
        return True
    except:
        return False
