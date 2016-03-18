# Library imports
import os

# Class imports
from fileutils import *
from twchannel import *

# Twitch chat server related constants
TWITCH_HOST = "irc.twitch.tv"
TWITCH_PORT = 6667
TWITCH_USER = "botusername"
TWITCH_AUTH = "oauth:xxxxxxxxxxxxxxxxxxxxxxxxxx"
TWITCH_MEMR = ":twitch.tv/membership"
TWITCH_CMDR = ":twitch.tv/commands"
TWITCH_TAGR = ":twitch.tv/tags"

# Twitch chat handling related variables / objects
TWITCH_CHANNELS_RGD = {}
TWITCH_CHANNELS_CND = {}
TWITCH_BOT_STAFF = {}
TWITCH_CHATTERS_TIMER = 0
TWITCH_CHATTERS_FREQU = 5
TWITCH_MSGS_PER_MINUTE_MOD = 200
TWITCH_MSGS_PER_MINUTE_NRM = 40
TWITCH_MSGS_RATE = 0

# MMaker related variables
TWITCH_MMAKER_URL_UNPLYD = "http://url_to_your_bot_mmaker_unplayed_folder (So you need to host it on webserv)"
TWITCH_MMAKER_ULR_PLAYED = "http://url_to_your_bot_mmaker_payed_folder (So you need to host it on webserv)"

# Save registered channels into a txt file
def saveChannelData():
    file = open("channels.cfg", "w")
    for key in TWITCH_CHANNELS_RGD:
        file.write(TWITCH_CHANNELS_RGD[key].name + "\n")
    file.close()

# Load registered channels to TWITCH_CHANNELS_RGD
def loadChannelData():
    fileExists("channels.cfg")
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
    fileExists("botstaff.cfg")
    file = open("botstaff.cfg", "r")
    for line in file:
        lfixed = str.split(line, "\n")
        TWITCH_BOT_STAFF[lfixed[0]] = lfixed[0]
    file.close()
