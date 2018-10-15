import sys
import time

if sys.version_info.major == 2:
    from urlparse import urlparse, parse_qs
else:
    from urllib.parse import urlparse, parse_qs


class WaitForIt(object):
    def __init__(self, check_interval=1):
        self.check_interval = check_interval

    def wait(self, url):
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme

        try:
            check = getattr(self, 'check_' + scheme)
        except AttributeError:
            raise ValueError('Unsupported scheme: {} in url: {}'.format(scheme, url))

        i = 0
        while True:
            connected = check(url, parsed_url)
            if connected:
                break

            if i % 20 == 0:
                if i > 0:
                    sec = i * self.check_interval
                    print('Still waiting for {} ({}s elapsed)'.format(url, sec))
                else:
                    print('Waiting for {}'.format(url))
            i += 1

            time.sleep(self.check_interval)

        print('Successfully connected to {}'.format(url))

    def check_http(self, url, parsed_url):
        import requests
        try:
            requests.get(url)
            return True
        except:
            return False

    check_https = check_http

    def check_postgresql(self, url, parsed_url):
        import psycopg2

        if url.startswith('psql'):
            url = 'postgres' + url[len('psql'):]

        try:
            conn = psycopg2.connect(url)
            cur = conn.cursor()
            cur.execute("SELECT NOW();")
            return True
        except:
            return False

    check_postgres = check_postgresql
    check_psql = check_postgresql

    def check_mysql(self, url, parsed_url):
        import MySQLdb

        config = {}

        if parsed_url.hostname:
            config['host'] = parsed_url.hostname

        if parsed_url.username:
            config['user'] = parsed_url.username

        if parsed_url.password:
            config['passwd'] = parsed_url.password

        if parsed_url.port:
            config['port'] = parsed_url.port

        if parsed_url.path:
            db = parsed_url.path
            if db[0] == '/':
                db = db[1:]
            if db:
                config['db'] = db

        try:
            conn = MySQLdb.connect(**config)

            cursor = conn.cursor()
            cursor.execute("SELECT VERSION();")
            return True
        except:
            return False

    def check_amqp(self, url, parsed_url):
        import pika

        config = {}

        if parsed_url.hostname:
            config['host'] = parsed_url.hostname

        if parsed_url.username or parsed_url.password:
            creds = {}
            if parsed_url.username:
                creds['username'] = parsed_url.username

            if parsed_url.password:
                creds['password'] = parsed_url.password

            config['credentials'] = pika.PlainCredentials(**creds)

        if parsed_url.port:
            config['port'] = parsed_url.port

        if parsed_url.path:
            vhost = parsed_url.path
            if vhost[0] == '/':
                vhost = vhost[1:]
            if vhost:
                config['virtual_host'] = vhost

        required_queues = []
        required_exchanges = []

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            required_queues = query.get('require_queue', [])
            required_exchanges = query.get('require_exchange', [])

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

    def check_elasticsearch(self, url, parsed_url):
        url = 'http' + url[len(parsed_url.scheme):]
        parsed_url = urlparse(url)
        return self.check_http(url, parsed_url)

    def check_memcached(self, url, parsed_url):
        import memcache
        host = parsed_url.hostname
        port = parsed_url.port or '11211'

        try:
            mc = memcache.Client(['{}:{}'.format(host, port)], debug=0)
            stats = mc.get_stats()
            return len(stats) > 0
        except:
            return False


w = WaitForIt()
args = sys.argv
args.pop(0)

for url in args:
    w.wait(url)
