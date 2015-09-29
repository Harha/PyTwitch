# Library imports
import os
import string
import json
import time
import threading

# Class imports
from fileutils import *
from twurlopener import *
from mmakerlevel import *

class TWChannel(object):

    # Class constructor
    def __init__(self, name, updateintrvl):
        # Assign input variables to member variables
        self.name = name.lower()
        self.updateintrvl = updateintrvl
        self.error = False
        self.cmdsent = 0
        self.thread = threading.Thread(target = self.run)
        self.running = False
        self.mmaker_levels_pld = []
        self.mmaker_levels_upl = []
        self.mmaker_level_crnt = MMakerLevel("null", "null")
        self.chatter_count = 0
        self.moderators = None
        self.staff = None
        self.admins = None
        self.global_mods = None
        self.viewers = None
        # Create urlopeners for receiving json data
        self.urlopener_chatters = TWURLOpener()
        self.urlopener_chatters.addheader("Accept", "application/vnd.twitchtv.v3+json")
        # Load saved mario maker levels
        self.loadLevels()

    # Update loop
    def run(self):
        while self.running:
            self.getchatters()
            time.sleep(self.updateintrvl)

    # For printing the object
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

    # Request channel info via json
    def getchatters(self):
        # Retrieve data from the channel, catch the to-be-expected ValueError.
        try:
            data = self.urlopener_chatters.open("https://tmi.twitch.tv/group/user/" + str.lstrip(self.name, '#') + "/chatters").read().decode("UTF-8")
        except ValueError:
            print("Error: Couldn't retrieve channel (" + self.name + ") JSON data, bot is temporarily unable to operate on this channel.")
            self.error = True
            return
        self.error = False
        # Capture the received data into our data_json object
        jdata = json.loads(data)
        # Assign all the indices into our member lists
        self.chatter_count = jdata["chatter_count"]
        self.moderators = jdata["chatters"]["moderators"]
        self.staff = jdata["chatters"]["staff"]
        self.admins = jdata["chatters"]["admins"]
        self.global_mods = jdata["chatters"]["global_mods"]
        self.viewers = jdata["chatters"]["viewers"]

    # Save Mario Maker level data into a txt file
    def saveLevels(self):
        file = open("chandata/mmaker_played_" + self.name + ".cfg", "w")
        for level in self.mmaker_levels_pld:
            file.write(level.code + " " + level.user + "\n")
        file.close()
        file = open("chandata/mmaker_unplyd_" + self.name + ".cfg", "w")
        for level in self.mmaker_levels_upl:
            file.write(level.code + " " + level.user + "\n")
        file.close()

    # Load Mario Maker level data from a txt file
    def loadLevels(self):
        fileExists("chandata/mmaker_played_" + self.name + ".cfg")
        fileExists("chandata/mmaker_unplyd_" + self.name + ".cfg")
        file = open("chandata/mmaker_played_" + self.name + ".cfg", "r")
        for line in file:
            lsplit = str.split(line, " ")
            code = lsplit[0]
            user = str.split(lsplit[1], "\n")[0]
            self.mmaker_levels_pld.append(MMakerLevel(code, user))
        file.close()
        file = open("chandata/mmaker_unplyd_" + self.name + ".cfg", "r")
        for line in file:
            lsplit = str.split(line, " ")
            code = lsplit[0]
            user = str.split(lsplit[1], "\n")[0]
            self.mmaker_levels_upl.append(MMakerLevel(code, user))
        file.close()
