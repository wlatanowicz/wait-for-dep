try:
    import psycopg2 as psycopg
except ImportError:
    import psycopg

def check(url):
    if url.startswith("psql"):
        url = "postgres" + url[len("psql") :]

    try:
        conn = psycopg.connect(url)
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        return True
    except:
        return False
