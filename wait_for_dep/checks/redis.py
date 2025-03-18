import redis


def check(url):
    try:
        redis.Redis.from_url(url).ping()
        return True
    except Exception as e:
        return False
