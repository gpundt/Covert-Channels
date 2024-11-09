from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import random
import numpy
import EmojiEncoding


class PostReceiver:
    """
    This class retrieves the caption from the most recent post of a specified Instagram account.

    Attributes:
        loggedin (bool): Indicates whether the login was successful.
        username (str): The Instagram username to log in with.
        password (str): The password for the Instagram account.
        account (str): The username of the Instagram account to retrieve the message from.
        base_url (str): The base URL for Instagram.
        posts (list): A list of Selenium web elements representing potential posts.
        encoded_message (str): The message (caption) retrieved from the latest post, encoded with emojis (if applicable).
        decoded_message (str, optional): The decoded message (caption) with emojis displayed correctly (if EmojiEncoding library is available).
    """

    def __init__(self, ig_username, ig_password, account_name):
        """
        Initializes the PostReceiver object.

        Args:
            ig_username (str): The Instagram username to log in with.
            ig_password (str): The password for the Instagram account.
            account_name (str): The username of the Instagram account to retrieve the message from.
        """
        self.loggedin = False
        self.username = ig_username
        self.password = ig_password
        self.account = account_name
        self.base_url = "https://www.instagram.com"
        self.posts = []

        # Initiate login process
        self.Login()

        # Go to the target user's profile page
        self.GoToUser(self.account)

        # Get the caption (encoded message)
        self.encoded = self.GetMessage()

        # Decode message
        if self.encoded is not None:
            self.decoded_message = EmojiEncoding.decode(self.encoded)

        print("[*] Closing [*]")


    ############### Helper Functions ###############

    def Wait(self, min, max):
        """
        Waits for a random amount of time between the specified minimum and maximum values (in seconds).

        This helps simulate human-like behavior and potentially avoid detection by Instagram's anti-scraping measures.

        Args:
            min_wait (float): The minimum wait time in seconds.
            max_wait (float): The maximum wait time in seconds.
        """
        time.sleep(random.choice(numpy.arange(min, max, 0.1)))


    def GoToUser(self, user):
        """
        Navigates to the specified user's Instagram profile page.

        Args:
            user (str): The username of the target Instagram account.
        """
        self.driver.get("{}/{}/".format(self.base_url, user))
        self.Wait(1, 2) # Wait for page to load


    ############### Logging In ###############

    def Login(self):
        """
        Logs in to Instagram using the provided credentials.

        Prints messages to indicate the login process and success/failure.

        Raises:
            Exception: If an unexpected error occurs during login.
        """
        print("[*] Opening Browser [*]")
        self.driver = webdriver.Chrome()
        print("[*] Logging in: {} [*]".format(self.username))

        try:
            self.driver.get("{}/accounts/login".format(self.base_url))
            self.Wait(2, 3)  # Wait for login page to load

            # Find username and password input elements
            username_input_element = self.driver.find_element(by=By.NAME, value="username")
            password_input_element = self.driver.find_element(by=By.NAME, value="password")

            # Enter username and password
            username_input_element.send_keys(self.username)
            self.Wait(1, 2)
            password_input_element.send_keys(self.password)
            self.Wait(1, 2)

            # Click the login button
            login_button = self.driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div/div[3]/button")
            login_button.click()

            print("[*] Logged in : {} [*]".format(self.username))
            self.loggedin = True
            self.Wait(7, 8)  # Wait for the homepage to load

        except Exception as e:
            print(f"An error occurred during login: {str(e)}")
            self.loggedin = False


    ############### Get Encoded Message ###############
    def GetMessage(self):
        """
        Retrieves the caption (encoded message) from the most recent post of the target user.

        Returns:
            str: The encoded message (caption) if a post is found, otherwise None.
        
        Raises:
            Exception: If any errors occur during information retrieval (e.g., element not found).
        """
        self.Wait(2,3)
        print("[*] Obtaining Posts [*]")

        try:
            # Find elements that link to the target user's posts using XPath
            self.posts = self.driver.find_elements(by=By.XPATH, value="//a[contains(@href, '/{}/p/')]".format(self.username))
        except Exception as e:    
            # Debugging purposes (shows the XPath search string)
            print("Search Value: " + "//a[contains(@href, '/{}/p/')]".format(self.username))

            print(f"Error obtaining posts: {e}")
            raise  # Re-raise the exception for further handling
        
        if not self.posts:
            print("/// No Posts Found... ///")
            print("[*] Closing [*]")
            return None  # No posts found, return None
        
        print("Number of Posts: {}".format(str(len(self.posts))))

        # Get the first element (the latest post) from the list of posts
        latest_post = self.posts[0]
        print("[*] Accessing Most Recent Post [*]")
        latest_post.click()  # Click on the latest post

        self.Wait(3,4)

        try:
            # Find elements with the specified XPath expression (caption and comments)
            comments = self.driver.find_elements(by=By.XPATH, value="//h1[contains(@dir, 'auto')]")
        except Exception as e:    
            print(f"Error obtaining comments: {e}")
            raise  # Re-raise the exception for further handling
        
        print("Number of Comments: {}".format(str(len(comments))))
        
        print("[*] Obtaining Message [*]")
        
        # If there are elements found, extract the text from the first one as the encoded message
        if comments:
            encoded_message = comments[0].text
            print("Encoded Message:\t{}".format(encoded_message))
            return encoded_message
        else:
            print("No caption element found for the post.")
            return None  # No caption element found, return None
    

def main():
    username, password = "<USERNAME>", "<PASSWORD>"
    PostReceiver(username, password, "steinybrown")


if __name__ == "__main__":
    main()