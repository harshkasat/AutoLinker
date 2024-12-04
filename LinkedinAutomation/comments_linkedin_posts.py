import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random



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


def post_comments(driver, comment_list, scroll_limit=2):
        """
        Post comments on LinkedIn posts with random text from the given list.
        """
        count = 0
        try:
            scroll_count = 0
            while scroll_count <= scroll_limit:
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

                        # Click the button
                        btn.click()
                        logger.info("Clicked Comment button")
                        time.sleep(2)

                        # Locate the comment box relative to the button
                        parent_container = btn.find_element(By.XPATH, "./ancestor::div[contains(@class, 'feed-shared-update-v2')]")
                        comment_box = parent_container.find_element(By.XPATH, ".//div[@contenteditable='true' and @role='textbox']")

                        # Type a random comment
                        random_comment = random.choice(comment_list)
                        comment_box.send_keys(random_comment)
                        logger.info(f"Typed comment: {random_comment}")
                        time.sleep(2)

                        # Submit the comment
                        try:
                            comment_button = parent_container.find_element(
                                By.XPATH,
                                ".//button[contains(@class, 'comments-comment-box__submit-button')]"
                            )

                            driver.execute_script("arguments[0].click();", comment_button)
                            logger.info("Comment submitted successfully")
                            count += 1
                        except Exception as e:
                            logger.warning(f"Error clicking the submit button: {e}")
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