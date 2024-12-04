import logging
import time
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


def like_posts(driver, scroll_limit=5):
    try:
        scroll_count = 0
        while scroll_count < scroll_limit:
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            logger.info(f"Found {len(all_buttons)} buttons")

            like_buttons = [btn for btn in all_buttons if "Like" in btn.text]
            logger.info(f"Found {len(like_buttons)} potential Like buttons")

            for btn in like_buttons:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(btn)
                    ).click()
                    logger.info("Clicked Like button successfully")
                    time.sleep(2)
                except Exception as e:
                    logger.warning(f"Failed to click Like button, using JS click: {e}")
                    driver.execute_script("arguments[0].click();", btn)

            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(3)
            scroll_count += 1
            logger.info(f"Scrolled {scroll_count}/{scroll_limit}")

    except Exception as e:
        logger.error(f"Error during liking posts: {e}")
        driver.save_screenshot("like_posts_error.png")
        raise
