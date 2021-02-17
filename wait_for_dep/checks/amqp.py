from urllib.parse import parse_qs, urlparse

import pika


def check(url):
    parsed_url = urlparse(url)
    config = {}

    if parsed_url.hostname:
        config["host"] = parsed_url.hostname

    if parsed_url.username or parsed_url.password:
        creds = {}
        if parsed_url.username:
            creds["username"] = parsed_url.username

        if parsed_url.password:
            creds["password"] = parsed_url.password

        config["credentials"] = pika.PlainCredentials(**creds)

    if parsed_url.port:
        config["port"] = parsed_url.port

    if parsed_url.path:
        vhost = parsed_url.path
        if vhost[0] == "/":
            vhost = vhost[1:]
        if vhost:
            config["virtual_host"] = vhost

    required_queues = []
    required_exchanges = []

    if parsed_url.query:
        query = parse_qs(parsed_url.query)
        required_queues = query.get("require_queue", [])
        required_exchanges = query.get("require_exchange", [])

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(**config))
        channel = connection.channel()

        for required_exchange in required_exchanges:
            channel.exchange_declare(exchange=required_exchange, passive=True)

        for required_queue in required_queues:
            channel.queue_declare(queue=required_queue, passive=True)

        return True
    except:
        return False
