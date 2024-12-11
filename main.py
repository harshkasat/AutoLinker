from LinkedinAutomation import LinkedInAutomation, ChromeDriver, COMMENT_LIST
from LinkedinAutomation.connections_linkedin import search_profiles
from LinkedinAutomation.likes_linkedin_posts import like_posts
from LinkedinAutomation.comments_linkedin_posts import post_comments
from utils import linkedin_args_parser
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

def send_connection_on_linkedin(driver: webdriver, page_limit: Optional[int] = 10):
    """Send Connection Requests on LinkedIn."""
    try:
        search_profiles(driver, page_limit=page_limit)
    except Exception as e:
        logger.error(f"Error in sending connection: {e}")
        driver.save_screenshot("error.png")

def likes_linkedin_posts(driver: webdriver, scroll_limit: Optional[int] = 5):
    """Like LinkedIn Posts."""
    try:
        like_posts(driver=driver, scroll_limit=scroll_limit)
    except Exception as e:
        logger.error(f"Error in liking posts: {e}")
        driver.save_screenshot("like_error.png")
        raise

def post_comments_on_linkedin(driver: webdriver, scroll_limit: Optional[int] = 2):
    """Post Comments on LinkedIn Posts."""
    try:
        post_comments(driver=driver, comment_list=COMMENT_LIST, scroll_limit=scroll_limit)
    except Exception as e:
        logger.error(f"Error in posting comments: {e}")
        driver.save_screenshot("comment_error.png")
        raise

def main():
    
    args = linkedin_args_parser()
    driver = ChromeDriver().create_webdriver()
    LinkedInAutomation().login(driver)

    try:
        if args.send_connections:
            connection_limit = args.connection_limit if args.connection_limit else 8  # default to 8 pages if not provided by user
            send_connection_on_linkedin(driver=driver, page_limit=connection_limit)

        if args.like_posts:
            like_scroll_limit = args.like_scroll_limit if args.like_scroll_limit else 5 # default to 5 pages if not provided by user
            likes_linkedin_posts(driver=driver, scroll_limit=like_scroll_limit)

        if args.comment_posts:
            comment_scroll_limit = args.comment_scroll_limit if args.comment_scroll_limit else 5 # default to 5 pages if not provided by user
            post_comments_on_linkedin(driver=driver, scroll_limit=comment_scroll_limit)

    except Exception as e:
        logger.error(f"LinkedIn automation failed: {e}")
        if driver:
            driver.save_screenshot('linkedin_automation_error.png')
        raise

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
