#!/usr/bin/env python3

# NAME: Griffin Pundt
# DATE: 9/19/2024
# PURPOSE: This program edits photo metadata to contain encoded messages
    # Messages will be decoded and read by photo_metadata_read.py
# OS REQUIREMENTS: Debian-based Linux (Kali, Ubuntu, Debian)

import os
import exif
import time

filepath = '<FULL PATH TO PHOTO>'
img = exif.Image(filepath)
empty_tags = []
encoded_messages = []

#####################
##### Mode == 1 #####
# Function will list all exif data of desired image
def check_exif(img : exif.Image):
    clear_terminal()
    print("[*] Checking for Image Metadata... [*]")
    if img.has_exif:
        print("The image contains EXIF information!\n")
        exif_tags = print_exif_tags(img)
        print_exif_data(img, exif_tags)
        if len(encoded_messages) > 0:
            print("\n[*] Encoded Message(s) Detected!! [*]")
        #list_available_tags(empty_tags)
        wait_for_input()
        return
    print("Exif info not found...\n")
    

# Function prints metadata tags
def print_exif_tags(img: exif.Image):
    print("[*] Displaying Exif Tags [*]")
    exif_tags = dir(img)
    
    for tag in exif_tags:
        if "<unknown EXIF tag" in tag:
            exif_tags.remove(tag)
            
    print(exif_tags)
    return exif_tags

# Function prints metadata
def print_exif_data(img : exif.Image, tags):
    print("\n[*] Displaying Exif Data [*]")
    for tag in tags:
        data = img.get(tag)
        if data is not None:
            if len(str(data)) < 500:
                print(str(tag) + ":\t" + str(data))
                if "**&**$$474" in str(data) and str(data) not in encoded_messages:
                    encoded_messages.append(str(data))
        else:
            empty_tags.append(tag)
            print(tag + ":\tEMPTY")
    
     
# Function prints metadata tags with no value, indicating these
# can be modified to contain encoded message
def list_available_tags(tag_list):
    print("\n[*] Listing Tags Available for Modification [*]")
    for tag in tag_list:
        print(tag)
##### Mode == 1 #####
#####################

#####################
##### Mode == 2 #####
def decode_message():
    exif_tags = dir(img)
    for tag in exif_tags:
        data = img.get(tag)
        if "**&**$$474" in str(data) and str(data) not in encoded_messages:
            encoded_messages.append(str(data))
    print("\n[*] Displaying Encoded Messages [*]")
    for message in encoded_messages:
        print("Message:\t", message)
        message = message[10:]
        decoded = bytes.fromhex(message).decode("utf-8")
        print("Decoded Message:\t", decoded)
        print("\n")
    wait_for_input()

##### Mode == 2 #####
#####################

#########################
### Utility Functions ###
def select_mode():
    clear_terminal()
    mode = input("1) Read Exif\n2) Decode Message\n3) Quit\n>>>\t")
    return mode

def exit_program():
    clear_terminal()
    print("Goodbye!")
    time.sleep(2)
    clear_terminal()

def wait_for_input():
    input("\n\n[*] Press ENTER to Continue... [*]\n")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def start(img : exif.Image):
    clear_terminal()
    print("[*] Photo Metadata Edit Tool [*]")
    mode = select_mode()
    while mode != "3":
        if mode == "1":
            check_exif(img)
        elif mode == "2":
            decode_message()
        else:
            clear_terminal()
            start(img)
        mode = select_mode()
    exit_program()
### Utility Functions ###
#########################


def main():
    start(img)


if __name__ == "__main__":
    main()