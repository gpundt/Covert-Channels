from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import random
import numpy
import EmojiEncoding


class PostReceiver:
    def __init__(self, ig_username, ig_password, account_name):
        self.loggedin = False
        self.username = ig_username
        self.password = ig_password
        self.account = account_name
        self.base_url = "https://www.instagram.com"
        self.posts = []
        self.Login()
        self.GoToUser(self.account)
        self.encoded = self.GetMessage()
        if self.encoded is not None:
            self.decoded_message = EmojiEncoding.decode(self.encoded)
        print("[*] Closing [*]")

    ############### Helper Functions ###############
    def Wait(self, min, max):
        #Pauses for random amount of time
        time.sleep(random.choice(numpy.arange(min, max, 0.1)))

    def GoToUser(self, user):
        # Goes to a user's page
        self.driver.get("{}/{}/".format(self.base_url, user))
        self.Wait(1, 2)


    ############### Logging In ###############
    def Login(self):
        print("[*] Opening Browser [*]")
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


    ############### Get Encoded Message ###############
    def GetMessage(self):
        self.Wait(2,3)
        print("[*] Obtaining Posts [*]")
        self.posts = self.driver.find_elements(by=By.XPATH, value="//a[contains(@href, '/{}/p/')]".format(self.username))
        #print("Search Value: " + "//a[contains(@href, '/{}/p/')]".format(self.username))
        if not self.posts:
            print("/// No Posts Found... ///")
            print("[*] Closing [*]")
            return None
        print("Number of Posts: {}".format(str(len(self.posts))))
        latest_post = self.posts[0]
        print("[*] Accessing Most Recent Post [*]")
        latest_post.click()
        self.Wait(3,4)
        comments = self.driver.find_elements(by=By.XPATH, value="//h1[contains(@dir, 'auto')]")
        print("Number of Comments: {}".format(str(len(comments))))
        print("[*] Obtaining Message [*]")
        encoded_message = comments[0].text
        print("Encoded Message:\t{}".format(encoded_message))
        return encoded_message
    

def main():
    username, password = "steinybrown", "crabbywhammystu88"
    bot = PostReceiver(username, password, "steinybrown")


if __name__ == "__main__":
    main()