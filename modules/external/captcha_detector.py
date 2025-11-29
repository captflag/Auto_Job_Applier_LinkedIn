'''
CAPTCHA Detector
Detects presence of CAPTCHA challenges.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from modules.helpers import print_lg


def detect_captcha(driver: WebDriver) -> tuple[bool, str]:
    '''
    Detect if CAPTCHA is present on the page.
    * Returns: (has_captcha, captcha_type)
    '''
    try:
        # Check for reCAPTCHA
        recaptcha_selectors = [
            'iframe[src*="recaptcha"]',
            'div[class*="recaptcha"]',
            'div[id*="recaptcha"]',
            '.g-recaptcha',
            '#g-recaptcha'
        ]
        
        for selector in recaptcha_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print_lg("Detected reCAPTCHA on page")
                    return True, "recaptcha"
            except:
                continue
        
        # Check for hCaptcha
        hcaptcha_selectors = [
            'iframe[src*="hcaptcha"]',
            'div[class*="hcaptcha"]',
            '.h-captcha'
        ]
        
        for selector in hcaptcha_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print_lg("Detected hCaptcha on page")
                    return True, "hcaptcha"
            except:
                continue
        
        # Check for Cloudflare challenge
        if "cloudflare" in driver.page_source.lower() and "challenge" in driver.page_source.lower():
            print_lg("Detected Cloudflare challenge")
            return True, "cloudflare"
        
        # Check for generic CAPTCHA text
        page_text = driver.page_source.lower()
        captcha_keywords = ['captcha', 'verify you are human', 'security check', 'bot check']
        for keyword in captcha_keywords:
            if keyword in page_text:
                print_lg(f"Detected potential CAPTCHA (keyword: {keyword})")
                return True, "unknown"
        
        return False, "none"
        
    except Exception as e:
        print_lg(f"Error detecting CAPTCHA: {e}")
        return False, "error"


def should_skip_captcha_site(driver: WebDriver, skip_captcha: bool = True) -> bool:
    '''
    Check if site should be skipped due to CAPTCHA.
    * Returns: True if should skip, False otherwise
    '''
    if not skip_captcha:
        return False
    
    has_captcha, captcha_type = detect_captcha(driver)
    
    if has_captcha:
        print_lg(f"CAPTCHA detected ({captcha_type}). Skipping this site.")
        return True
    
    return False
