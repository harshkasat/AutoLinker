import time
import random
import os
import logging
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('linkedin_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def create_chrome_options():
    """Create Chrome options for headless and GitHub Actions compatibility."""
    options = Options()
    
    # Chrome options for GitHub Actions
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    
    return options

def create_webdriver():
    """Create and return a configured Chrome WebDriver."""
    try:
        options = create_chrome_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver
    except Exception as e:
        logger.error(f"Failed to create WebDriver: {e}")
        raise

class LinkedinAutomate:
    @staticmethod
    def login(driver):
        """Login to LinkedIn with error handling."""
        try:
            username = os.getenv('LINKEDIN_USERNAME')
            password = os.getenv('LINKEDIN_PASSWORD')
            
            if not username or not password:
                raise ValueError("LinkedIn credentials not found in environment")
            
            driver.get("https://www.linkedin.com/login")
            
            # Wait for elements to be present
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='session_key']"))
            )
            password_input = driver.find_element(By.XPATH, "//input[@name='session_password']")
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            
            username_input.send_keys(username)
            password_input.send_keys(password)
            submit_button.click()
            
            time.sleep(3)
            logger.info("Successfully logged into LinkedIn")
        except Exception as e:
            logger.error(f"Login failed: {e}")
            # Take a screenshot on failure
            driver.save_screenshot('login_error.png')
            raise

    @staticmethod
    def send_connection_request(driver):
        """Send connection requests with comprehensive error handling."""
        try:
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]
            
            logger.info(f"Found {len(connect_buttons)} potential connection requests")
            
            for btn in connect_buttons:
                try:
                    # Click "Connect" button
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(2)
                    
                    # Send connection without note
                    send_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send without a note']"))
                    )
                    driver.execute_script("arguments[0].click();", send_button)
                    
                    # Dismiss dialog
                    dismiss_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Dismiss']"))
                    )
                    driver.execute_script("arguments[0].click();", dismiss_button)
                    
                    time.sleep(2)
                    logger.info("Connection request sent successfully")
                except Exception as btn_error:
                    logger.warning(f"Failed to send connection request for a button: {btn_error}")
        
        except Exception as e:
            logger.error(f"Error in sending connection requests: {e}")
            driver.save_screenshot('connection_request_error.png')
            raise

def random_choice_url():
    """Generate a random LinkedIn search URL."""
    all_keywords = ["amazon", 'google', 'microsoft', 'ibm', 'apple', 'salesforce', 'flipkart', 'facebook', 'meta', 'samsung']
    keyword = random.choice(all_keywords)
    return f'https://www.linkedin.com/search/results/people/?keywords={keyword}'

def search_profiles(driver: webdriver, base_url: str, limit: int, default_num: Optional[int] = 5):
    """Search and attempt to send connection requests."""
    try:
        search_profile_url = base_url + '&origin=FACETED_SEARCH&page={default_num}&position=0'

        for i in range(default_num, limit + default_num):
            url = search_profile_url.format(default_num=i)
            logger.info(f"Searching profiles on page {i}")
            
            driver.get(url)
            time.sleep(5)
            
            LinkedinAutomate.send_connection_request(driver)
    
    except Exception as e:
        logger.error(f"Error in searching profiles: {e}")
        driver.save_screenshot('search_profiles_error.png')
        raise

def linkedIn_automate():
    """Main automation function with comprehensive error handling."""
    driver = None
    try:
        base_url = random_choice_url()
        logger.info(f"Selected search URL: {base_url}")

        driver = create_webdriver()
        LinkedinAutomate.login(driver)
        search_profiles(driver=driver, base_url=base_url, limit=3)
        
        logger.info("LinkedIn automation completed successfully")
    
    except Exception as e:
        logger.error(f"LinkedIn automation failed: {e}")
        if driver:
            driver.save_screenshot('linkedin_automation_error.png')
        raise
    
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    linkedIn_automate()