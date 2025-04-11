import requests

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

# Fetch email from LinkedIn API
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
email_url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
profile_url = "https://api.linkedin.com/v2/me"

email_response = requests.get(email_url, headers=headers).json()
profile_response = requests.get(profile_url, headers=headers).json()

email = email_response.get("elements", [])[0]["handle~"]["emailAddress"]
name = profile_response.get("localizedFirstName") + " " + profile_response.get("localizedLastName")

print(f"✅ Found Email: {email} | Name: {name}")
