'''
Retry Handler Module
Provides retry logic with exponential backoff for failed actions.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

from time import sleep
from random import uniform
from typing import Callable, Any, List
from selenium.common.exceptions import WebDriverException
from modules.helpers import print_lg

def exponential_backoff(attempt: int, base_delay: float = 2.0) -> float:
    '''
    Calculate exponential backoff delay.
    * `attempt` - Current attempt number (0-indexed)
    * `base_delay` - Base delay in seconds
    * Returns delay in seconds with jitter
    '''
    delay = base_delay * (2 ** attempt)
    jitter = uniform(0, delay * 0.1)  # Add 10% jitter
    return delay + jitter


def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 2.0,
    exceptions: tuple = (Exception,),
    on_retry: Callable = None
) -> Any:
    '''
    Retry a function with exponential backoff.
    * `func` - Function to retry
    * `max_retries` - Maximum number of retry attempts
    * `base_delay` - Base delay for exponential backoff
    * `exceptions` - Tuple of exceptions to catch
    * `on_retry` - Optional callback function called on each retry
    * Returns the result of the function or raises the last exception
    '''
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            if attempt < max_retries:
                delay = exponential_backoff(attempt, base_delay)
                print_lg(f"Attempt {attempt + 1}/{max_retries + 1} failed: {str(e)[:100]}. Retrying in {delay:.2f}s...")
                if on_retry:
                    on_retry(attempt, e)
                sleep(delay)
            else:
                print_lg(f"All {max_retries + 1} attempts failed.")
    
    raise last_exception


def retry_click(driver, xpath: str, max_retries: int = 3, fallback_xpaths: List[str] = None) -> bool:
    '''
    Retry clicking an element with fallback selectors.
    * `driver` - Selenium WebDriver instance
    * `xpath` - Primary XPath selector
    * `max_retries` - Number of retries per selector
    * `fallback_xpaths` - List of fallback XPath selectors
    * Returns True if successful, False otherwise
    '''
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    xpaths_to_try = [xpath] + (fallback_xpaths or [])
    
    for xpath_selector in xpaths_to_try:
        try:
            def click_action():
                element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_selector))
                )
                element.click()
                return True
            
            return retry_with_backoff(
                click_action,
                max_retries=max_retries,
                base_delay=1.0,
                exceptions=(WebDriverException,)
            )
        except Exception as e:
            print_lg(f"Failed to click with selector: {xpath_selector[:50]}...")
            continue
    
    return False


def safe_execute(func: Callable, default_return: Any = None, log_error: bool = True) -> Any:
    '''
    Safely execute a function and return a default value on error.
    * `func` - Function to execute
    * `default_return` - Value to return on error
    * `log_error` - Whether to log errors
    * Returns function result or default_return on error
    '''
    try:
        return func()
    except Exception as e:
        if log_error:
            print_lg(f"Safe execute caught error: {str(e)[:100]}")
        return default_return
