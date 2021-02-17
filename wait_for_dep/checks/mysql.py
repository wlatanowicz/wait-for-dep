from urllib.parse import urlparse

import mysql.connector


def check(url):
    parsed_url = urlparse(url)
    config = {}

    if parsed_url.hostname:
        config["host"] = parsed_url.hostname

    if parsed_url.username:
        config["user"] = parsed_url.username

    if parsed_url.password:
        config["password"] = parsed_url.password

    if parsed_url.port:
        config["port"] = parsed_url.port

    if parsed_url.path:
        db = parsed_url.path
        if db[0] == "/":
            db = db[1:]
        if db:
            config["db"] = db

    try:
        conn = mysql.connector.connect(**config)

        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        return True
    except:
        return False
