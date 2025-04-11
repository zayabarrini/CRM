import re
import csv

# Function to extract emails and corresponding names from a Markdown file
def extract_emails_and_names(md_file):
    with open(md_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    email_name_pairs = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if "@" in line and re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", line):
            email = line
            name = lines[i + 1].strip() if i + 1 < len(lines) else "Unknown"
            email_name_pairs.append((name, email))
    
    return email_name_pairs

# Function to save extracted data to a CSV file
def save_to_csv(data, csv_filename):
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email"])
        writer.writerows(data)

# Example usage
md_filename = "/home/zaya/Downloads/contacts.md"  # Change this to your actual Markdown file
csv_filename = "contacts.csv"
results = extract_emails_and_names(md_filename)

# Save results to CSV
save_to_csv(results, csv_filename)

# Print results
for name, email in results:
    print(f"Name: {name}, Email: {email}")

