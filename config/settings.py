###################################################### CONFIGURE YOUR BOT HERE ######################################################

# >>>>>>>>>>> LinkedIn Settings <<<<<<<<<<<

# Keep the External Application tabs open?
close_tabs = False                  # True or False, Note: True or False are case-sensitive
'''
Note: RECOMMENDED TO LEAVE IT AS `True`, if you set it `False`, be sure to CLOSE ALL TABS BEFORE CLOSING THE BROWSER!!!
'''

# Follow easy applied companies
follow_companies = False            # True or False, Note: True or False are case-sensitive

## Upcoming features (In Development)
# Send connection requests to HR's 
connect_hr = True                  # True or False, Note: True or False are case-sensitive

# Message is automatically personalized with job title and company name
# Format: "Hello, my name is Divyansh Dewangan. I recently came across the [JOB_TITLE] opening at [COMPANY] and would be grateful for the opportunity to connect. If possible, I would sincerely appreciate your referral or guidance regarding the role. Thank you for your time and support."
connect_request_message = ""       # This field is no longer used - message is dynamically generated

# Do you want the program to run continuously until you stop it? (Beta)
run_non_stop = False                # True or False, Note: True or False are case-sensitive
'''
Note: Will be treated as False if `run_in_background = True`
'''
alternate_sortby = True             # True or False, Note: True or False are case-sensitive
cycle_date_posted = True            # True or False, Note: True or False are case-sensitive
stop_date_cycle_at_24hr = True      # True or False, Note: True or False are case-sensitive

# Minimum and Maximum run time in minutes
min_runtime_minutes = 20             # Integer > 0
max_runtime_minutes = 120            # Integer > min_runtime_minutes

# Session Management Settings
daily_application_limit = 50        # Maximum applications per day (LinkedIn limit is ~100-150)
applications_per_session = 10       # Maximum applications per session before break
break_between_applications = (30, 90)  # Random break range in seconds (min, max)

# Detection Avoidance Settings
simulate_reading_time = True        # Add delays to simulate reading job descriptions
reading_time_range = (5, 15)        # Reading time range in seconds (min, max)
simulate_mouse_movement = False     # Simulate random mouse movements (experimental)
human_like_typing = True            # Add delays between keystrokes

# Retry Logic Settings
retry_failed_actions = 3            # Number of retries for failed clicks/actions
retry_delay_base = 2                # Base delay in seconds for exponential backoff

# Session Recovery Settings
enable_session_recovery = True      # Save progress for recovery after crashes
checkpoint_interval = 5             # Save checkpoint every N applications

# Metrics & Monitoring Settings
enable_metrics_tracking = True      # Track success metrics and statistics
metrics_file_name = "all excels/bot_metrics.csv"  # File to store metrics

# AI Settings
ai_cache_enabled = True             # Cache AI responses to save API calls
ai_cache_duration_days = 7          # How long to keep cached responses

# Smart Filtering Settings
skip_high_applicant_jobs = True     # Skip jobs with too many applicants
max_applicants_threshold = 200      # Maximum applicants before skipping
skip_irrelevant_titles = True       # Skip jobs with irrelevant titles
relevant_title_keywords = []        # Keywords that must be in job title (empty = disabled)

# External Application Settings
enable_external_applications = True
max_external_apps_per_session = 5
external_app_timeout = 180  # 3 minutes
skip_captcha_sites = True
alert_on_captcha = True

# Supported Platforms
supported_ats_platforms = ['greenhouse']
use_universal_filler_fallback = True

# Knowledge Base
enable_field_learning = True
knowledge_base_file = "logs/field_knowledge_base.json"

# Link Collection
external_links_file = "all excels/external_application_links.csv"

# Connection Request Settings
enable_hr_connections = True
daily_connection_limit = 12  # Maximum connection requests per day
min_delay_between_connections = 120  # Minimum seconds between connection requests (2 minutes)

