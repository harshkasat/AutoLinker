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
    def is_logged_in(driver):
        """Check if login to LinkedIn was successful."""
        try:
            # Allow time for potential redirection
            time.sleep(3)
            current_url = driver.current_url
            logger.info(f"Current URL after login: {current_url}")

            # Check if redirected to a checkpoint
            if "checkpoint" in current_url:
                print("Checkpoint detected. Manual intervention required.")
                # Optionally, capture a screenshot for debugging
                driver.save_screenshot('checkpoint.png')
            else:
                print("Successfully logged in.")
            
            if "feed" in current_url or "linkedin.com/in/" in current_url:
                logger.info("Login verification successful: User is logged in.")
                return True
            else:
                logger.warning("Login verification failed: Unexpected URL.")
                return False
        except Exception as e:
            logger.error(f"Login verification failed: {e}")
            return False

    @staticmethod
    def send_connection_request(driver):
        """Send connection requests with comprehensive error handling."""
        try:
            button_text = []
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            logger.info(f"Found {len(all_buttons)} buttons")
            connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]
            text = [btn.text for btn in all_buttons]
            button_text.extend(text)
            # logger.info(f"Found {(button_text)} potential connection requests")
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
    return keyword

def search_profiles(driver: webdriver, keyword: str, limit: int, page_no: Optional[int] = 8):
    """Search and attempt to send connection requests."""
    try:
        base_url = 'https://www.linkedin.com/search/results/people/'
        
        for i in range(page_no, limit + page_no):
            # Construct the URL for the current page
            search_profile_url = f'{base_url}?page={i}&keywords={keyword}'
            logger.info(f"Searching profiles on page {i}")
            logger.info("Searching profiles URL: " + search_profile_url)
            
            driver.get(search_profile_url)
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
        keyword = random_choice_url()
        logger.info(f"Selected search URL: {keyword}")

        driver = create_webdriver()
        LinkedinAutomate.login(driver)
        if LinkedinAutomate.is_logged_in(driver):
            search_profiles(driver=driver, keyword=keyword, limit=5)
        else:
            logger.error("Login verification failed: User is not logged in.")
        
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