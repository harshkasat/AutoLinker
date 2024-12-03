import time
import random
import os
import logging
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

comment_list = [
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
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')


    return options

def create_webdriver():
    """Create and return a configured Chrome WebDriver."""
    try:
        options = create_chrome_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
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

    @staticmethod
    def like_posts(driver, scroll_limit=5):
        """
        Like all visible posts and scroll to load more posts.
        
        Args:
            driver: Selenium WebDriver instance.
            scroll_limit: Number of scrolls to perform (default is 5).
        """
        try:
            scroll_count = 0
            while scroll_count < scroll_limit:
                # Find all buttons on the page
                all_buttons = driver.find_elements(By.TAG_NAME, "button")
                logger.info(f"Found {len(all_buttons)} buttons")

                # Filter for buttons with "Like" text
                like_buttons = [btn for btn in all_buttons if "Like" in btn.text]
                logger.info(f"Found {len(like_buttons)} potential Like buttons")

                # Click each Like button
                for btn in like_buttons:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView(true);", btn)  # Ensure button is visible
                        WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(btn)
                        ).click()
                        logger.info("Clicked Like button successfully")
                        time.sleep(2)  # Small delay after clicking
                    except Exception as btn_error:
                        logger.warning(f"Failed to click Like button: {btn_error}")

                # Scroll down to load more posts
                driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                time.sleep(3)  # Allow time for new content to load
                scroll_count += 1
                logger.info(f"Scrolled {scroll_count}/{scroll_limit}")

        except Exception as e:
            logger.error(f"Error during liking posts: {e}")
            driver.save_screenshot("like_posts_error.png")
            raise



    @staticmethod
    def post_comments(driver, comment_list, scroll_limit=2):
        """
        Post comments on LinkedIn posts with random text from the given list.
        """
        count = 0
        try:
            scroll_count = 0
            while scroll_count < scroll_limit:
                # Find all "Comment" buttons
                comment_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Comment')]")
                logger.info(f"Found {len(comment_buttons)} Comment buttons")

                # Click each "Comment" button and post a random comment
                for btn in comment_buttons:
                    try:
                        # Scroll to the button to ensure it is visible
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                        time.sleep(1)  # Allow page to stabilize

                        # Check if button is clickable
                        WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(btn)
                        )

                        # Use JavaScript to click if intercepted
                        try:
                            btn.click()
                            logger.info("Clicked Comment button")
                            time.sleep(2)
                            count += 1
                            logger.info(f"Posted comment {count}")
                        except Exception as e:
                            logger.warning(f"Button click intercepted, using JS click: {e}")
                            driver.execute_script("arguments[0].click();", btn)

                        # # Wait for the comment box to appear
                        # comment_box = WebDriverWait(driver, 5).until(
                        # EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @role='textbox']"))
                        # )

                        # # Type a random comment
                        # random_comment = random.choice(comment_list)
                        # comment_box.send_keys(random_comment)
                        # logger.info(f"Typed comment: {random_comment}")
                        # time.sleep(2)

                        # # Submit the comment
                        # try:
                        #     # Wait for the button to be clickable
                        #     comment_button = WebDriverWait(driver, 10).until(
                        #         EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'comments-comment-box__submit-button')]"))
                        #     )
                        #     # Scroll the button into view (if necessary)
                        #     driver.execute_script("arguments[0].scrollIntoView(true);", comment_button)
                        #     driver.execute_script("arguments[0].click();", comment_button)
                        #     print("Comment button clicked successfully.")
                        # except Exception as e:
                        #     print(f"Error clicking the comment button: {e}")
                    except Exception as btn_error:
                        logger.warning(f"Failed to comment: {btn_error}")
                        continue

                # Scroll down to load more posts
                driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                time.sleep(3)  # Allow time for new content to load
                scroll_count += 1
                logger.info(f"Scrolled {scroll_count}/{scroll_limit}")

        except Exception as e:
            logger.error(f"Error during commenting: {e}")
            driver.save_screenshot("comment_error.png")
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
    POST = 'comment'
    # POST = 'like'
    keyword = None
    try:
        # keyword = random_choice_url()
        # logger.info(f"Selected search URL: {keyword}")

        driver = create_webdriver()
        LinkedinAutomate.login(driver)
        logger.info("LinkedIn automation completed successfully")
        if POST == 'like':
            LinkedinAutomate.like_posts(driver)
        elif POST == 'comment':
            LinkedinAutomate.post_comments(driver, comment_list)
        else:
            search_profiles(driver=driver, keyword=keyword, limit=10, page_no=10)

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
