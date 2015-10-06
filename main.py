# Library imports
import sys
import socket
import string
import threading
import random
import time

# Class imports
from config import *
from twchannel import *
from mmakerlevel import *

# Networking related variables / objects
SOCKET = socket.socket()
RBUFFR = ""
RECMDS = ""

## Bot channel Commands Below
# Help request
def botchan_help(channel, nick, cmds):
    sendRsp(channel, nick, "Commands: " + str(list(TWITCH_COMMANDS_BOTCHAN.keys())))

# Register a channel for user
def botchan_register(channel, nick, cmds):
    registerChannel(nick)
    sendRsp(channel, nick, "Your channel has been registered successfully!")

# Unregister a channel for user
def botchan_unregister(channel, nick, cmds):
    unregisterChannel(nick)
    sendRsp(channel, nick, "Your channel has been unregistered successfully!")

# HashMap of command function hooks
TWITCH_COMMANDS_BOTCHAN = {"help":botchan_help, "register":botchan_register, "unregister":botchan_unregister}

## Global Commands Below
# Help request
def global_help(channel, nick, cmds):
    sendRsp(channel, nick, "Commands: " + str(list(TWITCH_COMMANDS_GLOBAL.keys())) + " | " + botstaff_help() + " | " + mmaker_help())

# User amount request
def global_users(channel, nick, cmds):
    if len(cmds) <= 4:
        sendRsp(channel, nick, "Users on this channel: " + str(getChatterCount(channel)))
    else:
        subcomm = cmds[4]
        if subcomm == "all":
            chattercount = 0
            for key in TWITCH_CHANNELS_CND:
                chattercount += getChatterCount(key)
            sendRsp(channel, nick, "Users on all channels: " + str(chattercount))
        else:
            if subcomm.startswith('#') == False:
                subcomm = "#" + subcomm
            chattercount = getChatterCount(subcomm)
            if chattercount != None:
                sendRsp(channel, nick, "Users on (" + subcomm + "): " + str(chattercount))
            else:
                sendRsp(channel, nick, "Invalid channel! (" + subcomm + ")")

# Channel list info request
def global_chans(channel, nick, cmds):
    if len(cmds) <= 4:
        sendRsp(channel, nick, "Registered channels: " + str(len(TWITCH_CHANNELS_RGD)))
    else:
        subcomm = cmds[4]
        if subcomm == "registered":
            sendRsp(channel, nick, "Registered channels: " + str(len(TWITCH_CHANNELS_RGD)))
        elif subcomm == "connected":
            sendRsp(channel, nick, "Connected channels: " + str(len(TWITCH_CHANNELS_CND)))

# HashMap of command function hooks
TWITCH_COMMANDS_GLOBAL = {"help":global_help, "commands":global_help, "users":global_users, "chans":global_chans}

## Bot staff Commands Below
# Help request
def botstaff_help():
    return str(list(TWITCH_COMMANDS_BSTAFF.keys()))

# Add a bot staff member
def botstaff_addstaffmember(channel, nick, cmds):
    if len(cmds) > 4:
        addBotStaffMember(cmds[4])
        sendRsp(channel, nick, "User (" + cmds[4] + ") has been added to the bot staff member list.")

# Remove a bot staff member
def botstaff_remstaffmember(channel, nick, cmds):
    if len(cmds) > 4:
        remBotStaffMember(cmds[4])
        sendRsp(channel, nick, "User (" + cmds[4] + ") has been removed from the bot staff member list.")

# Force bot to join a channel
def botstaff_join(channel, nick, cmds):
    if len(cmds) > 4:
        subcomm = cmds[4]
        if subcomm.startswith('#') == False:
            subcomm = "#" + subcomm
        sendRaw("JOIN", subcomm)
        sendRsp(channel, nick, "Bot has been forced to join channel " + subcomm + ".")

