from selenium import webdriver  # Importing the main webdriver class for browser automation
from selenium.webdriver.firefox.service import Service  # For managing the Firefox WebDriver service
from selenium.webdriver.common.by import By  # For locating elements on the webpage
from selenium.webdriver.firefox.options import Options  # For setting options for Firefox browser
import os  # Importing os module for handling file paths and environment variables
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Loading environment variables from a .env file
load_dotenv()

# Getting the GitHub username and password from environment variables
USERNAME = os.getenv('NAME')
PASSWORD = os.getenv('PASSWORD')

# Path to GeckoDriver executable (used to interact with Firefox)
driver_path = "./FirefoxDriver/geckodriver.exe" 
# Path to the Firefox browser binary (the actual browser)
firefox_binary_path = "C:/Program Files/Mozilla Firefox/firefox.exe" 

class Github:
    # Initialization of the Github class, which includes setting up browser options, service, and credentials
    def __init__(self, username, password):
        # Configuring Firefox options
        self.options = Options()
        self.options.binary_location = firefox_binary_path  # Set Firefox's binary location
        self.service = Service(executable_path=driver_path)  # Set the path to the GeckoDriver
        self.browser = webdriver.Firefox(service=self.service, options=self.options)  # Create a new Firefox browser instance
        self.username = username  # Store the provided username
        self.password = password  # Store the provided password
        self.followers = []  # List to hold the followers' usernames
    
    # Method for logging into GitHub
    def signIn(self):
        # Navigate to the GitHub login page
        self.browser.get("https://github.com/login")
        self.browser.implicitly_wait(2)  # Wait for 2 seconds to ensure the page is loaded

        # Locate and fill the username and password fields
        self.browser.find_element(By.ID, "login_field").send_keys(self.username)
        self.browser.find_element(By.ID, "password").send_keys(self.password)
    
        self.browser.implicitly_wait(1)  # Wait for 1 second before clicking the login button

        # Locate and click the "Sign In" button
        button = self.browser.find_element(By.CLASS_NAME, "js-sign-in-button")
        button.click()
    
    # Method to get the list of followers of the logged-in user
    def getFollowers(self):
        # Navigate to the followers tab of the user's profile
        self.browser.get(f"https://github.com/{self.username}?tab=followers")
        self.browser.implicitly_wait(2)  # Wait for 2 seconds to load the followers page

        # Locate all elements representing individual followers
        items = self.browser.find_elements(By.CSS_SELECTOR, ".d-inline-block.no-underline.mb-1")
        for i in items:
            # Extract the text of each follower's username and add it to the followers list
            self.followers.append(i.find_element(By.CSS_SELECTOR, ".f4.Link--primary").text)

# Creating an instance of the Github class with the provided username and password
github = Github(USERNAME, PASSWORD)

github.signIn()
github.getFollowers()

# Printing the list of followers
print(github.followers)

# Closing the browser after the task is complete
github.browser.quit()
