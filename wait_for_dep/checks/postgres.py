import psycopg2


def check(url):
    if url.startswith("psql"):
        url = "postgres" + url[len("psql") :]

    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        return True
    except:
        return False