# Force bot to part a channel
def botstaff_part(channel, nick, cmds):
    if len(cmds) > 4:
        subcomm = cmds[4]
        if subcomm.startswith('#') == False:
            subcomm = "#" + subcomm
        sendRaw("PART", subcomm)
        sendRsp(channel, nick, "Bot has been forced to part channel " + subcomm + ".")

# Force the bot to say a message in given channel
def botstaff_say(channel, nick, cmds):
    if len(cmds) > 5:
        subcomm = cmds[4]
        if subcomm.startswith('#') == False:
            subcomm = "#" + subcomm
        sendMsg(subcomm, " ".join(cmds[5::]))

# Force the bort to broadcast a message to all channels
def botstaff_broadcast(channel, nick, cmds):
    if len(cmds) > 4:
        for key in TWITCH_CHANNELS_CND:
            sendMsg(key, " ".join(cmds[4::]))

# Register a channel for user
def botstaff_addchan(channel, nick, cmds):
    if len(cmds) > 4:
        subcomm = cmds[4]
        if subcomm.startswith('#') == False:
            subcomm = "#" + subcomm
        registerChannel(subcomm.lower())
        sendRsp(channel, nick, "Bot has been forced to register channel " + subcomm + ".")

# Unregister a channel for user
def botstaff_remchan(channel, nick, cmds):
    if len(cmds) > 4:
        subcomm = cmds[4]
        if subcomm.startswith('#') == False:
            subcomm = "#" + subcomm
        unregisterChannel(subcomm.lower())
        sendRsp(channel, nick, "Bot has been forced to unregister channel " + subcomm + ".")

# HashMap of command function hooks
TWITCH_COMMANDS_BSTAFF = {"addstaff":botstaff_addstaffmember, "remstaff":botstaff_remstaffmember, "join":botstaff_join, "part":botstaff_part, "say":botstaff_say, "broadcast":botstaff_broadcast, "addchan":botstaff_addchan, "remchan":botstaff_remchan}

# Mario Maker module commands Below
# Help request
def mmaker_help():
    return str(list(TWITCH_COMMANDS_MMAKER.keys()))

# Broadcast the current mario maker level on the channel
def mmaker_level(channel, nick, cmds):
    sendRsp(channel, nick, "The current level is (" + TWITCH_CHANNELS_CND[channel].mmaker_level_crnt.code + ") by (" +  TWITCH_CHANNELS_CND[channel].mmaker_level_crnt.user + ").")

# Print out level information
def mmaker_levels(channel, nick, cmds):
    sendRsp(channel, nick, "Unplayed levels: " + str(len(TWITCH_CHANNELS_CND[channel].mmaker_levels_upl)) + " Played levels: " + str(len(TWITCH_CHANNELS_CND[channel].mmaker_levels_pld)))

# Add a new mario maker level to the unplayed list
def mmaker_addlevel(channel, nick, cmds):
    if len(cmds) > 4:
        subcomm = cmds[4]
        if len(subcomm) < 19 or len(subcomm) > 20:
            return
        if not "-0000-" in subcomm:
            return
        n = 0
        for level in TWITCH_CHANNELS_CND[channel].mmaker_levels_upl:
            if level.user.lower() == nick.lower():
                n += 1
            if level.code.lower() == subcomm.lower(): # no duplicates
                return
            elif n > TWITCH_CHANNELS_CND[channel].mmaker_levels_max: # max level amount set by channel host
                return
        for level in TWITCH_CHANNELS_CND[channel].mmaker_levels_pld:
            if level.code.lower() == subcomm.lower():
                return
        TWITCH_CHANNELS_CND[channel].mmaker_levels_upl.append(MMakerLevel(subcomm, nick))
        TWITCH_CHANNELS_CND[channel].saveLevels()
        sendRsp(channel, nick, "a New level was added to the list.")

