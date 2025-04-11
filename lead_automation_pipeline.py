import requests
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# API Keys & Credentials
HUBSPOT_API_KEY = "YOUR_HUBSPOT_API_KEY"
ZOHO_ACCESS_TOKEN = "YOUR_ZOHO_ACCESS_TOKEN"
GOOGLE_CREDS_FILE = 'path/to/your-google-credentials.json'
SOCIAL_MEDIA_API_KEYS = {
    "LinkedIn": "YOUR_LINKEDIN_API_KEY",
    "Twitter": "YOUR_TWITTER_API_KEY",
    "Facebook": "YOUR_FACEBOOK_API_KEY",
    "Instagram": "YOUR_INSTAGRAM_API_KEY"
}

# Google Sheets Setup
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'path/to/your-google-credentials.json'
SPREADSHEET_NAME = 'Lead Database'

def authenticate_google_sheets():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME).sheet1

# Save Leads to CSV
def save_to_csv(leads, filename="leads.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "Source"])
        writer.writerows(leads)

# Send Leads to HubSpot CRM
def send_to_hubspot(leads, hubspot_api_key):
    HUBSPOT_URL = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {hubspot_api_key}",
        "Content-Type": "application/json"
    }
    for lead in leads:
        data = {"properties": {"email": lead[1], "firstname": lead[0], "lead_source": lead[2]}}
        response = requests.post(HUBSPOT_URL, json=data, headers=headers)
        print(response.json())

# Send Leads to Zoho CRM
def send_to_zoho(leads, zoho_access_token):
    ZOHO_URL = "https://www.zohoapis.com/crm/v2/Leads"
    headers = {"Authorization": f"Zoho-oauthtoken {zoho_access_token}", "Content-Type": "application/json"}
    for lead in leads:
        data = {"data": [{"Last_Name": lead[0], "Email": lead[1], "Lead_Source": lead[2]}]}
        response = requests.post(ZOHO_URL, json=data, headers=headers)
        print(response.json())

# Save Leads to Google Sheets
def save_to_google_sheets(leads):
    sheet = authenticate_google_sheets()
    sheet.append_rows(leads)

# Example Usage
leads = [["John Doe", "john.doe@example.com", "LinkedIn"],
         ["Jane Smith", "jane.smith@example.com", "Twitter"]]

save_to_csv(leads)
save_to_google_sheets(leads)
send_to_hubspot(leads, "YOUR_HUBSPOT_API_KEY")
send_to_zoho(leads, "YOUR_ZOHO_ACCESS_TOKEN")
