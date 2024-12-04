from LinkedinAutomation import LinkedInAutomation, ChromeDriver, COMMENT_LIST
from LinkedinAutomation.connections_linkedin import search_profiles
from LinkedinAutomation.likes_linkedin_posts import like_posts
from LinkedinAutomation.comments_linkedin_posts import post_comments
from selenium import webdriver
import logging
from typing import Optional

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


def send_connection_on_linkedin(driver:webdriver, limit:Optional[int] = 10):
    # Send Connection to LinkedIn
    try:
        # Search for profiles
        search_profiles(driver, limit=limit)
    except Exception as e:
        logger.error(f"Error in sending connection: {e}")
        driver.save_screenshot("error.png") 

def likes_linkedin_posts(driver:webdriver, scroll_limit:Optional[int] = 5):
    #  Likes to Linkedin Posts
    try:
        like_posts(driver=driver, scroll_limit=scroll_limit)
    except Exception as e:
        logger.error(f"Error in liking posts: {e}")
        driver.save_screenshot("like_error.png")
        raise

def post_comments_on_linkedin(driver:webdriver, scroll_limit:Optional[int] = 2):
    # Post Comments on Linkedin Posts
    try:
        post_comments(driver=driver, comment_list=COMMENT_LIST, scroll_limit=scroll_limit)
    except Exception as e:
        logger.error(f"Error in posting comments: {e}")
        driver.save_screenshot("comment_error.png")
        raise


def main():
    """Main function to run the LinkedIn automation."""
    # Create an instance of the LinkedInAutomation class
    driver = ChromeDriver().create_webdriver()
    LinkedInAutomation().login(driver)
    try:
        # send_connection_on_linkedin(driver=driver)
        likes_linkedin_posts(driver=driver)
        # post_comments_on_linkedin(driver=driver)
    except Exception as e:
        logger.error(f"LinkedIn automation failed: {e}")
        if driver:
            driver.save_screenshot('linkedin_automation_error.png')
        raise
    
    finally:
        # Close the browser
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
