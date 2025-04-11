import requests

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
PAGE_ID = "123456789"  # Replace with target Page ID

# Fetch Page Posts
url = f"https://graph.facebook.com/v12.0/{PAGE_ID}/feed?access_token={ACCESS_TOKEN}"
response = requests.get(url).json()

# Extract emails from posts
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = set()

for post in response.get("data", []):
    post_text = post.get("message", "")
    found_emails = re.findall(email_pattern, post_text)
    emails.update(found_emails)

print("✅ Extracted Emails:", emails)
