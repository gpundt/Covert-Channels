# NAME: Griffin Pundt
# DATE: 9/17/2024
# PURPOSE: this covert channel will send a hidden message between the sender and receiver by making subtle changes to the /tmp directory
# REQUIREMENTS: Python3, any Linux OS

# EXPLANATION:
    1) block_sender.py prompts a user for a message
        e.g. "hello"
    2) block_sender.py creates multiple files in /tmp, each file contains an encoded character in the message
        e.g. text.Sh34UkHJ89
             text.K7Ihbg3Yw1
             ...
    3) block_sender.py creates a signal file, signalling to the receiver that the message is ready for reading
        e.g. sender.signal
    4) block_receiver.py is listening in /tmp for sender.signal
    5) When block_receiver.py detects sender.signal, it pulls all encoded message files and pieces together the message
        (All message files are deleted after they're used)
    6) Once block_receiver.py generates the encoded message and all used files are deleted, it creates a signal file for the sender
        e.g. receiever.signal
    7) block_sender.py detects receiever.signal, understands that the message has been reading
    8) block_sender.py deletes receiever.signal, severing the communciation channel 