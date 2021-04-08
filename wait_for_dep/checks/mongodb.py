import pymongo


def check(url):
    try:
        pymongo.MongoClient(url)
        return True
    except:
        return False
