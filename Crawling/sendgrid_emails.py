import pandas as pd
import sendgrid
from sendgrid.helpers.mail import Mail

# Load CSV
df = pd.read_csv("emails.csv")  # Update with your CSV filename

# SendGrid Configuration
SENDGRID_API_KEY = "YOUR_SENDGRID_API_KEY"
sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

# Email Templates (Customize as needed)
TEMPLATES = {
    "English": "Hello {name},\n\nThis is a personalized email in English.",
    "Spanish": "Hola {name},\n\nEste es un correo personalizado en español.",
    "French": "Bonjour {name},\n\nCeci est un email personnalisé en français."
}

# Sending Emails
for _, row in df.iterrows():
    name, email, language = row["name"], row["email"], row["language"]
    message_text = TEMPLATES.get(language, TEMPLATES["English"]).format(name=name)

    message = Mail(
        from_email="your-email@example.com",
        to_emails=email,
        subject="Custom Email for You",
        plain_text_content=message_text
    )

    response = sg.send(message)
    print(f"Email sent to {name} ({email}) in {language} - Status: {response.status_code}")

print("All emails sent successfully!")
