'''
Universal Form Filler
AI-powered form filling using Gemini for field classification.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from typing import Dict, List
from modules.helpers import print_lg
from modules.external.field_knowledge_base import FieldKnowledgeBase
import re


# Standard field mappings
STANDARD_FIELD_PATTERNS = {
    'first_name': [
        'first_name', 'firstname', 'fname', 'given_name', 'forename',
        'first name', 'given name'
    ],
    'last_name': [
        'last_name', 'lastname', 'lname', 'surname', 'family_name',
        'last name', 'family name'
    ],
    'full_name': [
        'full_name', 'fullname', 'name', 'your_name', 'applicant_name',
        'full name', 'your name'
    ],
    'email': [
        'email', 'email_address', 'e_mail', 'mail', 'contact_email',
        'email address', 'e-mail'
    ],
    'phone': [
        'phone', 'phone_number', 'mobile', 'telephone', 'contact_number',
        'phone number', 'mobile number', 'tel'
    ],
    'linkedin': [
        'linkedin', 'linkedin_url', 'linkedin_profile', 'linkedin url'
    ],
    'website': [
        'website', 'portfolio', 'personal_website', 'url', 'homepage'
    ],
    'github': [
        'github', 'github_url', 'github_username'
    ]
}


def classify_field_with_gemini(gemini_client, field_info: Dict) -> str:
    '''
    Use Gemini AI to classify what a form field is asking for.
    * Returns: field type (e.g., 'first_name', 'email', etc.)
    '''
    try:
        from modules.ai.geminiConnections import gemini_completion
        
        prompt = f"""You are analyzing a form field to determine what information it's asking for.

Field Information:
- Label: {field_info.get('label', 'N/A')}
- Name attribute: {field_info.get('name', 'N/A')}
- ID attribute: {field_info.get('id', 'N/A')}
- Placeholder: {field_info.get('placeholder', 'N/A')}
- Type: {field_info.get('type', 'text')}

Classify this field into ONE of these categories:
first_name, last_name, full_name, email, phone, linkedin, website, github, address, city, state, zip, country, resume, cover_letter, unknown

Respond with ONLY the category name, nothing else."""

        messages = [{"role": "user", "content": prompt}]
        response = gemini_completion(gemini_client, messages, stream=False)
        
        field_type = response.strip().lower()
        print_lg(f"Gemini classified field as: {field_type}")
        return field_type
        
    except Exception as e:
        print_lg(f"Gemini classification failed: {e}")
        return 'unknown'


def detect_field_type(field: WebElement, knowledge_base: FieldKnowledgeBase = None, ats_platform: str = "unknown") -> str:
    '''
    Detect what type of information a field is asking for.
    Uses pattern matching first, then knowledge base, then returns unknown.
    '''
    try:
        # Get field attributes
        field_name = field.get_attribute('name') or ''
        field_id = field.get_attribute('id') or ''
        field_placeholder = field.get_attribute('placeholder') or ''
        
        # Try to find label
        label_text = ''
        try:
            label = field.find_element(By.XPATH, './preceding::label[1]')
            label_text = label.text
        except:
            pass
        
        # Combine all text for matching
        combined_text = f"{field_name} {field_id} {field_placeholder} {label_text}".lower()
        
        # Check knowledge base first
        if knowledge_base:
            for identifier in [field_name, field_id]:
                if identifier:
                    known_type = knowledge_base.get_field_type(identifier, ats_platform)
                    if known_type:
                        print_lg(f"Found in knowledge base: {identifier} → {known_type}")
                        return known_type
        
        # Pattern matching
        for field_type, patterns in STANDARD_FIELD_PATTERNS.items():
            for pattern in patterns:
                if pattern in combined_text:
                    return field_type
        
        return 'unknown'
        
    except Exception as e:
        print_lg(f"Error detecting field type: {e}")
        return 'unknown'


def fill_field(field: WebElement, field_type: str, user_data: Dict) -> bool:
    '''
    Fill a form field with appropriate data.
    * Returns: True if successful, False otherwise
    '''
    try:
        value = user_data.get(field_type, '')
        if not value:
            print_lg(f"No data available for field type: {field_type}")
            return False
        
        # Clear existing value
        field.clear()
        
        # Fill with value
        field.send_keys(str(value))
        print_lg(f"Filled {field_type} with: {str(value)[:50]}")
        return True
        
    except Exception as e:
        print_lg(f"Failed to fill field: {e}")
        return False


def upload_file_drag_drop(driver: WebDriver, file_input: WebElement, file_path: str) -> bool:
    '''
    Upload file using drag-and-drop simulation.
    Fallback to standard upload if drag-drop fails.
    '''
    try:
        # Try standard upload first (works 90% of the time)
        file_input.send_keys(file_path)
        print_lg(f"File uploaded successfully: {file_path}")
        return True
        
    except Exception as e:
        print_lg(f"Standard file upload failed: {e}")
        
        # Try JavaScript drag-drop simulation
        try:
            js_drop_file = """
                var target = arguments[0],
                    offsetX = arguments[1],
                    offsetY = arguments[2],
                    document = target.ownerDocument || document,
                    window = document.defaultView || window;

                var input = document.createElement('INPUT');
                input.type = 'file';
                input.onchange = function () {
                  var rect = target.getBoundingClientRect(),
                      x = rect.left + (offsetX || (rect.width >> 1)),
                      y = rect.top + (offsetY || (rect.height >> 1)),
                      dataTransfer = { files: this.files };

                  ['dragenter', 'dragover', 'drop'].forEach(function (name) {
                    var evt = document.createEvent('MouseEvent');
                    evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
                    evt.dataTransfer = dataTransfer;
                    target.dispatchEvent(evt);
                  });

                  setTimeout(function () { document.body.removeChild(input); }, 25);
                };
                document.body.appendChild(input);
                return input;
            """
            
            file_input_element = driver.execute_script(js_drop_file, file_input, 0, 0)
            file_input_element.send_keys(file_path)
            print_lg(f"File uploaded via drag-drop simulation: {file_path}")
            return True
            
        except Exception as e2:
            print_lg(f"Drag-drop upload also failed: {e2}")
            return False
