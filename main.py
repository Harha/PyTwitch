# Library imports
import sys
import socket
import string
import threading

# Class imports
from config import *
from twchannel import *

# Networking related variables / objects
SOCKET = socket.socket()
RBUFFR = ""
RECMDS = ""

## Bot channel Commands Below
# Help request
def botchan_help(channel, nick, cmds):
    sendRsp(channel, nick, "Available commands: " + str(TWITCH_COMMANDS_BOTCHAN))

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
    sendRsp(channel, nick, "Available commands: " + str(TWITCH_COMMANDS_GLOBAL))

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

# HashMap of command function hooks
TWITCH_COMMANDS_GLOBAL = {"help":global_help, "users":global_users}

# Send a message to the socket
def sendRaw(message, data):
    sdata = bytes(message + " %s\r\n" % data, "UTF-8")
    SOCKET.send(sdata)
    print(sdata.decode(), end = "")

# Send a chat message to given channel
def sendMsg(channel, message):
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
    if command.startswith("!") and len(command) > 2 and len(command) < 16:
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

# Main function
def main():
    # Global variable definitions
    global SOCKET
    global RBUFFR
    global RECMDS
    global TWITCH_CHATTERS_TIMER
    global TWITCH_CHATTERS_FREQU
    # Load bot configuration
    loadChannelData()
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