# Choose a random mario maker level to played
def mmaker_choose(channel, nick, cmds):
    if nick != channel.lstrip("#"):
        return
    if len(cmds) <= 4:
        levels = TWITCH_CHANNELS_CND[channel].mmaker_levels_upl
        amount = len(levels)
        if amount <= 0:
            sendRsp(channel, nick, "Cannot choose level; The unplayed levels list is empty.")
            return
        randnm = random.randrange(0, amount, 1)
        level = levels[randnm]
        TWITCH_CHANNELS_CND[channel].mmaker_level_crnt = level
        TWITCH_CHANNELS_CND[channel].mmaker_levels_upl.remove(level)
        TWITCH_CHANNELS_CND[channel].mmaker_levels_pld.append(level)
        TWITCH_CHANNELS_CND[channel].saveLevels()
        count = str(len(TWITCH_CHANNELS_CND[channel].mmaker_levels_pld))
        sendRsp(channel, nick, "The current level was set to #" + count + " (" + level.code.upper() + ") by (" + level.user + ").")

# Clear all levels
def mmaker_clearlevels(channel, nick, cmds):
    if nick != channel.lstrip("#"):
        return
    TWITCH_CHANNELS_CND[channel].mmaker_levels_upl = []
    TWITCH_CHANNELS_CND[channel].mmaker_levels_pld = []
    TWITCH_CHANNELS_CND[channel].saveLevels()
    sendRsp(channel, nick, "Cleared all played & unplayed levels from current channel!")

# Set max levels per user limit
def mmaker_maxlevels(channel, nick, cmds):
    if len(cmds) <= 4:
        sendRsp(channel, nick, "Max amount of unplayed levels per user is (" + str(TWITCH_CHANNELS_CND[channel].mmaker_levels_max + 1) + ").")
        return
    if nick != channel.lstrip("#"):
        return
    if len(cmds) > 4:
        n = int(cmds[4])
        n = max(n, 1)
        TWITCH_CHANNELS_CND[channel].mmaker_levels_max = n
        TWITCH_CHANNELS_CND[channel].saveSettings()
        sendRsp(channel, nick, "Changed max amount of unplayed levels per user to " + str(n) + ".")

# HashMap of command function hooks
TWITCH_COMMANDS_MMAKER = {"level":mmaker_level, "levels":mmaker_levels, "addlevel":mmaker_addlevel, "chooselevel":mmaker_choose, "clearlevels":mmaker_clearlevels, "maxlevels":mmaker_maxlevels}

# Send a message to the socket
def sendRaw(message, data):
    sdata = bytes(message + " %s\r\n" % data, "UTF-8")
    SOCKET.send(sdata)
    print(sdata.decode(), end = "")

# Send a chat message to given channel
def sendMsg(channel, message):
    global TWITCH_MSGS_RATE
    rate = 40
    if isModeratorOnChannel(TWITCH_USER, channel) or channel in TWITCH_USER:
        rate = TWITCH_MSGS_PER_MINUTE_MOD
    else:
        rate = TWITCH_MSGS_PER_MINUTE_NRM
    if TWITCH_MSGS_RATE >= rate - 1:
        print("Error: Message rate exceeded! Message (" + message + ") wasn't sent.")
        return
    TWITCH_MSGS_RATE += 1
    sendRaw("PRIVMSG", channel + " :" + message)

# Sends a chat response message to given user in a given channel
def sendRsp(channel, user, message):
    sendMsg(channel, user + " -> " + message)

# Handle the message PART
def handlePART(cmds):
    # Get the sender's username & mail
    info_s = str.split(cmds[0], "!")
    info_s[0] = str.lstrip(info_s[0], ':')
    nick_s = info_s[0]
    mail_s = info_s[1]
    chan_s = cmds[2]
    # Check if it's the bot itself
    if TWITCH_USER == nick_s:
        TWITCH_CHANNELS_CND[chan_s].running = False
        del TWITCH_CHANNELS_CND[chan_s]

