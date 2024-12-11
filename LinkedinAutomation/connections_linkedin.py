import logging
import time
import random
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

def random_keyword():
    """Generate a random LinkedIn search URL."""
    all_keywords = [
    "Google",
    "Apple",
    "Microsoft",
    "Amazon",
    "Salesforce",
    "Meta",
    "IBM",
    "Netflix",
    "Adobe",
    "Intel",
    "NVIDIA",
    "Cisco", 
    "Oracle",
    "Zoom",
    "Stripe",
    "Pinterest",
    "LinkedIn",
    "Square",
    "Snapchat",
    "Dropbox",
    "GitHub",
    "Slack",
    "Atlassian",
    "Twilio",
    "VMware",
    "ServiceNow",
    "HubSpot",
    "Red Hat",
    "Qualcomm", 
    "Airbnb"
]

    keyword = random.choice(all_keywords)
    return keyword

def send_connection_request(driver):
        """Send connection requests with comprehensive error handling."""
        try:
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            logger.info(f"Found {len(all_buttons)} buttons")
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

                    time.sleep(2)
                    logger.info("Connection request sent successfully")
                except Exception as btn_error:
                    logger.warning(f"Failed to send connection request for a button: {btn_error}")
        
        except Exception as e:
            logger.error(f"Error in sending connection requests: {e}")
            driver.save_screenshot('connection_request_error.png')
            raise


def search_profiles(driver: webdriver, page_limit: Optional[int] = 8, page_no: Optional[int] = 8, keyword: Optional[str] = None):
    """Search and attempt to send connection requests."""
    keyword = random_keyword()
    try:
        base_url = 'https://www.linkedin.com/search/results/people/'
        
        for i in range(page_no, page_limit + page_no):
            # Construct the URL for the current page
            search_profile_url = f'{base_url}?page={i}&keywords={keyword}'
            logger.info(f"Searching profiles on page {i}")
            logger.info("Searching profiles URL: " + search_profile_url)
            
            driver.get(search_profile_url)
            time.sleep(5)
            
            send_connection_request(driver)
    
    except Exception as e:
        logger.error(f"Error in searching profiles: {e}")
        driver.save_screenshot('search_profiles_error.png')
        raise
