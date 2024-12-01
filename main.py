import time
import random
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional

from dotenv import load_dotenv
load_dotenv()


def chrome_profile():
    # Create ChromeOptions instance
    options = webdriver.ChromeOptions()

    # Provide the location where Chrome stores user data
    # options.add_argument(f"--user-data-dir=C:/Users/Zedmat/AppData/Local/Google/Chrome/User Data")

    # Provide the profile directory name (make sure it's the correct profile directory)
    # options.add_argument(f'--profile-directory=Default')  # Ensure there's a space if the profile name includes one

    # Additional options
    options.add_argument("--no-sandbox")

    # Enable headless mode
    # options.add_argument("--headless")

    # Optionally, if you're using headless mode with a screen resolution requirement
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver



class LinkedinAutomate:

    def login(driver):
        username = os.getenv('LINKEDIN_USERNAME')
        password = os.getenv('LINKEDIN_PASSWORD')
        driver.get("https://www.linkedin.com/login")
        # Login user with session is out
        driver.find_element(By.XPATH, "//input[@name='session_key']").send_keys(username)
        driver.find_element(By.XPATH, "//input[@name='session_password']").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)

    def send_connection_request(driver):
        
        try:
            # Find all buttons and filter for those with text "Connect"
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]

            for btn in connect_buttons:
                # Click the "Connect" button using JavaScript
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(2)  # Wait for the popup to appear

                # Find and click the "Send now" button
                send_button = driver.find_element(By.XPATH, "//button[@aria-label='Send without a note']")
                driver.execute_script("arguments[0].click();", send_button)
                # Find and click the "Dismiss" button to close the dialog
                dismiss_button = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                driver.execute_script("arguments[0].click();", dismiss_button)
                time.sleep(2)  # Wait before moving to the next connection

                print(f"Connection request sent ")

        except Exception as e:
            print(f"Couldn't send connection request to {e}")


def random_choice_url():
    all_keyword = ["amazon", 'google', 'microsoft', 'ibm', 'apple', 'saleforce', 'flipkart' 'facebook', 'meta', 'samsung']
    keyword = random.choice(all_keyword)
    base_url = f'https://www.linkedin.com/search/results/people/?keywords={keyword}'
    return base_url

def search_profiles(driver: webdriver, base_url: str, limit:int, default_num: Optional[int] = 5):
        search_profile_url = base_url + '&origin=FACETED_SEARCH&page={default_num}&position=0' 

        for i in range(default_num, limit+default_num):
            url = search_profile_url.format(default_num=i)
            driver.get(url)
            time.sleep(5)
            LinkedinAutomate.send_connection_request(driver)


def linkedIn_automate():
    base_url = random_choice_url()

    driver = chrome_profile()

    linkedin = LinkedinAutomate
    linkedin.login(driver)
    search_profiles(driver=driver, base_url=base_url, limit=3)

if __name__ == '__main__':
    linkedIn_automate()