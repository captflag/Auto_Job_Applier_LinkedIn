'''
Greenhouse Handler
Handles job applications on Greenhouse ATS platform.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.helpers import print_lg, buffer
from modules.external.universal_form_filler import detect_field_type, fill_field, upload_file_drag_drop
from modules.external.field_knowledge_base import FieldKnowledgeBase
from typing import Dict


def is_greenhouse_site(driver: WebDriver) -> bool:
    '''
    Check if current site is Greenhouse.
    '''
    url = driver.current_url.lower()
    return 'greenhouse.io' in url or 'boards.greenhouse.io' in url


def fill_greenhouse_application(
    driver: WebDriver,
    user_data: Dict,
    resume_path: str,
    knowledge_base: FieldKnowledgeBase = None,
    gemini_client = None
) -> tuple[bool, str]:
    '''
    Fill out a Greenhouse application form.
    * Returns: (success, message)
    '''
    try:
        print_lg("Starting Greenhouse application...")
        
        # Wait for form to load
        wait = WebDriverWait(driver, 10)
        
        # Find all input fields
        input_fields = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"], input[type="email"], input[type="tel"]')
        
        filled_count = 0
        for field in input_fields:
            try:
                # Detect field type
                field_type = detect_field_type(field, knowledge_base, 'greenhouse')
                
                if field_type == 'unknown' and gemini_client:
                    # Use Gemini for unknown fields
                    from modules.external.universal_form_filler import classify_field_with_gemini
                    field_info = {
                        'label': field.get_attribute('aria-label') or '',
                        'name': field.get_attribute('name') or '',
                        'id': field.get_attribute('id') or '',
                        'placeholder': field.get_attribute('placeholder') or '',
                        'type': field.get_attribute('type') or 'text'
                    }
                    field_type = classify_field_with_gemini(gemini_client, field_info)
                
                # Fill field
                if field_type != 'unknown':
                    success = fill_field(field, field_type, user_data)
                    if success:
                        filled_count += 1
                        # Learn this mapping
                        if knowledge_base:
                            field_name = field.get_attribute('name') or field.get_attribute('id')
                            if field_name:
                                knowledge_base.learn_field_mapping(field_name, field_type, 'greenhouse')
                
            except Exception as e:
                print_lg(f"Error filling field: {e}")
                continue
        
        print_lg(f"Filled {filled_count} fields")
        
        # Handle resume upload
        try:
            file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
            for file_input in file_inputs:
                if resume_path:
                    upload_file_drag_drop(driver, file_input, resume_path)
                    print_lg("Resume uploaded successfully")
                    break
        except Exception as e:
            print_lg(f"Resume upload failed: {e}")
        
        # Look for submit button
        try:
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button[id*="submit"]',
                'button[class*="submit"]',
                'button:contains("Submit")',
                'button:contains("Apply")'
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = driver.find_element(By.CSS_SELECTOR, selector)
                    print_lg(f"Found submit button: {submit_button.text}")
                    # Don't auto-submit yet, just report success
                    return True, f"Form filled successfully ({filled_count} fields)"
                except:
                    continue
                    
        except Exception as e:
            print_lg(f"Could not find submit button: {e}")
        
        if filled_count > 0:
            return True, f"Partially filled ({filled_count} fields), manual submission needed"
        else:
            return False, "No fields were filled"
        
    except Exception as e:
        error_msg = f"Greenhouse application failed: {str(e)}"
        print_lg(error_msg)
        return False, error_msg


def submit_greenhouse_application(driver: WebDriver) -> tuple[bool, str]:
    '''
    Submit the Greenhouse application.
    * Returns: (success, message)
    '''
    try:
        # Find and click submit button
        submit_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button[id*="submit"]',
            'button[class*="submit"]'
        ]
        
        for selector in submit_selectors:
            try:
                submit_button = driver.find_element(By.CSS_SELECTOR, selector)
                submit_button.click()
                buffer(2)
                
                # Check for success message
                success_indicators = [
                    'thank you',
                    'application submitted',
                    'application received',
                    'we\'ll be in touch'
                ]
                
                page_text = driver.page_source.lower()
                for indicator in success_indicators:
                    if indicator in page_text:
                        print_lg("Application submitted successfully!")
                        return True, "Application submitted"
                
                return True, "Submit button clicked (verification needed)"
                
            except:
                continue
        
        return False, "Could not find submit button"
        
    except Exception as e:
        return False, f"Submission failed: {str(e)}"
