'''
ATS Platform Detector
Detects which Applicant Tracking System is being used.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

from selenium.webdriver.remote.webdriver import WebDriver
from modules.helpers import print_lg

# ATS URL patterns
ATS_PATTERNS = {
    'greenhouse': [
        'greenhouse.io',
        'boards.greenhouse.io',
        'job-boards.greenhouse.io'
    ],
    'lever': [
        'lever.co',
        'jobs.lever.co'
    ],
    'workday': [
        'myworkdayjobs.com',
        'wd1.myworkdayjobs.com',
        'wd5.myworkdayjobs.com'
    ],
    'taleo': [
        'taleo.net',
        'tbe.taleo.net'
    ],
    'icims': [
        'icims.com',
        'careers.icims.com'
    ],
    'bamboohr': [
        'bamboohr.com'
    ],
    'jobvite': [
        'jobvite.com'
    ],
    'smartrecruiters': [
        'smartrecruiters.com'
    ]
}

# DOM structure signatures
ATS_DOM_SIGNATURES = {
    'greenhouse': [
        'div[id*="application"]',
        'div[class*="application"]',
        'form[id*="greenhouse"]'
    ],
    'lever': [
        'div[class*="posting"]',
        'div[class*="application-form"]'
    ]
}


def detect_ats_from_url(url: str) -> str:
    '''
    Detect ATS platform from URL.
    * Returns: 'greenhouse', 'lever', 'workday', 'taleo', 'icims', or 'unknown'
    '''
    url_lower = url.lower()
    
    for ats_name, patterns in ATS_PATTERNS.items():
        for pattern in patterns:
            if pattern in url_lower:
                print_lg(f"Detected ATS from URL: {ats_name}")
                return ats_name
    
    return 'unknown'


def detect_ats_from_dom(driver: WebDriver) -> str:
    '''
    Detect ATS platform from DOM structure.
    * Returns: ATS platform name or 'unknown'
    '''
    try:
        from selenium.webdriver.common.by import By
        
        for ats_name, selectors in ATS_DOM_SIGNATURES.items():
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print_lg(f"Detected ATS from DOM: {ats_name}")
                        return ats_name
                except:
                    continue
        
        return 'unknown'
    except Exception as e:
        print_lg(f"Error detecting ATS from DOM: {e}")
        return 'unknown'


def detect_ats_platform(driver: WebDriver) -> str:
    '''
    Detect ATS platform using multiple methods.
    * Returns: ATS platform name or 'unknown'
    '''
    current_url = driver.current_url
    
    # Try URL detection first (most reliable)
    ats = detect_ats_from_url(current_url)
    if ats != 'unknown':
        return ats
    
    # Fallback to DOM detection
    ats = detect_ats_from_dom(driver)
    return ats


def is_supported_ats(ats_platform: str, supported_platforms: list) -> bool:
    '''
    Check if ATS platform is supported.
    * Returns: True if supported, False otherwise
    '''
    return ats_platform in supported_platforms
