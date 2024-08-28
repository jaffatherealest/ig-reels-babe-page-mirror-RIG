import os
from dotenv import load_dotenv

# load env vars
load_dotenv()

# google vars
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
# Define the path to the service account JSON file
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(__file__), 'ig-theme-scraper-5bf0a0910b46.json')
# Set the environment variable for Google Application Credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_PATH

# airtable vars
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY") 
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_REELS_TABLE = os.getenv("AIRTABLE_REELS_TABLE")
AIRTABLE_REELS_BABE_PAGE_TEMPLATE_VIEW = os.getenv("AIRTABLE_REELS_BABE_PAGE_TEMPLATE_VIEW")
AIRTABLE_BASE_ID_2 = os.getenv("AIRTABLE_BASE_ID_2")
AIRTABLE_CAPTIONS_TABLE = os.getenv("AIRTABLE_CAPTIONS_TABLE")
AIRTABLE_ACTIVE_CAPTIONS_VIEW = os.getenv("AIRTABLE_ACTIVE_CAPTIONS_VIEW")
bp_source_scraper_base_id = os.getenv("bp_source_scraper_base_id")
videos_table = os.getenv("videos_table")
tiktok_videos_view = os.getenv("tiktok_videos_view")

# creatomate vars
CREATOMATE_API_KEY = os.getenv("CREATOMATE_API_KEY")

# slack vars
SLACK_ALERT_WEBHOOK = os.getenv("SLACK_ALERT_WEBHOOK")
