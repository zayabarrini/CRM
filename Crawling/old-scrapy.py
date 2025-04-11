import scrapy
import re
import csv
import signal
from urllib.parse import urlparse
from scrapy.http import Request
from contextlib import contextmanager

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

class EmailSpider(scrapy.Spider):
    name = "email_spider"
    custom_settings = {
        "FEEDS": {
            "/home/zaya/Downloads/emails.csv": {
                "format": "csv",
                "fields": ["Email", "Source URL", "Status"],
                "overwrite": True,  # Overwrite the file on each run
            }
        },
        "LOG_LEVEL": "ERROR",  # Suppress most logs, only show errors
        "RETRY_TIMES": 1,  # Reduce retries for failed requests
        "CONCURRENT_REQUESTS": 16,  # Increase concurrent requests
        "DOWNLOAD_TIMEOUT": 30,  # Set a timeout for each request (in seconds)
        "DNS_TIMEOUT": 10,  # Set a timeout for DNS resolution (in seconds)
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_emails = set()  # Track unique emails globally
        self.email_counters = {}  # Track email counts per website
        self.seen_errors = {}  # Track unique errors per website

    def start_requests(self):
        # Read URLs from a CSV file
        with open("/home/zaya/Downloads/websites.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row["website"]
                if not self.is_valid_url(url):  # Skip invalid URLs
                    self.logger.warning(f"⚠️ Skipping invalid URL: {url}")
                    continue
                self.email_counters[url] = 0  # Initialize email counter for this website
                self.seen_errors[url] = set()  # Initialize error tracker for this website
                yield Request(url, callback=self.parse, meta={"source_url": url}, errback=self.handle_error)

    def is_valid_url(self, url):
        """Check if a URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])  # Ensure scheme and netloc are present
        except ValueError:
            return False

    def parse(self, response):
        source_url = response.meta["source_url"]
        try:
            # Check if the response content is text-based
            content_type = response.headers.get("Content-Type", b"").decode("utf-8").lower()
            if not content_type.startswith("text/"):
                error_message = f"Non-text content type: {content_type}"
                if error_message not in self.seen_errors[source_url]:
                    self.seen_errors[source_url].add(error_message)  # Track this error
                    yield {
                        "Email": "",
                        "Source URL": source_url,
                        "Status": error_message,
                    }
                return  # Skip non-text responses

            # Set a timeout of 7 minutes (420 seconds) for each URL
            with time_limit(420):
                # Extract all text
                text = response.text
                # Regular expression to find emails (improved)
                email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b(?!.*\.(png|webp|jpg|jpeg|gif|svg|ico)\b)'
                emails = set(re.findall(email_pattern, text))
                
                # Save only new unique emails, up to 20 per website
                for email in emails:
                    if self.email_counters[source_url] >= 20:
                        break  # Stop saving emails for this website
                    if email not in self.seen_emails:
                        self.seen_emails.add(email)  # Add to seen emails
                        self.email_counters[source_url] += 1  # Increment counter
                        yield {
                            "Email": email,
                            "Source URL": source_url,
                            "Status": "ok",
                        }

                # Follow links and continue scraping (if email count is less than 20)
                if self.email_counters[source_url] < 20:
                    for link in response.css("a::attr(href)").getall():
                        if link.startswith("http"):  # Only follow valid links
                            yield response.follow(link, self.parse, meta={"source_url": source_url}, errback=self.handle_error)
        except TimeoutException:
            error_message = "Timeout exceeded"
            if error_message not in self.seen_errors[source_url]:
                self.seen_errors[source_url].add(error_message)  # Track this error
                yield {
                    "Email": "",
                    "Source URL": source_url,
                    "Status": error_message,
                }
            self.logger.warning(f"⏰ Timeout exceeded for {source_url}")
        except Exception as e:
            error_message = f"Error: {str(e)}"
            if error_message not in self.seen_errors[source_url]:
                self.seen_errors[source_url].add(error_message)  # Track this error
                yield {
                    "Email": "",
                    "Source URL": source_url,
                    "Status": error_message,
                }
            self.logger.error(f"⚠️ Error for {source_url}: {e}")

    def handle_error(self, failure):
        """Handle request errors (e.g., DNS failures, connection errors)."""
        request = failure.request
        source_url = request.meta.get("source_url", request.url)
        error_message = str(failure.value)

        if "DNSLookupError" in error_message:
            error_message = "DNS lookup failed"
        elif "500" in error_message:
            error_message = "500 Internal Server Error"

        if error_message not in self.seen_errors[source_url]:
            self.seen_errors[source_url].add(error_message)  # Track this error
            yield {
                "Email": "",
                "Source URL": source_url,
                "Status": error_message,
            }
        self.logger.warning(f"⚠️ Error for {source_url}: {error_message}")