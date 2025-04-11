#!/usr/bin/env python3
import sys
import yaml
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Configure paths
template_path = Path("/home/zaya/Downloads/Zayas/zayasCRM/Documentation/Emails/Psychoanalysis.yaml")
CSS_PATH = Path("/home/zaya/Downloads/Zayas/zayasCRM/Documentation/Emails/styles.css")

# Configure logging
logging.basicConfig(
    filename='email_sender.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EmailSender:
    def __init__(self):
        load_dotenv()
        self.templates = self.load_templates()
        self.css_content = self._load_css()  # Load CSS during initialization
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('EMAIL_SENDER')
        self.sender_password = os.getenv('EMAIL_PASSWORD')

    def _load_css(self):
        """Load CSS content from file"""
        try:
            with open(CSS_PATH, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Failed to load CSS: {str(e)}")
            return ""  # Fallback to no styling

    def load_templates(self, template_path=template_path):
        """Load email templates from YAML file"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                templates = yaml.safe_load(f)
            
            if not all(k in templates for k in ['metadata', 'content']):
                raise ValueError("Invalid YAML structure")
            
            if 'en' not in templates['content']:
                raise ValueError("English template (en) is required")
            
            return templates
        except Exception as e:
            logging.error(f"Error loading templates: {str(e)}")
            raise

    def build_email_body(self, lang_content, recipient_name):
        """Construct complete HTML email with CSS"""
        try:
            # Build the main content sections
            sections_html = self._build_content_sections(lang_content, recipient_name)
            
            # Combine with CSS and HTML structure
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    {self.css_content}
                </style>
            </head>
            <body>
                <header>
                    <h1>{lang_content['title']}</h1>
                </header>
                {sections_html}
            </body>
            </html>
            """
            return html
        except Exception as e:
            logging.error(f"Error building email body: {str(e)}")
            raise

    def _build_content_sections(self, lang_content, recipient_name):
        """Build all content sections"""
        sections = []
        
        # Add greeting
        sections.append(f'<p>Dear {recipient_name},</p>')
        
        # Add each section
        for section in lang_content.get('sections', []):
            section_html = []
            if section.get('title'):
                section_html.append(f'<h2>{section["title"]}</h2>')
            if section.get('body'):
                section_html.append(f'<div>{section["body"]}</div>')
            sections.append('\n'.join(section_html))
        
        # Add links if present
        if lang_content.get('links'):
            sections.append('<h3>Links</h3><ul>')
            sections.extend(
                f'<li><a href="{link["href"]}">{link["text"]}</a></li>'
                for link in lang_content['links']
            )
            sections.append('</ul>')
        
        # Add footer
        sections.extend([
            '<p>Looking forward to your thoughts.</p>',
            '<p>Best regards,<br>Zaya Barrini</p>'
        ])
        
        return '\n'.join(sections)

    def send_emails(self, contacts_csv="contacts.csv"):
        """Send emails to all contacts"""
        try:
            contacts_df = pd.read_csv(contacts_csv)
            
            if not {'Name', 'Email', 'Language'}.issubset(contacts_df.columns):
                raise ValueError("CSV missing required columns")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                
                success_count = 0
                for _, row in contacts_df.iterrows():
                    try:
                        lang_code = row['Language'].lower()
                        lang_content = self.templates['content'].get(
                            lang_code,
                            self.templates['content']['en']
                        )
                        
                        msg = MIMEMultipart('alternative')
                        msg['From'] = self.sender_email
                        msg['To'] = row['Email']
                        msg['Subject'] = lang_content['title']
                        
                        html_body = self.build_email_body(lang_content, row['Name'])
                        msg.attach(MIMEText(html_body, 'html'))
                        
                        server.send_message(msg)
                        success_count += 1
                        logging.info(f"Sent to {row['Name']} ({row['Email']}) in {lang_code}")
                        
                    except Exception as e:
                        logging.error(f"Failed to send to {row['Name']}: {str(e)}")
                
                logging.info(f"Completed: {success_count}/{len(contacts_df)} emails sent")
                return success_count
                
        except Exception as e:
            logging.error(f"Fatal error: {str(e)}")
            raise

if __name__ == "__main__":
    sender = EmailSender()
    # print(sender.build_email_body(
    #     sender.templates['content']['zh-ch'],
    #     "Test Name"
    # ))
    try:
        result = sender.send_emails()
        sys.exit(0 if result else 1)
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        sys.exit(1)