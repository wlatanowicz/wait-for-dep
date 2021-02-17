from urllib.parse import urlparse

import redis


def check(url):
    parsed_url = urlparse(url)

    db_num = 0
    if parsed_url.path:
        url_path = parsed_url.path
        if url_path.startswith("/"):
            url_path = url_path[1:]
        db_num = int(url_path)

    try:
        redis.Redis(host=parsed_url.hostname, port=parsed_url.port or 6379, db=db_num)
        return True
    except Exception as e:
        return False