# Smart Filtering Settings
enable_smart_filtering = True
skip_viewed_jobs = True  # Skip jobs that were viewed but not applied to
skip_rejected_companies = True  # Skip companies that rejected applications
company_rejection_threshold = 2  # Skip company after this many rejections
prioritize_low_applicant_jobs = True  # Prioritize jobs with fewer applicants
max_applicants_for_priority = 50  # Jobs with fewer applicants get priority

# Dynamic Time Filter Settings
enable_dynamic_time_filter = True  # Keep strict r600 filter (10 minutes)
initial_time_filter = "r600"  # Start with 10 minutes
fallback_filters = ["r3600", "r86400"]  # Fallback to 1 hour, then 24 hours
min_jobs_threshold = 5  # Expand filter if fewer than this many jobs

# Analytics Settings
enable_analytics = True
analytics_file = "logs/success_metrics.json"
generate_weekly_reports = True





# >>>>>>>>>>> RESUME GENERATOR (Experimental & In Development) <<<<<<<<<<<

# Give the path to the folder where all the generated resumes are to be stored
generated_resume_path = "all resumes/" # (In Development)





# >>>>>>>>>>> Global Settings <<<<<<<<<<<

# Directory and name of the files where history of applied jobs is saved (Sentence after the last "/" will be considered as the file name).
file_name = "all excels/all_applied_applications_history.csv"
failed_file_name = "all excels/all_failed_applications_history.csv"
logs_folder_path = "logs/"

# Set the maximum amount of time allowed to wait between each click in secs
click_gap = 1                       # Enter max allowed secs to wait approximately. (Only Non Negative Integers Eg: 0,1,2,3,....)

# If you want to see Chrome running then set run_in_background as False (May reduce performance). 
run_in_background = False           # True or False, Note: True or False are case-sensitive ,   If True, this will make pause_at_failed_question, pause_before_submit and run_in_background as False

# If you want to disable extensions then set disable_extensions as True (Better for performance)
disable_extensions = False          # True or False, Note: True or False are case-sensitive

# Run in safe mode. Set this true if chrome is taking too long to open or if you have multiple profiles in browser. This will open chrome in guest profile!
safe_mode = True                   # True or False, Note: True or False are case-sensitive

# Do you want scrolling to be smooth or instantaneous? (Can reduce performance if True)
smooth_scroll = False               # True or False, Note: True or False are case-sensitive

# If enabled (True), the program would keep your screen active and prevent PC from sleeping. Instead you could disable this feature (set it to false) and adjust your PC sleep settings to Never Sleep or a preferred time. 
keep_screen_awake = True            # True or False, Note: True or False are case-sensitive (Note: Will temporarily deactivate when any application dialog boxes are present (Eg: Pause before submit, Help needed for a question..))

# Run in undetected mode to bypass anti-bot protections (Preview Feature, UNSTABLE. Recommended to leave it as False)
stealth_mode = False               # True or False, Note: True or False are case-sensitive

# Do you want to get alerts on errors related to AI API connection?
showAiErrorAlerts = False            # True or False, Note: True or False are case-sensitive

# Use ChatGPT for resume building (Experimental Feature can break the application. Recommended to leave it as False) 
# use_resume_generator = False       # True or False, Note: True or False are case-sensitive ,   This feature may only work with 'stealth_mode = True'. As ChatGPT website is hosted by CloudFlare which is protected by Anti-bot protections!











############################################################################################################
'''
THANK YOU for using my tool 😊! Wishing you the best in your job hunt 🙌🏻!

Sharing is caring! If you found this tool helpful, please share it with your peers 🥺. Your support keeps this project alive.

Support my work on <PATREON_LINK>. Together, we can help more job seekers.

As an independent developer, I pour my heart and soul into creating tools like this, driven by the genuine desire to make a positive impact.

Your support, whether through donations big or small or simply spreading the word, means the world to me and helps keep this project alive and thriving.

Gratefully yours 🙏🏻,
Sai Vignesh Golla
'''
############################################################################################################
