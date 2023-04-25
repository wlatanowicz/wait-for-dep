from os import path

with open(path.join(path.dirname(__file__), "VERSION"), encoding="utf-8") as f:
    __version__ = f.read().strip()
