'''
Smart Job Filtering Module
Intelligent filtering to skip irrelevant jobs.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from modules.helpers import print_lg

def extract_applicant_count(driver: WebDriver, job_element: WebElement = None) -> int | None:
    '''
    Extract the number of applicants for a job.
    * `driver` - Selenium WebDriver instance
    * `job_element` - Job element (uses current page if None)
    * Returns applicant count or None if not found
    '''
    try:
        # Try to find applicant count in job details
        applicant_text = None
        
        # Try multiple selectors
        selectors = [
            ".//span[contains(text(), 'applicant')]",
            ".//span[contains(text(), 'applications')]",
            ".//li[contains(@class, 'job-details') and contains(., 'applicant')]"
        ]
        
        search_element = job_element if job_element else driver
        
        for selector in selectors:
            try:
                element = search_element.find_element(By.XPATH, selector)
                applicant_text = element.text
                break
            except:
                continue
        
        if not applicant_text:
            return None
        
        # Extract number from text like "50 applicants" or "Over 100 applicants"
        import re
        
        # Handle "Over X" format
        if "over" in applicant_text.lower():
            match = re.search(r'over\s+(\d+)', applicant_text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Handle regular number format
        match = re.search(r'(\d+)', applicant_text)
        if match:
            return int(match.group(1))
        
        return None
    except Exception as e:
        print_lg(f"Failed to extract applicant count: {e}")
        return None


def should_skip_high_applicants(driver: WebDriver, threshold: int = 200) -> tuple[bool, str | None]:
    '''
    Check if job should be skipped due to high applicant count.
    * `driver` - Selenium WebDriver instance
    * `threshold` - Maximum acceptable applicant count
    * Returns (should_skip, reason)
    '''
    try:
        applicant_count = extract_applicant_count(driver)
        
        if applicant_count is None:
            return False, None
        
        if applicant_count > threshold:
            reason = f"Too many applicants ({applicant_count} > {threshold})"
            return True, reason
        
        return False, None
    except Exception as e:
        print_lg(f"Error checking applicant count: {e}")
        return False, None


def match_title_keywords(title: str, required_keywords: List[str], exclude_keywords: List[str] = None) -> tuple[bool, str | None]:
    '''
    Check if job title matches required keywords and doesn't contain excluded keywords.
    * `title` - Job title
    * `required_keywords` - Keywords that must be present (empty list = no requirement)
    * `exclude_keywords` - Keywords that must NOT be present
    * Returns (should_skip, reason)
    '''
    title_lower = title.lower()
    
    # Check excluded keywords first
    if exclude_keywords:
        for keyword in exclude_keywords:
            if keyword.lower() in title_lower:
                return True, f'Title contains excluded keyword "{keyword}"'
    
    # Check required keywords
    if required_keywords:
        has_required = any(keyword.lower() in title_lower for keyword in required_keywords)
        if not has_required:
            return True, f"Title doesn't match required keywords: {required_keywords}"
    
    return False, None


def calculate_job_relevance_score(
    title: str,
    description: str,
    preferred_keywords: List[str],
    applicant_count: int = None,
    max_applicants: int = 200
) -> float:
    '''
    Calculate a relevance score for a job (0.0 to 1.0).
    * Higher score = more relevant
    * Returns score between 0.0 and 1.0
    '''
    score = 0.5  # Base score
    
    title_lower = title.lower()
    desc_lower = description.lower() if description else ""
    
    # Keyword matching (up to +0.3)
    if preferred_keywords:
        keyword_matches = sum(1 for kw in preferred_keywords if kw.lower() in title_lower or kw.lower() in desc_lower)
        keyword_score = min(keyword_matches / len(preferred_keywords), 1.0) * 0.3
        score += keyword_score
    
    # Applicant count penalty (up to -0.3)
    if applicant_count is not None and max_applicants > 0:
        if applicant_count > max_applicants:
            penalty = min((applicant_count - max_applicants) / max_applicants, 1.0) * 0.3
            score -= penalty
    
    # Ensure score is between 0 and 1
    return max(0.0, min(1.0, score))
