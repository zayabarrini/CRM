import instaloader
import re

L = instaloader.Instaloader()

# Get Instagram profile
profile = instaloader.Profile.from_username(L.context, "cinema_director")

# Extract email from bio
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = re.findall(email_pattern, profile.biography)

print("✅ Extracted Emails:", emails)
