from selenium import webdriver
from selenium.webdriver.common.by import By

import os
import time
import random
import numpy
import pyautogui
import clipboard
import EmojiEncoding

class PostBot:
    def __init__ (self, ig_username, ig_password):
        self.loggedin = False
        self.username = ig_username
        self.password = ig_password
        self.base_url = "https://www.instagram.com"
        self.base_filepath = "C:\\Users\\13158\\OneDrive\\Desktop\\CSEC 750\\Instagram Covert Channel\\photos\\"
        self.followers_count = 0
        self.following_count = 0
        self.post_count = 0
        self.file = str(self.SelectFile())
        self.message = self.InputMessage()
        self.Login()
        self.GetInfo()
        self.MakePost()
        print("[*] Closing [*]")


    ############### Helper Functions ###############
    def ConvertToNumber(self, text):
        #Converts instagram's shorthand to a number
        #Example 16K -> 16000
        if "K" in text:
            return int((float(text.replace("K", "")))* 1000)
        elif "M" in text:
            return int((float(text.replace("M","")))* 1000000)
        else:
            return int(text)
        
    def Wait(self, min, max):
        #Pauses for random amount of time
        time.sleep(random.choice(numpy.arange(min, max, 0.1)))

    def GoToUser(self, user):
        # Goes to a user's page
        self.driver.get("{}/{}/".format(self.base_url, user))
        self.Wait(1, 2)

    def InputMessage(self):
        print("[*] Prompting for Message... [*]")
        message = input("Message:\t")
        return message
    
    def InputChoice(self, size_of_list):
        print("Choose Number of File to Upload")
        choice_index = input("Number:\t")
        if int(choice_index) > size_of_list-1:
            return self.InputChoice(size_of_list)
        return int(choice_index)

    
    def SelectFile(self):
        print("\n[*] Choosing Photo from ./photos [*]")
        filelist = os.listdir(self.base_filepath)
        print("Available Photos:")
        string = ""
        index = 0
        for file in filelist:
            string += "\t" + str(index) + ") " + str(file) + "\n"
            index += 1
        print(string)
        choice_index = self.InputChoice(len(filelist))
        file = filelist[choice_index]
        return file


    ############### Logging In ###############
    def Login(self):
        self.driver = webdriver.Chrome()
        print("[*] Logging in: {} [*]".format(self.username))
        self.driver.get("{}/accounts/login".format(self.base_url))
        self.Wait(2,3)
        self.driver.find_element(by=By.NAME, value="username").send_keys(self.username)
        self.Wait(1,2)
        self.driver .find_element(by=By.NAME, value="password").send_keys(self.password)
        self.Wait(1,2)
        self.driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div/div[3]/button").click()
        print("[*] Logged in : {} [*]".format(self.username))
        self.loggedin = True
        self.Wait(7,8)

    ### Gets info from account ###
    def GetInfo(self):
        print("[*] Getting Account Info [*]")
        self.GoToUser(self.username)
        self.Wait(4, 5)
        # Get number of followers
        temp = self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value="followers").text
        temp = temp[:-9]
        self.followers_count = self.ConvertToNumber(temp)
        # Get number of following
        temp = self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value="following").text
        temp = temp[:-9]
        self.following_count = self.ConvertToNumber(temp)
        print("[*] {} Account Info: [*]".format(self.username))
        #print("\t{} Post Count: {}".format(self.username, self.post_count))
        print("\t{} Follower Count: {}".format(self.username, self.followers_count))
        print("\t{} Following Count: {}".format(self.username, self.following_count))

    ### Make Post ###
    def MakePost(self):
        self.Wait(1,2)
        print("[*] Creating Post... [*]")
        self.driver.find_element(by=By.XPATH, value="//*[@aria-label='New post']").click()
        self.Wait(2,3)
        self.driver.find_element(by=By.XPATH, value="//button[text()='Select from computer']").click()
        self.Wait(3,4)
        ##Full path to picture being shared##
        pyautogui.typewrite("<FILEPATH TO PICTURE>{}".format(self.file))
        self.Wait(1,2)
        pyautogui.press("enter")
        self.Wait(2, 3)
        self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Next')]").click()
        self.Wait(2, 3)
        self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Next')]").click()
        
        # Input message into caption
        self.Wait(1, 1.5)
        emoji_string, encoded_message = EmojiEncoding.encode(self.message)
        print("Encoded Message:\t{}".format(encoded_message))
        print("Emoji String:\t{}".format(emoji_string))
        for _ in range(5):
            pyautogui.press("tab")
        clipboard.copy(emoji_string)
        pyautogui.hotkey("ctrl", "v")
        self.Wait(5, 6)

        #Share post
        print("[*] Sharing Post... [*]")
        for _ in range(7):
            pyautogui.press("tab")
        self.Wait(1, 2)
        pyautogui.press("enter")
        self.Wait(8, 10)
        print("[*] Post Shared! [*]")        
        print("[*] Returning to {}'s Page... [*]".format(self.username))
        self.GoToUser(self.username)
        self.Wait(5, 6)


def main():
    username, password = "<USERNAME>", "<PASSWORD>"
    bot = PostBot(username, password)

if __name__ == "__main__":
    main()