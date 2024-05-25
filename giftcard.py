import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the text file with search topics
file_path = 'search_topics.txt'

# Initialize Microsoft Edge WebDriver
driver = webdriver.Edge()

# Navigate to Bing's homepage
driver.get("https://www.bing.com/")

# Time interval to wait for Bing to load (adjust as needed)
time.sleep(10)

# Read search topics from the text file
with open(file_path, 'r') as file:
    search_topics = file.readlines()

# Pass each search query to the Bing search box using JavaScript
for topic in search_topics:
    search_query = topic.strip()  # Remove leading/trailing whitespace
    if search_query:  # Ensure the search query is not empty
        # Execute JavaScript to set the search query directly in the search box
        driver.execute_script("document.getElementById('sb_form_q').value = '{}'".format(search_query))
        # Find the search button and click after waiting for it to be clickable
        search_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.ID, "sb_form_go"))
        )
        search_button.click()
        # Wait for a short interval before submitting the next search query
        time.sleep(2)

# Close the WebDriver session
driver.quit()
