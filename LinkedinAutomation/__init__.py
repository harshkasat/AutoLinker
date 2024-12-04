from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import logging
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


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

COMMENT_LIST = [
    "This post really resonates with me. Thanks for sharing!",
    "I appreciate your insights on this topic. It's thought-provoking.",
    "Your perspective adds valuable depth to the conversation. Well said!",
    "This is such an important discussion to have. Thanks for starting it.",
    "I've never thought about it that way before. Thanks for sharing your viewpoint.",
    "Your post inspired me to [action or reflection]. Thank you for that!",
    "I agree with your points wholeheartedly. Well articulated!",
    "Your expertise shines through in this post. Informative and engaging!",
    "I learned something new from reading your post. Thanks for the enlightenment!",
    "Your positivity is contagious! This post brought a smile to my face.",
    "Thanks for shedding light on this topic. Your insights are invaluable.",
    "Great post! Your insights are always valuable.",
    "Love seeing your content on my feed. Keep it coming!",
    "This is spot-on! Thanks for sharing your expertise.",
    "Your posts always provide such valuable information. Thanks for sharing!",
    "I always learn something new from your posts. Thanks for the knowledge!",
    "Your content is always so engaging. It's a pleasure to read.",
    "Thanks for sharing this insightful perspective. Really enjoyed reading!",
    "Your posts make a difference in my day. Keep up the great work!",
    "Your content deserves more recognition. It's always top-notch.",
    "Thanks for consistently delivering great content. It's appreciated!",
]

class ChromeDriver:
    """Custom ChromeDriverManager class to handle GitHub Actions compatibility."""
    def create_chrome_options(self):
        """Create Chrome options for headless and GitHub Actions compatibility."""
        options = Options()
        
        # Chrome options for GitHub Actions
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')


        return options

    def create_webdriver(self):
        """Create and return a configured Chrome WebDriver."""
        try:
            options = self.create_chrome_options()
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.maximize_window()
            driver.implicitly_wait(10)
            return driver
        except Exception as e:
            logger.error(f"Failed to create WebDriver: {e}")
            raise

class LinkedInAutomation:
    
    def login(self, driver:webdriver):
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