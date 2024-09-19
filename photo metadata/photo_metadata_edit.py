#!/usr/bin/env python3

# NAME: Griffin Pundt
# DATE: 9/19/2024
# PURPOSE: This program edits photo metadata to contain encoded messages
    # Messages will be decoded and read by photo_metadata_read.py
# OS REQUIREMENTS: Debian-based Linux (Kali, Ubuntu, Debian)

import os
import exif
import time

# Full path of image
filepath = '<FULL PATH TO PHOTO>'
img = exif.Image(filepath)
empty_tags = []


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
#When mode 2 is selected, execute esit_exif
def edit_exif(img : exif.Image):
    clear_terminal()
    empty_tags = []
    tags = dir(img)
    for tag in tags:
        data = img.get(tag)
        if isinstance(data, str):
            empty_tags.append(tag)
    list_available_tags(empty_tags)
    tag_to_modify = select_empty_tag(empty_tags)
    if tag_to_modify is not None:
        print("[*] Selected Tag: " + tag_to_modify + " [*]")
        message = get_user_message()
        encoded = encode_message(message)
        print("\n[*] Injecting Encoded Message into Selected Tag: " + tag_to_modify + " [*]")
        inject_encoded_message(img, encoded, tag_to_modify)
        save_changes(img)
    else:
        wait_for_input()
        start(img)

# prompts user for message that will be embedded in photo metadata
def get_user_message():
    message = input("\n[*] Prompting User Message [*]\nInput Message >>>\t")
    return message

#encodes message in hex and prepends a hardcoded prefix
def encode_message(message):
    prefix = "**&**$$474"
    print("[*] Message Prefix: " + prefix + " [*]\n")
    
    encoded = message.encode("utf-8").hex()
    encoded = prefix + encoded
    print("[*] Encoded Message with Prefix [*]\n", encoded)
    return encoded
    
# changes metadata to contain encoded message
def inject_encoded_message(img : exif.Image, encoded, tag_to_modify):
    wait_for_input()
    img.set(tag_to_modify, encoded)
    print("[*] Encoded Message Injected! [*]\n")
    #img.set(str(tag_to_modify).strip(), encoded)
   # print("[*] Encoded Message Injected! [*]")

# overwrites changes to original photo
def save_changes(img):
    print("[*] Saving Changes! [*]\n\n")
    with open(filepath, "wb") as image:
        image.write(img.get_file())
    print("[*] Changes Saved! [*]")
    wait_for_input()

# Prompts user to select which metadata tag they want to embed message
def select_empty_tag(tag_list):
    print("\n[*] Select Tag to Modify [*]")
    number = 1
    for tag in tag_list:
        line = "" + str(number) + ") " + str(tag)
        print(line)
        number += 1
    selection = input(">>>\t")
    try:
        selection = int(selection)
    except ValueError:
        print("VALUE ERROR")
        return None
    try:
        #print(tag_list)
        tag_to_modify = tag_list[selection - 1]
        return tag_to_modify
    except IndexError:
        print("INDEX ERROR")
        return None
##### Mode == 2 #####
#####################


#########################
### Utility Functions ###
# Prompts user for which mode they want
def select_mode():
    clear_terminal()
    mode = input("1) Read Exif\n2) Edit Metadata\n3) Quit\n>>>\t")
    return mode

# exits program
def exit_program():
    clear_terminal()
    print("Goodbye!")
    time.sleep(2)
    clear_terminal()

# prompts user before continuing
def wait_for_input():
    input("\n\n[*] Press ENTER to Continue... [*]\n")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# executes program start sequence
def start(img : exif.Image):
    clear_terminal()
    print("[*] Photo Metadata Edit Tool [*]")
    mode = select_mode()
    while mode != "3":
        if mode == "1":
            check_exif(img)
        elif mode == "2":
            edit_exif(img)
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