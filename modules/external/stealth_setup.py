'''
Selenium Stealth Setup
Configures Selenium to avoid bot detection.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

from selenium.webdriver.remote.webdriver import WebDriver
from selenium_stealth import stealth
from fake_useragent import UserAgent
from modules.helpers import print_lg


def apply_stealth(driver: WebDriver) -> None:
    '''
    Apply stealth settings to Selenium WebDriver.
    Makes the bot harder to detect.
    '''
    try:
        # Get a realistic user agent
        ua = UserAgent()
        user_agent = ua.random
        
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            user_agent=user_agent
        )
        
        print_lg("Selenium Stealth applied successfully")
        print_lg(f"User-Agent: {user_agent[:50]}...")
        
    except Exception as e:
        print_lg(f"Failed to apply Selenium Stealth: {e}")
        print_lg("Continuing without stealth mode...")


def get_random_user_agent() -> str:
    '''
    Get a random realistic user agent string.
    '''
    try:
        ua = UserAgent()
        return ua.random
    except:
        # Fallback user agent
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
