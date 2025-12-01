# LinkedIn Auto Job Applier - Enhanced Edition 🚀

An intelligent web automation bot that streamlines your LinkedIn job search process. This enhanced version features advanced search capabilities, robust error handling, and improved application management.

**Apply to 100+ relevant jobs in less than 1 hour!** 🔥

## 🌟 Key Enhancements in This Version

This fork includes significant improvements over the original:

- ✅ **Grouped Search Terms** - Organize your job searches into targeted categories (Backend, Frontend, Full Stack, AI/ML)
- ✅ **Dynamic Time Filters** - Intelligent filtering to optimize search results and avoid premature exits
- ✅ **Enhanced Error Handling** - Robust error recovery and detailed logging for troubleshooting
- ✅ **Recruiter Tracking** - Better tracking and logging of recruiter interactions
- ✅ **Improved Search Logic** - Combined search functionality for more efficient job discovery
- ✅ **Better Reliability** - Refined codebase with removed redundancies and improved stability

## 📽️ See it in Action
[![Auto Job Applier demo video](https://github.com/GodsScion/Auto_job_applier_linkedIn/assets/100998531/429f7753-ebb0-499b-bc5e-5b4ee28c4f69)](https://youtu.be/gMbB1fWZDHw)
Click on above image to watch the demo or use this link https://youtu.be/gMbB1fWZDHw

## ✨ Content
- [Introduction](#linkedin-auto-job-applier---enhanced-edition-)
- [Key Enhancements](#-key-enhancements-in-this-version)
- [Demo Video](#%EF%B8%8F-see-it-in-action)
- [Index](#-content)
- [Install](#%EF%B8%8F-how-to-install)
- [Configure](#-how-to-configure)
- [Updates](%EF%B8%8F-major-updates-history)
- [Disclaimer](#-disclaimer)
- [Terms and Conditions](#%EF%B8%8F-terms-and-conditions)
- [License](#%EF%B8%8F-license)

<br>

## ⚙️ How to Install

[![Auto Job Applier setup tutorial video](https://github.com/user-attachments/assets/9e876187-ed3e-4fbf-bd87-4acc145880a2)](https://youtu.be/f9rdz74e1lM?si=4fRBcte0nuvr6tEH)
Click on above image to watch the tutorial for installation and configuration or use this link https://youtu.be/f9rdz74e1lM (Recommended to watch it in 2x speed)

### Prerequisites

1. **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
   - Windows users can also get it from Microsoft Store
   - ⚠️ **Important**: Make sure Python is added to your System Path

2. **Google Chrome** - [Download Chrome](https://www.google.com/chrome)
   - Install in the default location

### Installation Steps

1. **Clone this repository**
   ```bash
   git clone https://github.com/captflag/Auto_Job_Applier_LinkedIn.git
   cd Auto_Job_Applier_LinkedIn
   ```

2. **Install required Python packages**
   ```bash
   pip install undetected-chromedriver pyautogui setuptools openai flask-cors flask
   ```

3. **Chrome Driver Setup** (Optional if using stealth mode)
   - If `stealth_mode = True` in `config/settings.py`, this step is not needed
   - Otherwise, download [Chrome Driver](https://googlechromelabs.github.io/chrome-for-testing/)
   - **Windows users**: Simply run `windows-setup.bat` in the `/setup` folder for automatic installation

[back to index](#-content)

<br>

## 🔧 How to Configure

### Required Configuration

1. **Personal Information** (`config/personals.py`)
   - Enter your name, phone number, address, and other personal details
   - This information will be used to auto-fill application forms

2. **Application Questions** (`config/questions.py`)
   - Configure your standard answers for common application questions
   - Set whether to pause before submission
   - Configure behavior for unknown questions

3. **Search Preferences** (`config/search.py`) - ⭐ Enhanced in this version!
   - Define your job search criteria using **grouped search terms**:
     - Backend/Dev roles
     - Frontend/UI positions  
     - Full Stack opportunities
     - AI/ML/GenAI positions
   - Set job filters and preferences
   - Configure dynamic time filters for optimal results

4. **Secrets** (`config/secrets.py`) - Optional but recommended
   - LinkedIn credentials (username & password)
   - OpenAI API Key for AI-powered resume customization
   - ⚠️ **Note**: This file is gitignored and won't be pushed to GitHub

5. **Bot Settings** (`config/settings.py`)
   - Configure stealth mode (recommended: `True`)
   - Set click intervals and timing
   - Enable/disable background running
   - Adjust keep-awake settings

6. **Resume** (Optional)
   - Add your default resume to `all resumes/default/resume.pdf`
   - If not provided, uses your previous LinkedIn resume

### Running the Bot

```bash
# Run the job application bot
python runAiBot.py

# View applied jobs history (optional)
python app.py
# Then open http://localhost:5000 in your browser
```

[back to index](#-content)

<br>


## 📊 Enhanced Features Details

### Grouped Search Strategy
This version implements an intelligent grouped search approach:
- Searches are organized into specific job categories
- Each group is processed independently for better targeting
- Reduces search conflicts and improves result relevance

### Dynamic Time Filtering  
- Automatically adjusts time filters based on search results
- Prevents premature exits when jobs are available
- Optimizes search efficiency

### Error Handling & Logging
- Comprehensive error logging for troubleshooting
- Recruiter interaction tracking
- Detailed session summaries

<br>

## 🧑‍💻 Contributing

Contributions are welcome! If you'd like to improve this fork:
Thank you for your efforts and being a part of the community. All contributions are appreciated no matter how small or big. Once you contribute to the code base, your work will be remembered forever.

NOTE: Only Pull request to `community-version` branch will be accepted. Any other requests will be declined by default, especially to main branch.
Once your code is tested, your changes will be merged to the `main` branch in next cycle.

### Code Guidelines
  #### Functions:
  1. All functions or methods are named lower case and snake case
  2. Must have explanation of their purpose. Write explanation surrounded in `''' Explanation '''` under the definition `def function() -> None:`. Example:
      ```python
      def function() -> None:
        '''
        This function does nothing, it's just an example for explanation placement!
        '''
      ```
  4. The Types `(str, list, int, list[str], int | float)` for the parameters and returns must be given. Example:
      ```python
      def function(param1: str, param2: list[str], param3: int) -> str:
      ```
  5. Putting all that together some valid examples for function or method declarations would be as follows.
      ```python
      def function_name_in_camel_case(parameter1: driver, parameter2: str) -> list[str] | ValueError:
        '''
        This function is an example for code guidelines
        '''
        return [parameter2, parameter2.lower()]
      ```
  6. The hashtag comments on top of functions are optional, which are intended for developers `# Comments for developers`.
      ```python
      # Enter input text function
      def text_input_by_ID(driver: WebDriver, id: str, value: str, time: float=5.0) -> None | Exception:
          '''
          Enters `value` into the input field with the given `id` if found, else throws NotFoundException.
          - `time` is the max time to wait for the element to be found.
          '''
          username_field = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, id)))
          username_field.send_keys(Keys.CONTROL + "a")
          username_field.send_keys(value)
      
      ```
   
  #### Variables
  1. All variables must start with lower case, must be in explainable full words. If someone reads the variable name, it should be easy to understand what the variable stores.
  2. All local variables are camel case. Examples:
      ```python
      jobListingsElement = None
      ```
      ```python
      localBufferTime = 5.5
      ```
  3. All global variables are snake case. Example:
      ```
      total_runs = 1
      ```
  4. Mentioning types are optional.
      ```python
      localBufferTime: float | int = 5.5
      ```
  
  #### Configuration variables
  1. All config variables are treated as global variables. They have some extra guidelines.
  2. Must have variable setting explanation, and examples of valid values. Examples:
      ```python
      # Explanation of what this setting will do, and instructions to enter it correctly
      config_variable = "value1"    #  <Valid values examples, and NOTES> "value1", "value2", etc. Don't forget quotes ("")
      ```
      ```python
      # Do you want to randomize the search order for search_terms?
      randomize_search_order = False     # True of False, Note: True or False are case-sensitive
      ```
      ```python
      # Avoid applying to jobs if their required experience is above your current_experience. (Set value as -1 if you want to apply to all ignoring their required experience...)
      current_experience = 5             # Integers > -2 (Ex: -1, 0, 1, 2, 3, 4...)
      ```
      ```python
      # Search location, this will be filled in "City, state, or zip code" search box. If left empty as "", tool will not fill it.
      search_location = "United States"               # Some valid examples: "", "United States", "India", "Chicago, Illinois, United States", "90001, Los Angeles, California, United States", "Bengaluru, Karnataka, India", etc.

      ```
  4. Add the config variable in appropriate `/config/file`.
  5. Every config variable must be validated. Go to `/modules/validator.py` and add it over there. Example:
      For config variable `search_location = ""` found in `/config/search.py`, string validation is added in file `/modules/validator.py` under the method `def validate_search()`.
      ```python
      def validate_search() -> None | ValueError | TypeError:
          '''
          Validates all variables in the `/config/search.py` file.
          '''
          check_string(search_location, "search_location")
      ```

  [back to index](#-content)
  
  ### Attestation
  1. All contributions require proper attestion. Format for attestation:
  ```python
  ##> ------ <Your full name> : <github id> OR <email> - <Type of change> ------
      print("My contributions 😍") # Your code
  ##<
  ```
  2. Examples for proper attestation:
  New feature example
  ```python
  ##> ------ Sai Vignesh Golla : godsscion - Feature ------
  def alert_box(title: str, message: str) -> None:
    '''
    Shows an alert box with the given `title` and `message`.
    '''
    from pyautogui import alert
    return alert(title, message)

  ##<
  ```
  
  Bug fix example
  ```python
  def alert_box(title: str, message: str) -> None:
    '''
    Shows an alert box with the given `title` and `message`.
    '''
    from pyautogui import alert

  ##> ------ Sai Vignesh Golla : saivigneshgolla@outlook.com - Bug fix ------
    return alert(message, title)
  ##<
  ```

[back to index](#-content)

## 🗓️ Major Updates History:
### Jul 20, 2024
- Contributions from community have been added
- Better AI support, minor bug fixes

### Nov 28, 2024
- Patched to work for latest changes in Linkedin.
- Users can now select to follow or not follow companies when submitting application.
- Frameworks for future AI Developments have been added.
- AI can now be used to extract skills from job description. 

### Oct 16, 2024
- Framework for OpenAI API and Local LLMs
- Framework for RAG

### Sep 09, 2024
- Smarter Auto-fill for salaries and notice periods
- Robust Search location filter, will work in window mode (No need for full screen)
- Better logic for Select and Radio type questions
- Proper functioning of Decline to answer questions in Equal Employment opportunity questions
- Checkbox questions select fail bug fixed
- Annotations are clearer in instructions for setup

### Sep 07, 2024
- Annotations for developers
- Robust input validations
- Restructured config file
- Fixed pagination bug

### Aug 21, 2024
- Performance improvements (skip clicking on applied jobs and blacklisted companies)
- Stop when easy apply application limit is reached
- Added ability to discard from pause at submission dialogue box
- Added support for address input
- Bug fixed radio questions, added support for physical disability questions
- Added framework for future config file updates

### June 19, 2024
- Major Bug fixes (Text Area type questions)
- Made uploading default resume as not required

### May 15, 2024
- Added functionality for textarea type questions `summary`, `cover_letter`(Summary, Cover letter); checkbox type questions (acknowledgements)
- Added feature to skip irrelevant jobs based on `bad_words` 
- Improved performance for answering questions
- Logic change for masters students skipping
- Change variable names `blacklist_exceptions` -> `about_company_good_words` and `blacklist_words` -> `about_company_bad_words`
- Added session summary for logs
- Added option to turn off "Pause before Submit" until next run

### May 05, 2024
- For questions similar to "What is your current location?", City posted in Job description will be posted as the answer if `current_city` is left empty in the configuration
- Added option to over write previously saved answers for a question `overwrite_previous_answers`
- Tool will now save previous answer of a question
- Tool will now collect all available options for a Radio type or Select type question
- Major update in answering logic for Easy Apply Application questions
- Added Safe mode option for quick stable launches `safe_mode`

### May 04, 2024
- Added option to fill in "City, state, or zip code" search box `search_location`
- Bug fixes in answering City or location question


[back to index](#-content)

<br>

## 📜 Disclaimer

**This program is for educational purposes only. By downloading, using, copying, replicating, or interacting with this program or its code, you acknowledge and agree to abide by all the Terms, Conditions, Policies, and Licenses mentioned, which are subject to modification without prior notice. The responsibility of staying informed of any changes or updates bears upon yourself. For the latest Terms & Conditions, Licenses, or Policies, please refer to [Auto Job Applier](https://github.com/GodsScion/Auto_job_applier_linkedIn). Additionally, kindly adhere to and comply with LinkedIn's terms of service and policies pertaining to web scraping. Usage is at your own risk. The creators and contributors of this program emphasize that they bear no responsibility or liability for any misuse, damages, or legal consequences resulting from its usage.**


## 🏛️ Terms and Conditions

Please consider the following:

- **LinkedIn Policies**: LinkedIn has specific policies regarding web scraping and data collection. The responsibility to review and comply with these policies before engaging, interacting, or undertaking any actions with this program bears upon yourself. Be aware of the limitations and restrictions imposed by LinkedIn to avoid any potential violation(s).

- **No Warranties or Guarantees**: This program is provided as-is, without any warranties or guarantees of any kind. The accuracy, reliability, and effectiveness of the program cannot be guaranteed. Use it at your own risk.

- **Disclaimer of Liability**: The creators and contributors of this program shall not be held responsible or liable for any damages or consequences arising from the direct or indirect use, interaction, or actions performed with this program. This includes but is not limited to any legal issues, loss of data, or other damages incurred.

- **Use at Your Own Risk**: It is important to exercise caution and ensure that your usage, interactions, and actions with this program comply with the applicable laws and regulations. Understand the potential risks and consequences associated with web scraping and data collection activities.

- **Chrome Driver**: This program utilizes the Chrome Driver for web scraping. Please review and comply with the terms and conditions specified for [Chrome Driver](https://chromedriver.chromium.org/home).


## ⚖️ License

**Original Work:**  
Copyright (C) 2024 Sai Vignesh Golla  <saivigneshgolla@outlook.com>

**Modifications:**  
Copyright (C) 2025 Divyansh (captflag)  
- Implemented grouped search terms and dynamic time filter
- Enhanced error handling and recruiter logging  
- Combined search functionality improvements

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

See [AGPLv3 LICENSE](LICENSE) for more info.


<br>

[back to index](#-content)

<br>

## 📬 Contact & Support

For questions, issues, or feature requests, please:
- Open an issue on [GitHub](https://github.com/captflag/Auto_Job_Applier_LinkedIn/issues)
- Check existing issues before creating a new one

---

#### ℹ️ Version: Enhanced Edition v1.0 (2025)
**Based on**: Community Alpha 25.07.20.9.30

---

[⬆ back to the top](#linkedin-auto-job-applier---enhanced-edition-)
