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
    """
    This class defines a PostBot object that can be used to automate Instagram posting.
    
    Attributes:
      loggedin (bool): Tracks if the bot has successfully logged in.
      username (str): Username for the Instagram account.
      password (str): Password for the Instagram account.
      base_url (str): Base URL for Instagram website.
      base_filepath (str): Base file path for the directory containing photos to post.
      followers_count (int): Stores the number of followers for the account.
      following_count (int): Stores the number of accounts the user is following.
      post_count (int): Currently not used, intended to store the number of posts made.
      file (str): Stores the filename of the chosen photo to post.
      message (str): Stores the caption message for the post.
    """
    
    def __init__ (self, ig_username, ig_password):
        """
        Initializes the PostBot object with the provided username and password.

        Args:
            ig_username (str): Username for the Instagram account.
            ig_password (str): Password for the Instagram account.
        """
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
        """
        Converts Instagram's shorthand follower/following count (e.g., 16K) to a numerical value.

        Args:
            text (str): The text containing the follower/following count.

        Returns:
            int: The numerical value of the follower/following count.
        """
        if "K" in text:
            return int((float(text.replace("K", "")))* 1000)
        elif "M" in text:
            return int((float(text.replace("M","")))* 1000000)
        else:
            return int(text)
        

    def Wait(self, min, max):
        """
        Pauses execution for a random amount of time within the specified range.

        Args:
            min (float): Minimum time to wait in seconds.
            max (float): Maximum time to wait in seconds.
        """
        time.sleep(random.choice(numpy.arange(min, max, 0.1)))


    def GoToUser(self, user):
        """
        Navigates the browser to the specified user's Instagram page.

        Args:
            user (str): Username of the user to visit.
        """
        self.driver.get("{}/{}/".format(self.base_url, user))
        self.Wait(1, 2)


    def InputMessage(self):
        """
        Prompts the user for a message to be used as the caption for the post.

        Returns:
            str: The message entered by the user.
        """
        print("[*] Prompting for Message... [*]")
        message = input("Message:\t")

        return message
    

    def InputChoice(self, size_of_list):
        """
        Prompts the user to choose a file to upload from a list, handling invalid input.

        Args:
            size_of_list (int): The number of files available for selection.

        Returns:
            int: The index of the chosen file in the list.
        """
        print("Choose Number of File to Upload")
        choice_index = input("Number:\t")

        if int(choice_index) > size_of_list-1:
            return self.InputChoice(size_of_list)
        return int(choice_index)

    
    def SelectFile(self):
        """
        Prompts the user to select a photo to post from a list of available photos in a directory.

        Returns:
            str: The filename of the chosen photo.
        """
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
        """
        Logs in to the target website using the provided credentials.

        Raises:
            Exception: If any errors occur during login (e.g., invalid credentials).
        """
        self.driver = webdriver.Chrome()

        print("[*] Logging in: {} [*]".format(self.username))

        try:
            self.driver.get("{}/accounts/login".format(self.base_url)) # Navigate to login page
        except Exception as e:
            print(f"Error navigating to login page: {e}")
            raise  # Re-raise the exception for further handling

        self.Wait(2,3)

        try:
            # Enter username
            self.driver.find_element(by=By.NAME, value="username").send_keys(self.username)
            self.Wait(1,2)

            # Enter password
            self.driver .find_element(by=By.NAME, value="password").send_keys(self.password)
            self.Wait(1,2)
        except Exception as e:
            print(f"Error finding or entering credentials: {e}")
            raise  # Re-raise the exception for further handling
        
        try:
            # Click login button
            self.driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div/div[3]/button").click()
        except Exception as e:
            print(f"Error clicking login button: {e}")
            raise  # Re-raise the exception for further handling
        
        print("[*] Logged in : {} [*]".format(self.username))
        
        self.loggedin = True
        self.Wait(7,8)


    def GetInfo(self):
        """
        Retrieves information about the current user's account, such as follower and following counts.

        Raises:
            Exception: If any errors occur during information retrieval (e.g., network issues).
        """
        print("[*] Getting Account Info [*]")

        try:
            self.GoToUser(self.username)  # Navigate to user's profile page
        except Exception as e:
            print(f"Error navigating to user profile: {e}")
            raise  # Re-raise the exception for further handling

        self.Wait(4, 5)

        try:
            followers_element = self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value="followers")
            followers_text = followers_element.text[:-9]  # Extract follower count
            self.followers_count = self.ConvertToNumber(followers_text)  # Convert text to number

            following_element = self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value="following")
            following_text = following_element.text[:-9]  # Extract following count
            self.following_count = self.ConvertToNumber(following_text)  # Convert text to number
        except Exception as e:
            print(f"Error finding or parsing follower/following count elements: {e}")
            raise  # Re-raise the exception for further handling

        print("[*] {} Account Info: [*]".format(self.username))

        print("\t{} Follower Count: {}".format(self.username, self.followers_count))
        print("\t{} Following Count: {}".format(self.username, self.following_count))


    def MakePost(self):
        """
        Creates a new post on the target website.

        Raises:
            Exception: If any errors occur during post creation (e.g., element not found).
        """
        self.Wait(1,2)

        print("[*] Creating Post... [*]")

        try:
            # Click "New post" button to initiate post creation
            self.driver.find_element(by=By.XPATH, value="//*[@aria-label='New post']").click()
        except Exception as e:
            print(f"Error clicking 'New post' button: {e}")
            raise  # Re-raise the exception for further handling
        
        self.Wait(2,3)
        try:
            # Click "Select from computer" button to upload image
            self.driver.find_element(by=By.XPATH, value="//button[text()='Select from computer']").click()
            self.Wait(3,4)

            # Grabs selected image from the SelectFile function
            pyautogui.typewrite("<FILEPATH TO PICTURE>{}".format(self.file))
            self.Wait(1,2)

            # Press Enter to confirm file selection
            pyautogui.press("enter")
        except Exception as e:
            print(f"Error uploading image: {e}")
            raise  # Re-raise the exception for further handling

        # Click "Next" buttons to navigate through post creation steps
        self.Wait(2, 3)
        self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Next')]").click()
        self.Wait(2, 3)
        self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Next')]").click()
        
        # Input message into caption
        self.Wait(1, 1.5)
        emoji_string, encoded_message = EmojiEncoding.encode(self.message)
        print("Encoded Message:\t{}".format(encoded_message))
        print("Emoji String:\t{}".format(emoji_string))

        # Simulate tabbing to the caption field
        for _ in range(5):
            pyautogui.press("tab")
        
        # Copy encoded message to clipboard and paste into caption field
        clipboard.copy(emoji_string)
        pyautogui.hotkey("ctrl", "v")

        self.Wait(5, 6)

        print("[*] Sharing Post... [*]")

        # Simulate tabbing to the "Share" button
        for _ in range(7):
            pyautogui.press("tab")

        self.Wait(1, 2)

        pyautogui.press("enter") # Press Enter to share the post
        
        self.Wait(8, 10)

        print("[*] Post Shared! [*]")        
        print("[*] Returning to {}'s Page... [*]".format(self.username))

        try:
            self.GoToUser(self.username)  # Navigate back to user's profile page
        except Exception as e:
            print(f"Error navigating back to user profile: {e}")
            raise  # Re-raise the exception for handling

        self.Wait(5, 6)


def main():
    username, password = "<USERNAME>", "<PASSWORD>"
    PostBot(username, password)

if __name__ == "__main__":
    main()