# Handle the message 353
def handle353(cmds):
    # Parse the message
    channel = cmds[4]
    # Add the channel to TWITCH_CHANNELS and start new thread for it
    TWITCH_CHANNELS_CND[channel] = TWChannel(channel, TWITCH_CHATTERS_FREQU)
    TWITCH_CHANNELS_CND[channel].running = True
    TWITCH_CHANNELS_CND[channel].thread.start()

# Handle the message 376
def handle376(cmds):
    # Request additional information via messages
    sendRaw("CAP REQ", TWITCH_MEMR)
    sendRaw("CAP REQ", TWITCH_CMDR)
    # Connect to all registered channels
    for key in TWITCH_CHANNELS_RGD:
        sendRaw("JOIN", TWITCH_CHANNELS_RGD[key])

# Handle the message PING
def handlePING(cmds):
    sendRaw("PONG", cmds[1])

# Handle the message PRIVMSG
def handlePRIVMSG(cmds):
    # Get the sender's username & mail
    info_s = str.split(cmds[0], "!")
    info_s[0] = str.lstrip(info_s[0], ':')
    nick_s = info_s[0]
    mail_s = info_s[1]
    # Parse the message
    channel = cmds[2]
    cmds[3] = str.lstrip(cmds[3], ':')
    command = cmds[3]
    # Check if the current channel state is in ERROR or not, return if True
    if TWITCH_CHANNELS_CND[channel].error == True:
        return
    # Handle the message, first check for command
    if command.startswith("!") and len(command) > 2 and len(command) < 20:
        command = str.lstrip(command, '!')
        # First, handle commands on bot's own channel
        if "#" + TWITCH_USER == channel:
            try:
                TWITCH_COMMANDS_BOTCHAN[command](channel, nick_s, cmds)
            except KeyError:
                pass
        # Then, handle all global commands
        try:
            TWITCH_COMMANDS_GLOBAL[command](channel, nick_s, cmds)
        except KeyError:
            pass
        # Then, handle mario maker related commands
        try:
            TWITCH_COMMANDS_MMAKER[command](channel, nick_s, cmds)
        except KeyError:
            pass
        # Then, handle bot staff member commands
        if isBotStaffMember(nick_s):
            try:
                TWITCH_COMMANDS_BSTAFF[command](channel, nick_s, cmds)
            except KeyError:
                pass

# Handle all messages sent to our bot
def handleMessages(lines):
    for index, i in enumerate(lines):
        # Split the current line with spaces
        cmds = str.split(lines[index], " ")
        # PART message
        if cmds[1] == "PART":
            handlePART(cmds)
        # Succesful channel join message
        elif cmds[1] == "353":
            handle353(cmds)
        # After connected, do the initialization procedure
        elif cmds[1] == "376":
            handle376(cmds)
        # Handle PING PONG heart pulse
        elif cmds[0] == "PING":
            handlePING(cmds)
        # Handle PRIVMSG
        elif cmds[1] == "PRIVMSG":
            handlePRIVMSG(cmds)

# Get the chatter list from given channel
def getChatterList(channel):
    chatterlist = None
    try:
        chatterlist = TWITCH_CHANNELS_CND[channel].viewers
    except KeyError:
        print("Error: Invalid channel key (" + channel + "), channel not found!")
    return chatterlist

# Get the chatter count from given channel
def getChatterCount(channel):
    chattercount = None
    try:
        chattercount = TWITCH_CHANNELS_CND[channel].chatter_count
    except KeyError:
        print("Error: Invalid channel key (" + channel + "), channel not found!")
    return chattercount

# Get the played mario maker levels from given channel
def getMMakerPlayed(channel):
    mmakerplayed = None
    try:
        mmakerplayed = TWITCH_CHANNELS_CND[channel].mmaker_levels_pld
    except KeyError:
        print("Error: Invalid channel key (" + channel + "), channel not found!")
    return mmakerplayed

