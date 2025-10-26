import requests
from bs4 import BeautifulSoup
import re
import csv
import signal
from contextlib import contextmanager
import datetime

# Timeout handler
class TimeoutException(Exception):
    pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)  # Disable the alarm

# Function to extract emails from a given URL
def extract_emails(url):
    try:
        response = requests.get(url, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Regular expression to find emails
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b(?!.*\.(png|webp|jpg|jpeg|gif|svg|ico)\b)'
        # email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = set(re.findall(email_pattern, soup.get_text()))
        
        return emails, "ok"  # Return emails and status
    except requests.exceptions.RequestException as e:
        return set(), str(e)  # Return empty set and error message

current_time = datetime.datetime.now()
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
# Read URLs from a CSV file
input_csv = "/home/zaya/Downloads/Barcelona.csv"  # Input CSV file with a header called "website"
output_csv = f"/home/zaya/Downloads/Barcelona-emails-b4s_{time_string}.csv"  # Output CSV file with timestamp

# Open CSV file in write mode
with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Updated header row including additional fields
    writer.writerow(["Name", "Email", "Source URL", "Status", "Industry", "Language", "Location"])

    with open(input_csv, mode="r", newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            url = row["Website"]
            # Preserve the additional data from input
            name = row.get("Name", "")
            industry = row.get("Industry", "")
            language = row.get("Language", "")
            location = row.get("Location", "")
            
            print(f"🔍 Scraping {url}...")
            try:
                with time_limit(420):  # 7 minutes timeout
                    emails, status = extract_emails(url)
                    if emails:
                        for email in emails:
                            writer.writerow([
                                name,
                                email, 
                                url, 
                                status,
                                industry,
                                language,
                                location
                            ])
                    else:
                        writer.writerow([
                            name,
                            "", 
                            url, 
                            status,
                            industry,
                            language,
                            location
                        ])
            except TimeoutException:
                status = "Timeout exceeded"
                writer.writerow([
                    name,
                    "", 
                    url, 
                    status,
                    industry,
                    language,
                    location
                ])
                print(f"⏰ {status} for {url}")
            except Exception as e:
                status = f"Error: {str(e)}"
                writer.writerow([
                    name,
                    "", 
                    url, 
                    status,
                    industry,
                    language,
                    location
                ])
                print(f"⚠️ {status} for {url}")

print(f"✅ Emails saved to {output_csv}")