# Library imports
import string
import json
import time
import threading

# Class imports
from config import *
from twurlopener import *

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
        self.chatter_count = 0
        self.moderators = None
        self.staff = None
        self.admins = None
        self.global_mods = None
        self.viewers = None
        # Create urlopeners for receiving json data
        self.urlopener_chatters = TWURLOpener()
        self.urlopener_chatters.addheader("Accept", "application/vnd.twitchtv.v3+json")

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
