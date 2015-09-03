# Library imports
import os

# Class imports
from twchannel import *

# Twitch chat server related constants
TWITCH_HOST = "irc.twitch.tv"
TWITCH_PORT = 6667
TWITCH_USER = "BOTNAME"
TWITCH_AUTH = "oauth:xxxxxxxxxxx"
TWITCH_MEMR = ":twitch.tv/membership"
TWITCH_CMDR = ":twitch.tv/commands"
TWITCH_TAGR = ":twitch.tv/tags"

# Twitch chat handling related variables / objects
TWITCH_CHANNELS_RGD = {}
TWITCH_CHANNELS_CND = {}
TWITCH_BOT_STAFF = {}
TWITCH_CHATTERS_TIMER = 0
TWITCH_CHATTERS_FREQU = 5

# Save registered channels into a txt file
def saveChannelData():
    file = open("channels.cfg", "w")
    for key in TWITCH_CHANNELS_RGD:
        file.write(TWITCH_CHANNELS_RGD[key].name + "\n")
    file.close()

# Load registered channels to TWITCH_CHANNELS_RGD
def loadChannelData():
    if not os.path.exists("channels.cfg"):
        open("channels.cfg", "w+").close()
    file = open("channels.cfg", "r")
    for line in file:
        lfixed = str.split(line, "\n")
        TWITCH_CHANNELS_RGD[lfixed[0]] = TWChannel(lfixed[0], TWITCH_CHATTERS_FREQU)
    file.close()

# Save registered staff into a txt file
def saveStaffData():
    file = open("botstaff.cfg", "w")
    for key in TWITCH_BOT_STAFF:
        file.write(TWITCH_BOT_STAFF[key] + "\n")
    file.close()

# Load registered staff to TWITCH_BOT_STAFF
def loadStaffData():
    if not os.path.exists("botstaff.cfg"):
        open("botstaff.cfg", "w+").close()
    file = open("botstaff.cfg", "r")
    for line in file:
        lfixed = str.split(line, "\n")
        TWITCH_BOT_STAFF[lfixed[0]] = lfixed[0]
    file.close()
