import binascii
import EmojiList
import random


# Map each hexadecimal digit to a list of corresponding emojis
# This allows for random selection from a variety of emojis for each digit
end_chars = {
    "0": EmojiList.emojis_0, 
    "1": EmojiList.emojis_1, 
    "2": EmojiList.emojis_2, 
    "3": EmojiList.emojis_3, 
    "4": EmojiList.emojis_4, 
    "5": EmojiList.emojis_5, 
    "6": EmojiList.emojis_6, 
    "7": EmojiList.emojis_7, 
    "8": EmojiList.emojis_8, 
    "9": EmojiList.emojis_9,
    "A": EmojiList.emojis_A, 
    "B": EmojiList.emojis_B, 
    "C": EmojiList.emojis_C, 
    "D": EmojiList.emojis_D, 
    "E": EmojiList.emojis_E, 
    "F": EmojiList.emojis_F
}

# Filler words break up the string to help avoid detection
filler_words = [
    " wow ", 
    " hahaha ", 
    " omg ", 
    " what ", 
    " sort of ", 
    " anyway ", 
    " yeah ", 
    " YOLO ", 
    " lmao ", 
    " lol ", 
    " literally ", 
    " I mean ", 
    " really ", 
    " fr ", 
    " true "
    ]


def encode(message: str):
    """
    Encodes a message into a string of emojis.

    Args:
        message: The message to encode.

    Process:
        ascii message -> hex string -> match to last character in emoji unicode -> random emoji

    Returns:
        A tuple containing the emoji string and the encoded message.
    """

    hex, encoded_message, emoji_string = "","",""

    # Convert the message to uppercase and then to a hexadecimal string
    print("[*] Encoding Message '{}' into Hex String [*]".format(message.upper()))
    message = bytes(message.upper(), 'utf-8')
    hex = binascii.hexlify(message)
    hex = str(hex).strip("b'").upper()
    print("Message Hex Encoded: {}".format(hex))

    # Iterate over each hexadecimal digit and replace it with a random emoji
    print("\n[*] Encoding Hex String into Emojis [*]")
    for char in hex:
        if char in end_chars:
            emoji_code_list = end_chars[char]
            
            # Randomly select emoji
            new_emoji = random.choice(emoji_code_list)
            
            # Add emoji to encoded message
            emoji_string += new_emoji
            encoded_message += new_emoji

            # Randomly insert a filler word to obfuscate the pattern
            if random.randint(0,len(emoji_string)) == emoji_string.index(new_emoji):
                encoded_message += str(random.choice(filler_words))

            print("Char: {}   ->   Emoji: {}".format(char, new_emoji))

    return emoji_string, encoded_message


def decode(emoji_string):
    """
    Decodes an emoji string into the original message.

    Args:
        emoji_string: The emoji string to decode.

    Process:
        emoji -> last char in emoji unicode -> hex string -> ascii message

    Returns:
        The decoded message.
    """
    
    hex_string = ""

    print("\n[*] Decoding Emojis into Hex String [*]")
    for emoji_char in emoji_string:
        if emoji_char in end_chars["0"]:
            hex_string += "0"
        elif emoji_char in end_chars["1"]:
            hex_string += "1"
        elif emoji_char in end_chars["2"]:
            hex_string += "2"
        elif emoji_char in end_chars["3"]:
            hex_string += "3"
        elif emoji_char in end_chars["4"]:
            hex_string += "4"
        elif emoji_char in end_chars["5"]:
            hex_string += "5"
        elif emoji_char in end_chars["6"]:
            hex_string += "6"
        elif emoji_char in end_chars["7"]:
            hex_string += "7"
        elif emoji_char in end_chars["8"]:
            hex_string += "8"
        elif emoji_char in end_chars["9"]:
            hex_string += "9"
        elif emoji_char in end_chars["A"]:
            hex_string += "A"
        elif emoji_char in end_chars["B"]:
            hex_string += "B"
        elif emoji_char in end_chars["C"]:
            hex_string += "C"
        elif emoji_char in end_chars["D"]:
            hex_string += "D"
        elif emoji_char in end_chars["E"]:
            hex_string += "E"
        elif emoji_char in end_chars["F"]:
            hex_string += "F"

    print("Hex String:\t{}".format(hex_string))
    print("\n[*] Decoding Hex String into Message [*]")

    # Convert the hexadecimal string back to bytes and then to ascii string
    decoded_message = bytes.fromhex(hex_string)
    decoded_message = str(decoded_message).strip("b'")
    print("Decoded Message:\t{}".format(decoded_message))

    return decoded_message


def main():
    message = "hello"
    emoji_string, encoded_message  = encode(message)

    print("\nEmoji String:\t{}".format(emoji_string))
    print("Encoded Message:{}".format(encoded_message))

    decode(emoji_string)

if __name__ == "__main__":
    main()
