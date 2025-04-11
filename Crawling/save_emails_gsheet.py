import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import re

# Google Sheets setup
SHEET_NAME = "Email List"  # Change to your Google Sheet name
CREDENTIALS_FILE = "your-credentials.json"  # Downloaded from Google Cloud Console

# Authenticate with Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open(SHEET_NAME).sheet1

# Function to extract emails from a given URL
def extract_emails(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    emails = set(re.findall(email_pattern, soup.get_text()))
    return emails

# List of websites to scrape
urls = ["https://example.com", "https://another-site.com"]

# Save extracted emails to Google Sheets
for url in urls:
    emails = extract_emails(url)
    for email in emails:
        sheet.append_row([email, url])  # Append email & source URL

print("✅ Emails saved to Google Sheets successfully!")
