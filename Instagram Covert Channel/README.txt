# Title: Instagram Covert Channel Proof of Concept
# Authors: Griffin Pundt & Kora Lovdahl
# Class: CSEC-750 Covert Communcations
# Notes: This repository contains proof of concept code to show Instagram's functionality as a covert communication channel

# SETUP:
1) Install / upgrade dependencies
  - python3 -m pip install -r ./requirements.txt

2) Edit PostBot.py and PostReceiver.py to contain valid Instagram login credentials
  - username, password = "<USERNAME>", "<PASSWORD>"

3) Edit PostBot.py self.base_filepath variable to point to photo directory
  - self.base_filepath = "/path/to/photos"

4) Run PostBot.py to create a new post with an encoded message
  - python3 PostBot.py

5) Run PostReceiver.py to receive encoded message from sender account
  - python3 PostReceiver.py
