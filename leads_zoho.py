import requests

# Zoho API Credentials
ZOHO_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ZOHO_URL = "https://www.zohoapis.com/crm/v2/Leads"

# Example Lead
lead = {
    "data": [
        {
            "Last_Name": "Doe",
            "First_Name": "John",
            "Email": "john.doe@example.com",
            "Company": "Example Corp",
            "Phone": "+1 123 456 7890",
            "Lead_Source": "LinkedIn"
        }
    ]
}

headers = {
    "Authorization": f"Zoho-oauthtoken {ZOHO_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Send data to Zoho CRM
response = requests.post(ZOHO_URL, json=lead, headers=headers)
print(response.json())
