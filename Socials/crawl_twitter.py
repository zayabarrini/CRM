import tweepy
import re

# Twitter API Keys
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_SECRET = "YOUR_ACCESS_SECRET"

# Authenticate Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Find emails in bios
def find_emails(usernames):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = {}
    
    for username in usernames:
        user = api.get_user(screen_name=username)
        bio = user.description
        found_emails = re.findall(email_pattern, bio)
        if found_emails:
            emails[username] = found_emails

    return emails

# Example Usage
usernames = ["psychoanalysisX", "cinema_director"]
emails = find_emails(usernames)
print("✅ Extracted Emails:", emails)
