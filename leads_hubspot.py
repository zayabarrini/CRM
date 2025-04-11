import requests

HUBSPOT_API_KEY = "YOUR_HUBSPOT_API_KEY"
HUBSPOT_URL = "https://api.hubapi.com/crm/v3/objects/contacts"

# Example Lead
lead = {
    "properties": {
        "email": "john.doe@example.com",
        "firstname": "John",
        "lastname": "Doe",
        "phone": "+1 123 456 7890",
        "company": "Example Corp",
        "lead_source": "LinkedIn"
    }
}

headers = {
    "Authorization": f"Bearer {HUBSPOT_API_KEY}",
    "Content-Type": "application/json"
}

# Send data to HubSpot
response = requests.post(HUBSPOT_URL, json=lead, headers=headers)
print(response.json())
