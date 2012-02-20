import os
from unittest import defaultTestLoader

def run():
    path = os.path.dirname(__file__)
    return defaultTestLoader.discover(path)
