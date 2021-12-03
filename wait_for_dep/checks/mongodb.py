import pymongo


def check(url):
    try:
        pymongo.MongoClient(url,connect=True)
        return True
    except:
        return False
