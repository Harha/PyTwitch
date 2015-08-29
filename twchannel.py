# Library imports
import string

class TWChannel(object):

    # Class constructor
    def __init__(self, name):
        self.name = name
        self.users = [None]
        self.cmdsent = 0

    # For printing the object
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
