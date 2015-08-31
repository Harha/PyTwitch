# Class imports
from twchannel import *

# Twitch chat server related constants
TWITCH_HOST = "irc.twitch.tv"
TWITCH_PORT = 6667
TWITCH_USER = ""
TWITCH_AUTH = "oauth:xxxxxxxxx"
TWITCH_MEMR = ":twitch.tv/membership"
TWITCH_CMDR = ":twitch.tv/commands"
TWITCH_TAGR = ":twitch.tv/tags"

# Twitch chat handling related variables / objects
TWITCH_CHANNELS_RGD = {}
TWITCH_CHANNELS_CND = {}
TWITCH_CHATTERS_TIMER = 0
TWITCH_CHATTERS_FREQU = 5

# Save registered channels into a json file
def saveChannelData():
    file = open("channels.cfg", "w")
    for key in TWITCH_CHANNELS_RGD:
        file.write(TWITCH_CHANNELS_RGD[key].name + "\n")
    file.close()

# Load registered channels to TWITCH_CHANNELS_RGD
def loadChannelData():
    file = open("channels.cfg", "r")
    for line in file:
        lfixed = str.split(line, "\n")
        TWITCH_CHANNELS_RGD[lfixed[0]] = TWChannel(lfixed[0], TWITCH_CHATTERS_FREQU)
    file.close()
