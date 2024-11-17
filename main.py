# Import necessary modules
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
import pandas as pd

# Define paths for GeckoDriver and Firefox binary
driver_path = "./FirefoxDriver/geckodriver.exe"
firefox_binary_path = "C:/Program Files/Mozilla Firefox/firefox.exe"

# Set up Firefox options and initialize the WebDriver
options = Options()
options.binary_location = firefox_binary_path
service = Service(executable_path=driver_path)
driver = webdriver.Firefox(service=service, options=options)

# Open the URL and wait for the page to load
driver.get("https://www.iku.edu.tr/tr/istanbulkulturuniversitesi")
driver.implicitly_wait(3)

# Find and click the target link
divs = driver.find_elements(By.CSS_SELECTOR, ".kayip.boxfk.grey")
target_element = divs[1].find_element(By.XPATH, ".//a")
target_element.click()
driver.implicitly_wait(3)

# Extract and print page title
titles = driver.find_elements(By.TAG_NAME, "h1")
print(titles[0].text)

# Extract table data
text = ""
tables = driver.find_elements(By.TAG_NAME, "table")
for table in tables:
    text += f'{table.text}\n'

# Process the table data into a DataFrame
rows = []
for line in text.splitlines():
    match = re.match(r"(.+?) (\d+ \w+ \d{4}) (\w+)", line)
    if match:
        event, date, day = match.groups()
        rows.append([event, date, day])

dataFrame = pd.DataFrame(rows, columns=["Event", "Date", "Day"])
print(dataFrame.to_string(index=False))

# Close the browser
driver.quit()
