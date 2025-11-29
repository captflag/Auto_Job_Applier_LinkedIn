'''
Pre-flight Checks Module
Validates configuration and environment before starting the bot.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

import os
from typing import List, Tuple
from modules.helpers import print_lg

def validate_resume_exists(resume_path: str) -> Tuple[bool, str]:
    '''
    Check if resume file exists.
    * Returns (is_valid, message)
    '''
    if not resume_path or resume_path == "":
        return False, "Resume path is empty"
    
    if not os.path.exists(resume_path):
        return False, f"Resume file not found: {resume_path}"
    
    if not resume_path.lower().endswith('.pdf'):
        return False, "Resume must be a PDF file"
    
    file_size = os.path.getsize(resume_path)
    if file_size == 0:
        return False, "Resume file is empty"
    
    if file_size > 5 * 1024 * 1024:  # 5MB
        return False, f"Resume file is too large ({file_size / 1024 / 1024:.2f}MB > 5MB)"
    
    return True, f"Resume validated: {os.path.basename(resume_path)}"


def validate_ai_credentials(use_ai: bool, ai_provider: str, api_key: str) -> Tuple[bool, str]:
    '''
    Validate AI configuration.
    * Returns (is_valid, message)
    '''
    if not use_ai:
        return True, "AI is disabled"
    
    if not ai_provider or ai_provider == "":
        return False, "AI provider not specified"
    
    if not api_key or api_key == "" or "YOUR_API_KEY" in api_key:
        return False, f"Invalid API key for {ai_provider}"
    
    return True, f"AI configured: {ai_provider}"


def validate_search_terms(search_terms: List[str]) -> Tuple[bool, str]:
    '''
    Validate search terms configuration.
    * Returns (is_valid, message)
    '''
    if not search_terms or len(search_terms) == 0:
        return False, "No search terms configured"
    
    if any(term.strip() == "" for term in search_terms):
        return False, "Empty search term found"
    
    return True, f"{len(search_terms)} search term(s) configured"


def validate_credentials(username: str, password: str) -> Tuple[bool, str]:
    '''
    Validate LinkedIn credentials.
    * Returns (is_valid, message)
    '''
    if not username or username == "" or "YOUR_USERNAME" in username:
        return False, "LinkedIn username not configured (will use saved profile)"
    
    if not password or password == "" or "YOUR_PASSWORD" in password:
        return False, "LinkedIn password not configured (will use saved profile)"
    
    return True, "LinkedIn credentials configured"


def check_disk_space(required_mb: int = 100) -> Tuple[bool, str]:
    '''
    Check if sufficient disk space is available.
    * Returns (is_valid, message)
    '''
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        free_mb = free // (1024 * 1024)
        
        if free_mb < required_mb:
            return False, f"Low disk space: {free_mb}MB available (need {required_mb}MB)"
        
        return True, f"Disk space OK: {free_mb}MB available"
    except Exception as e:
        return True, f"Could not check disk space: {e}"


def run_all_checks(
    resume_path: str,
    use_ai: bool,
    ai_provider: str,
    api_key: str,
    search_terms: List[str],
    username: str,
    password: str
) -> Tuple[bool, List[str]]:
    '''
    Run all pre-flight checks.
    * Returns (all_passed, messages)
    '''
    messages = []
    all_passed = True
    
    print_lg("\n" + "="*60)
    print_lg("PRE-FLIGHT CHECKS")
    print_lg("="*60)
    
    # Resume check
    is_valid, msg = validate_resume_exists(resume_path)
    status = "✓" if is_valid else "✗"
    print_lg(f"{status} Resume: {msg}")
    messages.append(msg)
    if not is_valid:
        all_passed = False
    
    # AI check
    is_valid, msg = validate_ai_credentials(use_ai, ai_provider, api_key)
    status = "✓" if is_valid else "✗"
    print_lg(f"{status} AI: {msg}")
    messages.append(msg)
    if not is_valid and use_ai:
        all_passed = False
    
    # Search terms check
    is_valid, msg = validate_search_terms(search_terms)
    status = "✓" if is_valid else "✗"
    print_lg(f"{status} Search Terms: {msg}")
    messages.append(msg)
    if not is_valid:
        all_passed = False
    
    # Credentials check
    is_valid, msg = validate_credentials(username, password)
    status = "✓" if is_valid else "⚠"
    print_lg(f"{status} Credentials: {msg}")
    messages.append(msg)
    
    # Disk space check
    is_valid, msg = check_disk_space()
    status = "✓" if is_valid else "⚠"
    print_lg(f"{status} Disk Space: {msg}")
    messages.append(msg)
    
    print_lg("="*60)
    
    if all_passed:
        print_lg("✓ All critical checks passed!\n")
    else:
        print_lg("✗ Some checks failed. Please fix the issues above.\n")
    
    return all_passed, messages
