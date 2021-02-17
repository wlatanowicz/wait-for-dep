from urllib.parse import urlparse

from kafka import KafkaProducer


def check(url):
    bootstrap_urls = url.split(",")
    bootstrap_parsed_urls = (urlparse(u) for u in bootstrap_urls)
    bootstrap_nodes = list(
        u.hostname + ":" + str(u.port or "9092") for u in bootstrap_parsed_urls
    )

    try:
        KafkaProducer(bootstrap_servers=bootstrap_nodes)
        return True
    except Exception as e:
        return False
