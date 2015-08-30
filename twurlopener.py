# Library imports
from urllib.request import urlopen, FancyURLopener, Request

class TWURLOpener(FancyURLopener):

    # UrlOpener version info
    version = "PyTwitch"
