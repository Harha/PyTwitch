# Library imports
import sys
import socket
import string

# Class imports
from twchannel import *

# Twitch chat server related constants
TWITCH_HOST = "irc.twitch.tv"
TWITCH_PORT = 6667
TWITCH_USER = "BOTNAME"
TWITCH_AUTH = "oauth:xxxxxxxxxxxxxxxx"
TWITCH_MEMR = ":twitch.tv/membership"
TWITCH_CMDR = ":twitch.tv/commands"
TWITCH_TAGR = ":twitch.tv/tags"

# Networking related variables / objects
SOCKET = socket.socket()
RBUFFR = ""
RECMDS = ""

# Twitch chat handling related variables / objects
TWITCH_CHANNELS_RGD = [TWChannel("#" + TWITCH_USER)]
TWITCH_CHANNELS_CND = {}
TWITCH_CHATTERS_TIMER = 0
TWITCH_CHATTERS_FREQU = 10

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

# Handle the message 353
def handle353(cmds):
    # Parse the message
    channel = cmds[4]
    # Add the channel to TWITCH_CHANNELS
    TWITCH_CHANNELS_CND[channel] = (TWChannel(channel))

# Handle the message 376
def handle376(cmds):
    # Request additional information via messages
    sendRaw("CAP REQ", TWITCH_MEMR)
    sendRaw("CAP REQ", TWITCH_CMDR)
    # Connect to all registered channels
    for index, i in enumerate(TWITCH_CHANNELS_RGD):
        sendRaw("JOIN", TWITCH_CHANNELS_RGD[index])

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
    # Handle the message, first check for command
    if (command.startswith("!") and len(command) > 2) and len(command) < 16:
        command = str.lstrip(command, '!')
        if (command == "connected"):
            sendRsp(channel, nick_s, "Connected channels: " + str(TWITCH_CHANNELS_CND))
        elif (command == "registered"):
            sendRsp(channel, nick_s, "Registered channels: " + str(TWITCH_CHANNELS_RGD))
        elif (command == "users"):
            sendRsp(channel, nick_s, "Users on this channel: " + str(TWITCH_CHANNELS_CND[channel].viewers))
        else:
            sendRsp(channel, nick_s, "Invalid command (" + command + ").")

# Handle all messages sent to our bot
def handleMessages(lines):
    for index, i in enumerate(lines):
        # Split the current line with spaces
        cmds = str.split(lines[index], " ")
        # Succesful channel join message
        if (cmds[1] == "353"):
            handle353(cmds)
        # After connected, do the initialization procedure
        elif (cmds[1] == "376"):
            handle376(cmds)
        # Handle PING PONG heart pulse
        elif (cmds[0] == "PING"):
            handlePING(cmds)
        # Handle PRIVMSG
        elif (cmds[1] == "PRIVMSG"):
            handlePRIVMSG(cmds)

# Main function
def main():
    # Global variable definitions
    global SOCKET
    global RBUFFR
    global RECMDS
    global TWITCH_CHATTERS_TIMER
    global TWITCH_CHATTERS_FREQU
    # Initially connect to the chat servers
    SOCKET.connect((TWITCH_HOST, TWITCH_PORT))
    # Send authorization information to the servers
    sendRaw("PASS", TWITCH_AUTH)
    sendRaw("USER", TWITCH_USER)
    sendRaw("NICK", TWITCH_USER)
    # Main loop
    while True:
        # Allocate a buffer and read data from socket and store it in it
        RBUFFR = RBUFFR + SOCKET.recv(1024).decode("UTF-8")
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
        # Update CHATTERS list in each channel
        if (TWITCH_CHATTERS_TIMER <= 0):
            for key in TWITCH_CHANNELS_CND:
                TWITCH_CHANNELS_CND[key].getchatters()
            TWITCH_CHATTERS_TIMER = TWITCH_CHATTERS_FREQU
        # Decrease CHATTERS list update timer
        TWITCH_CHATTERS_TIMER -= 1
    # Close the socket before exit
    SOCKET.close()

# Function hooks
if __name__ == "__main__":
    main()
