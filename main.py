from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import os
from dotenv import load_dotenv
load_dotenv()

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager




def ChromeProfile():
    # Create ChromeOptions instance
    options = webdriver.ChromeOptions()

    # Provide the location where Chrome stores user data
    options.add_argument(f"--user-data-dir=C:/Users/Zedmat/AppData/Local/Google/Chrome/User Data")

    # Provide the profile directory name (make sure it's the correct profile directory)
    options.add_argument(f'--profile-directory=Default')  # Ensure there's a space if the profile name includes one

    # Additional options
    options.add_argument("--no-sandbox")


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    return driver



def login(driver):
    driver.get("https://www.linkedin.com/")
    # driver.find_element(By.ID, "username").send_keys(username)
    # driver.find_element(By.ID, "password").send_keys(password)
    # driver.find_element(By.XPATH, "//button[@type='submit']").click()
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "global-nav")))

def search_profiles(driver, keyword):
    search_bar = driver.find_element(By.XPATH, "//input[@aria-label='Search']")
    search_bar.clear()
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.RETURN)
    
    # Wait for search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-reusables__filters-bar-grouping")))


def click_people(driver):

    driver.find_element(By.XPATH, "//button[text()='People']").click()
    # WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//button[@aria-lable = 'Actively hiring filter.'")))
    time.sleep(5)

    # time.sleep(10)

def extract_profiles(driver, num_profiles):
    try:
        # Find all elements with the class name 'app-aware-link'
        elements = driver.find_elements(By.CLASS_NAME, "app-aware-link")
        
        # Ensure that we have the right number of profiles
        if len(elements) < num_profiles:
            num_profiles = len(elements)
        
        # Extract the href attribute of each element
        urls = set([element.get_attribute('href') for element in elements[8:]])
        filtered_urls = [url for url in urls if '/in/' in url]
        
        return filtered_urls

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    # return profiles

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def send_connection_request(driver, profile_urls):
    for url in profile_urls:
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        try:
            # Find all buttons and filter for those with text "Connect"
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]

            for btn in connect_buttons:
                # Click the "Connect" button using JavaScript
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(2)  # Wait for the popup to appear

                # Find and click the "Send now" button
                send_button = driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
                driver.execute_script("arguments[0].click();", send_button)

                # Find and click the "Dismiss" button to close the dialog
                dismiss_button = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                driver.execute_script("arguments[0].click();", dismiss_button)
                time.sleep(2)  # Wait before moving to the next connection

            print(f"Connection request sent to {url}")

        except Exception as e:
            print(f"Couldn't send connection request to {url} - {e}")


def main():
    # driver = webdriver.Chrome()
    driver = ChromeProfile()
    login(driver)
    
    # username = os.getenv("LINKEDIN_USERNAME")
    # password = os.getenv("LINKEDIN_PASSWORD")
    
    # login(driver, username, password)
    
    search_keyword = "software developer"
    num_profiles_to_connect = 10
    
    search_profiles(driver, search_keyword)
    # time.sleep(3)
    click_people(driver)
    profiles = extract_profiles(driver, num_profiles_to_connect)
    
    # for profile in profiles:
    send_connection_request(driver, profiles)
    
    # driver.quit()

if __name__ == "__main__":
    main()