#!/usr/bin/env python3

# Name: Griffin Pundt
# Class: CSEC 750 - Covert Communication
# Purpose: This program will make changes to the /tmp directory in accordance to an input message
import os
from pathlib import Path
import string
import random
import time


# wordlists used to create filenames and file contents
char_list = string.ascii_letters + string.digits
ascii_list = string.printable


# Prompts user for message
def input_message():
    plaintext = input("Enter message to send:\t")
    return plaintext


# Using user prompt, creates message files in /tmp
# Once message has been sent, waits for receiver's signal
def generate_message(message):
    print("\nMessage: '" + message + "'")
    for char in message:
        make_file(char)
    make_signal_file()
    print("[*] Files Created in /tmp [*]")
    print("[*] Waiting for Receiver Signal... [*]")
    listen()
    print("[*] Message Received! [*]")
    
    
# makes a file in /tmp to signal the receiver to begin reading
def make_signal_file():
    filename = "/tmp/sender.signal"
    open(filename, "a").close()


# Listens for receiver's signal, indicating message has been read
# deletes signal file, removing existance of communication
def listen():
    signal_file = Path("/tmp/receiver.signal")
    while signal_file.is_file() != True:
        pass
    os.remove("/tmp/receiver.signal")


# Creates files in /tmp containing encoded message
def make_file(letter):
    filename = "/tmp/text."
    for _ in range(10):
        filename += random.choice(char_list)

    file_contents = ""
    for _ in range(50):
        file_contents += random.choice(ascii_list)       
    file_contents += letter

    f = open(filename, "w")
    f.write(file_contents)
    f.close()
    #sleep to ensure timestamps are different
    time.sleep(.1)


def main():
    message = input_message()
    generate_message(message)


if __name__ == "__main__":
    main()