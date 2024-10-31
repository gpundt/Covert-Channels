import emoji
import binascii
import EmojiList
import random

## Unicode Emoji List: https://unicode.org/emoji/charts/full-emoji-list.html ##



# emoji_code_list = ["\U0001F600",
#                     "\U0001F601",
#                     "\U0001F602",
#                     "\U0001F603",
#                     "\U0001F604",
#                     "\U0001F605",
#                     "\U0001F606",
#                     "\U0001F607",
#                     "\U0001F608",
#                     "\U0001F609",
#                     "\U0001F60A",
#                     "\U0001F60B",
#                     "\U0001F60C",
#                     "\U0001F60D",
#                     "\U0001F60E",
#                     "\U0001F60F"]

end_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",\
             "A", "B", "C", "D", "E", "F"]

def encode(message: str):
    emoji_code_list = EmojiList.random_emojis
    # message.upper() -> hex string -> last char in emoji code -> emoji code -> emoji
    encoded_message = ""
    emoji_string = ""
    # Turniong message into hex
    print("[*] Encoding Message '{}' into Hex String [*]".format(message.upper()))
    message = bytes(message.upper(), 'utf-8')
    encoded = binascii.hexlify(message)
    encoded = str(encoded).strip("b'").upper()
    print("Message Hex Encoded: {}".format(encoded))

    # Turning hex into emojis
    print("[*] Encoding Hex String into Emojis [*]")
    for char in encoded:
        for end_char in end_chars:
            if char == end_char:
                index = end_chars.index(end_char)
                usable_emojis = []
                for unicode in emoji_code_list:
                    if unicode[1].upper() == end_char:
                        usable_emojis.append(unicode[:1])
                #print(usable_emojis)
                ### Emoji
                new_emoji = emoji.emojize(random.choice(usable_emojis))
                ### Emoji code
                encoded_message += new_emoji
                emoji_string += new_emoji
                print("Char: {}   ->   Emoji: {}".format(char, new_emoji))
    return emoji_string, encoded_message

def decode(emoji_string):
    emoji_code_list = EmojiList.random_emojis
    # emoji -> last char in emoji code -> hex string -> message.upper()
    hex_string = ""
    print("[*] Decoding Emojis into Hex String [*]")
    # for emoji_character in emoji_string:
    #     for emoji_code in emoji_code_list:
    #         if emoji_character == emoji.emojize(emoji_code):
    #             index = emoji_code_list.index(emoji_code)
    #             # Adding last char of emoji code to hex_string
    #             hex_string += end_chars[index]
    #             print("Emoji: {}   ->   Char: {}".format(emoji_character, end_chars[index]))
    for emoji_character in emoji_string:
        for emoji_code in emoji_code_list:
            if emoji_character == emoji.emojize(emoji_code[0]):
                hex_string += emoji_code[1]
    
    print("Hex String: {}".format(hex_string))
    print("[*] Decoding Hex String into Message [*]")
    #decoding hex string into ascii
    decoded_message = bytes.fromhex(hex_string)
    decoded_message = str(decoded_message).strip("b'")
    print("Decoded Message:\t{}".format(decoded_message))
    return decoded_message


def main():
    message = "hello"
    emoji_string, encoded_message  = encode(message)
    print("Emoji String: {}".format(emoji_string))
    print("Encoded Message: {}".format(encoded_message))
    decoded_message = decode(emoji_string)
    # for unicode in EmojiList.random_emojis:
    #     print(emoji.emojize(unicode))

if __name__ == "__main__":
    main()