# Get the unplayed mario maker levels from given channel
def getMMakerUnplayed(channel):
    mmakerunplayed = None
    try:
        mmakerunplayed = TWITCH_CHANNELS_CND[channel].mmaker_levels_upl
    except KeyError:
        print("Error: Invalid channel key (" + channel + "), channel not found!")
    return mmakerunplayed

# Register a new channel
def registerChannel(channel):
    if channel.startswith('#') == False:
        channel = "#" + channel
    TWITCH_CHANNELS_RGD[channel] = TWChannel(channel, TWITCH_CHATTERS_FREQU)
    sendRaw("JOIN", TWITCH_CHANNELS_RGD[channel])
    saveChannelData()
    print("a New channel was registered! (" + channel + ")")

# Unregister a channel
def unregisterChannel(channel):
    if channel.startswith('#') == False:
        channel = "#" + channel
    if channel not in TWITCH_CHANNELS_RGD:
        return
    del TWITCH_CHANNELS_RGD[channel]
    sendRaw("PART", channel)
    saveChannelData()
    print("a Channel has been unregistered! (" + channel + ")")

# Add a new bot staff member
def addBotStaffMember(nick):
    TWITCH_BOT_STAFF[nick] = nick
    saveStaffData()
    print("a New bot staff member was added! (" + nick + ")")

# Remove a bot staff member
def remBotStaffMember(nick):
    if nick not in TWITCH_BOT_STAFF:
        return
    del TWITCH_BOT_STAFF[nick]
    saveStaffData()
    print("a Bot staff member was removed! (" + nick + ")")

# Check if nick is a bot staff member
def isBotStaffMember(nick):
    if nick in TWITCH_BOT_STAFF:
        return True
    return False

# Check if nick is a moderator on channel
def isModeratorOnChannel(nick, channel):
    moderators = None
    try:
        moderators = TWITCH_CHANNELS_CND[channel].moderators
    except KeyError:
        print("Error: Invalid channel key (" + channel + "), channel not found!")
        return False
    if nick in moderators:
        return True
    return False

# Scheluded 1 second interval jobs
def scheluded_ones_jobs():
    global TWITCH_MSGS_RATE
    while True:
        if TWITCH_MSGS_RATE > 0:
            TWITCH_MSGS_RATE -= 1
        time.sleep(1)

# Main function
def main():
    # Global variable definitions
    global SOCKET
    global RBUFFR
    global RECMDS
    global TWITCH_CHATTERS_TIMER
    global TWITCH_CHATTERS_FREQU
    # Seed global rng
    random.seed(None)
    # Setup scheduled jobs
    one_second_jobs = threading.Thread(target = scheluded_ones_jobs)
    one_second_jobs.start()
    # Load bot configuration
    loadChannelData()
    loadStaffData()
    # Initially connect to the chat servers
    SOCKET.connect((TWITCH_HOST, TWITCH_PORT))
    # Send authorization information to the servers
    sendRaw("PASS", TWITCH_AUTH)
    sendRaw("USER", TWITCH_USER)
    sendRaw("NICK", TWITCH_USER)
    # Main loop
    while True:
        # Allocate a buffer and read data from socket and store it in it
        RBUFFR = RBUFFR + SOCKET.recv(1024).decode("UTF-8", "ignore")
        RECMDS = str.split(RBUFFR, "\n")
        RBUFFR = RECMDS.pop()
        # Iterate through all received messages
        for line in RECMDS:
            line = str.rstrip(line)
            line = str.lstrip(line)
            lines = str.split(line, "\r\n")
            # First, print the received messages
            for index, i in enumerate(lines):
                print(lines[index].encode("cp850", errors = "replace").decode("cp850"), end = "\n", flush = True)
            # Then, Handle messages
            handleMessages(lines)
    # Close the socket before exit
    SOCKET.close()

# Function hooks
if __name__ == "__main__":
    main()
