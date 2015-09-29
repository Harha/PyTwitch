# Library imports
import os

# Check if a file exists, if not then create it
def fileExists(filename):
    if not os.path.exists(filename):
        open(filename, "w").close()
