#!/usr/bin/env python3

# Name: Griffin Pundt
# Class: CSEC 750 - Covert Communication
# Purpose: this program will monitor changes to the /tmp directory and piece together a message from the sender
import os
from pathlib import Path


# Function that listens for changes in /tmp
# Once signal is detected, reads covert message
def listen():
    print("[*] Listening for Sender Signal... [*]")
    signal_file = Path("/tmp/sender.signal")
    while signal_file.is_file() != True:
        pass
    print("[*] Signal Detected! Reading message... [*]")
    read_message()


# Reads covert message, afterwards erases all files used in message
# Makes signal file to indicate message has been read
def read_message():
    os.remove("/tmp/sender.signal")
    search_dir = "/tmp/"
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))

    message = ""
    for filename in files:
        if '/tmp/text.' in filename:
            file = open(filename)
            lines = file.read()
            last_line = lines[-1]
            last_char = last_line[-1]
            message += last_char
            file.close()
            os.remove(filename)
    print("[*] Message Received! [*]")
    print("Message:\t '" + message + "'")
    print("\n\n[*] Sending Signal to Sender and Closing! [*]")
    make_signal_file()


# Makes signal to sender indicating messgae has been read
def make_signal_file():
    filename = "/tmp/receiver.signal"
    open(filename, "a").close()


def main():
    listen()


if __name__ == "__main__":
    main()