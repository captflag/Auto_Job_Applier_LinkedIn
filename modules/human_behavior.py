'''
Human Behavior Simulation Module
Simulates human-like behavior to avoid bot detection.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

from time import sleep
from random import uniform, randint, choice
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from modules.helpers import print_lg

def simulate_reading(min_seconds: float = 5.0, max_seconds: float = 15.0) -> None:
    '''
    Simulate time spent reading content.
    * `min_seconds` - Minimum reading time
    * `max_seconds` - Maximum reading time
    '''
    reading_time = uniform(min_seconds, max_seconds)
    print_lg(f"Simulating reading for {reading_time:.2f} seconds...")
    sleep(reading_time)


def random_mouse_movement(driver: WebDriver, actions: ActionChains, num_movements: int = 3) -> None:
    '''
    Simulate random mouse movements.
    * `driver` - Selenium WebDriver instance
    * `actions` - ActionChains instance
    * `num_movements` - Number of random movements
    '''
    try:
        for _ in range(num_movements):
            x_offset = randint(-100, 100)
            y_offset = randint(-100, 100)
            actions.move_by_offset(x_offset, y_offset).perform()
            sleep(uniform(0.1, 0.3))
    except Exception as e:
        print_lg(f"Mouse movement simulation failed: {e}")


def human_like_scroll(driver: WebDriver, element: WebElement = None, smooth: bool = True) -> None:
    '''
    Scroll in a human-like manner.
    * `driver` - Selenium WebDriver instance
    * `element` - Element to scroll to (None for page scroll)
    * `smooth` - Use smooth scrolling
    '''
    if element:
        # Scroll to element in steps
        driver.execute_script("""
            var element = arguments[0];
            var start = window.pageYOffset;
            var end = element.offsetTop - 100;
            var distance = end - start;
            var duration = 500;
            var startTime = null;
            
            function animation(currentTime) {
                if (startTime === null) startTime = currentTime;
                var timeElapsed = currentTime - startTime;
                var progress = Math.min(timeElapsed / duration, 1);
                window.scrollTo(0, start + distance * progress);
                if (timeElapsed < duration) {
                    requestAnimationFrame(animation);
                }
            }
            requestAnimationFrame(animation);
        """, element)
        sleep(uniform(0.5, 1.0))
    else:
        # Random page scroll
        scroll_amount = randint(100, 500)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        sleep(uniform(0.3, 0.7))


def typing_with_delays(element: WebElement, text: str, min_delay: float = 0.05, max_delay: float = 0.15) -> None:
    '''
    Type text with human-like delays between keystrokes.
    * `element` - Input element
    * `text` - Text to type
    * `min_delay` - Minimum delay between keys
    * `max_delay` - Maximum delay between keys
    '''
    element.clear()
    for char in text:
        element.send_keys(char)
        sleep(uniform(min_delay, max_delay))
        # Occasional longer pause (simulating thinking)
        if randint(1, 20) == 1:
            sleep(uniform(0.3, 0.8))


def random_pause(min_seconds: float = 1.0, max_seconds: float = 3.0, probability: float = 0.3) -> None:
    '''
    Randomly pause with given probability.
    * `min_seconds` - Minimum pause duration
    * `max_seconds` - Maximum pause duration
    * `probability` - Probability of pausing (0.0 to 1.0)
    '''
    if uniform(0, 1) < probability:
        pause_time = uniform(min_seconds, max_seconds)
        print_lg(f"Random pause for {pause_time:.2f} seconds...")
        sleep(pause_time)


def simulate_distraction() -> None:
    '''
    Simulate getting distracted (random longer pause).
    '''
    if randint(1, 50) == 1:  # 2% chance
        distraction_time = uniform(5, 15)
        print_lg(f"Simulating distraction for {distraction_time:.2f} seconds...")
        sleep(distraction_time)
