from urllib.parse import urlparse

import memcache


def check(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or "11211"

    try:
        mc = memcache.Client(["{}:{}".format(host, port)], debug=0)
        stats = mc.get_stats()
        return len(stats) > 0
    except:
        return False
