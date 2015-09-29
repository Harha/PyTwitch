# Library imports
import string

# Class imports
from config import *

class MMakerLevel(object):

    # Class constructor
    def __init__(self, code, user):
        # Assign input variables to member variables
        self.code = code.lower()
        self.user = user.lower()

    # For printing the object
    def __str__(self):
        return self.code
    def __repr__(self):
        return self.code
