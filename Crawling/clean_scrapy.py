import pandas as pd
import re

# Define the regex pattern for valid emails (without look-behind)
email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

# List of invalid email extensions
invalid_extensions = ['.png', '.webp', '.jpg', '.jpeg', '.gif', '.svg', '.ico']

# Read the CSV file
df = pd.read_csv('/home/zaya/Downloads/scrapy.csv')  # Replace 'input.csv' with your file name

# Filter out invalid emails
df = df[df['Email'].apply(lambda x: bool(re.match(email_pattern, str(x))))]

# Further filter out emails that end with invalid extensions
df = df[~df['Email'].str.lower().str.endswith(tuple(invalid_extensions))]

# Filter by unique emails
df = df.drop_duplicates(subset='Email', keep='first')

# Remove websites with non-unique errors
# Assuming 'Status' column contains error messages
# df = df.drop_duplicates(subset=['Website', 'Status'], keep=False)

# Export the filtered data to a new CSV file
df.to_csv('/home/zaya/Downloads/filtered_scrapy.csv', index=False)  # Replace 'output.csv' with your desired output file name

print("Filtered data exported to 'output.csv'")