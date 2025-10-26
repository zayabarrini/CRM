import scrapy
import re
import csv
import signal
import time
from urllib.parse import urlparse
from scrapy.http import Request
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

class EmailSpider(scrapy.Spider):
    name = "email_spider"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generate timestamp for output file
        current_time = datetime.datetime.now()
        time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        self.output_file = f"/home/zaya/Downloads/Crawl_emails_{time_string}.csv"
        
        self.custom_settings = {
            "FEEDS": {
                self.output_file: {
                    "format": "csv",
                    "fields": ["Name", "Email", "Source URL", "Status", "Industry", "Language", "Location"],
                    "overwrite": True,
                }
            },
            "LOG_LEVEL": "ERROR",
            "RETRY_TIMES": 1,
            "CONCURRENT_REQUESTS": 16,
            "DOWNLOAD_TIMEOUT": 30,
            "DNS_TIMEOUT": 10,
            "CLOSESPIDER_TIMEOUT": 7200/20,  # 2 hours in seconds
        }

        self.seen_emails = set()
        self.email_counters = {}
        self.seen_errors = {}
        self.start_time = time.time()
        self.max_runtime = 7200  # 2 hours in seconds
        self.url_metadata = {}  # Store additional metadata for each URL

        self.commercial_keywords = [
            "amazon", "shopify", "imdb", "login", "signup", "oauth", 
            "accounts", "pro", "redirect", "callback"
        ]

    def start_requests(self):
        try:
            with time_limit(10):  # Timeout for reading the input file
                with open("/home/zaya/Downloads/Barcelona.csv", newline="", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if time.time() - self.start_time > self.max_runtime:
                            raise scrapy.exceptions.CloseSpider("Maximum runtime reached before starting requests")
                            
                        url = row["website"]
                        if not self.is_valid_url(url):
                            continue
                        if self.is_commercial(url):
                            continue
                            
                        # Store metadata for this URL
                        self.url_metadata[url] = {
                            'name': row.get('Name', ''),
                            'industry': row.get('Industry', ''),
                            'language': row.get('Language', ''),
                            'location': row.get('Location', '')
                        }
                        
                        self.email_counters[url] = 0
                        self.seen_errors[url] = set()
                        yield Request(
                            url, 
                            callback=self.parse, 
                            meta={
                                "source_url": url,
                                "download_timeout": 30
                            }, 
                            errback=self.handle_error
                        )
        except TimeoutException:
            self.logger.error("Timeout while reading input file")
            raise scrapy.exceptions.CloseSpider("Timeout reading input file")
        except Exception as e:
            self.logger.error(f"Error reading input file: {str(e)}")
            raise scrapy.exceptions.CloseSpider(f"Input file error: {str(e)}")

    def parse(self, response):
        if time.time() - self.start_time > self.max_runtime:
            self.logger.info("🕒 Maximum runtime (2 hours) reached. Stopping spider.")
            raise scrapy.exceptions.CloseSpider("Maximum runtime reached")

        source_url = response.meta["source_url"]
        metadata = self.url_metadata.get(source_url, {})
        
        try:
            with time_limit(25):
                content_type = response.headers.get("Content-Type", b"").decode("utf-8").lower()
                if not content_type.startswith("text/"):
                    error_message = f"Non-text content type: {content_type}"
                    if error_message not in self.seen_errors[source_url]:
                        self.seen_errors[source_url].add(error_message)
                        yield {
                            "Name": metadata.get('name', ''),
                            "Email": "",
                            "Source URL": source_url,
                            "Status": error_message,
                            "Industry": metadata.get('industry', ''),
                            "Language": metadata.get('language', ''),
                            "Location": metadata.get('location', '')
                        }
                    return

                text = response.text
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = set(re.findall(email_pattern, text))
                
                for email in emails:
                    if self.email_counters[source_url] >= 20:
                        break
                    if email not in self.seen_emails:
                        self.seen_emails.add(email)
                        self.email_counters[source_url] += 1
                        yield {
                            "Name": metadata.get('name', ''),
                            "Email": email,
                            "Source URL": source_url,
                            "Status": "ok",
                            "Industry": metadata.get('industry', ''),
                            "Language": metadata.get('language', ''),
                            "Location": metadata.get('location', '')
                        }

                if self.email_counters[source_url] < 20:
                    for link in response.css("a::attr(href)").getall():
                        if time.time() - self.start_time > self.max_runtime:
                            raise scrapy.exceptions.CloseSpider("Maximum runtime reached during parsing")
                        if link.startswith("http"):
                            yield response.follow(
                                link, 
                                self.parse, 
                                meta={
                                    "source_url": source_url,
                                    "download_timeout": 30
                                }, 
                                errback=self.handle_error
                            )
        except TimeoutException:
            error_message = "Parsing timeout exceeded"
            if error_message not in self.seen_errors[source_url]:
                self.seen_errors[source_url].add(error_message)
                yield {
                    "Name": metadata.get('name', ''),
                    "Email": "",
                    "Source URL": source_url,
                    "Status": error_message,
                    "Industry": metadata.get('industry', ''),
                    "Language": metadata.get('language', ''),
                    "Location": metadata.get('location', '')
                }
        except Exception as e:
            error_message = f"Error: {str(e)}"
            if error_message not in self.seen_errors[source_url]:
                self.seen_errors[source_url].add(error_message)
                yield {
                    "Name": metadata.get('name', ''),
                    "Email": "",
                    "Source URL": source_url,
                    "Status": error_message,
                    "Industry": metadata.get('industry', ''),
                    "Language": metadata.get('language', ''),
                    "Location": metadata.get('location', '')
                }

    def handle_error(self, failure):
        """Handle request errors while preserving metadata."""
        request = failure.request
        source_url = request.meta.get("source_url", request.url)
        metadata = self.url_metadata.get(source_url, {})
        error_message = str(failure.value)

        if "DNSLookupError" in error_message:
            error_message = "DNS lookup failed"
        elif "500" in error_message:
            error_message = "500 Internal Server Error"

        if error_message not in self.seen_errors[source_url]:
            self.seen_errors[source_url].add(error_message)
            yield {
                "Name": metadata.get('name', ''),
                "Email": "",
                "Source URL": source_url,
                "Status": error_message,
                "Industry": metadata.get('industry', ''),
                "Language": metadata.get('language', ''),
                "Location": metadata.get('location', '')
            }
        
    def is_valid_url(self, url):
        """Check if a URL is valid and properly formatted.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(url, str) or not url.strip():
            return False
        
        try:
            result = urlparse(url)
            
            # Basic validation checks
            if not all([result.scheme, result.netloc]):
                return False
                
            # Scheme should be http or https
            if result.scheme not in ('http', 'https'):
                return False
                
            # Netloc should contain a dot (.)
            if '.' not in result.netloc:
                return False
                
            # Basic TLD validation (at least 2 chars)
            if len(result.netloc.split('.')[-1]) < 2:
                return False
                
            # Check for common invalid patterns
            if ' ' in url or '..' in url or '//' in url[8:]:
                return False
                
            return True
            
        except (ValueError, AttributeError):
            return False

    def is_commercial(self, url):
        """Check if a URL appears to be commercial or should be skipped.
        
        Args:
            url (str): The URL to check
            
        Returns:
            bool: True if commercial (should skip), False otherwise
        """
        if not isinstance(url, str):
            return False
            
        lower_url = url.lower()
        
        # Skip common commercial domains
        commercial_domains = {
            'amazon.', 'shopify.', 'ebay.', 'walmart.', 'alibaba.',
            'etsy.', 'booking.', 'tripadvisor.', 'expedia.', 'paypal.'
        }
        
        if any(domain in lower_url for domain in commercial_domains):
            return True
            
        # Skip paths with commercial keywords
        commercial_paths = {
            '/shop', '/product', '/cart', '/checkout',
            '/pricing', '/subscribe', '/buy', '/store'
        }
        
        parsed = urlparse(url)
        if any(path in parsed.path.lower() for path in commercial_paths):
            return True
            
        # Skip URLs with commercial query parameters
        commercial_params = {
            'utm_', 'ref=', 'affiliate=', 'campaign=',
            'promo=', 'discount=', 'coupon='
        }
        
        if any(param in parsed.query.lower() for param in commercial_params):
            return True
            
        # Skip based on domain patterns
        domain_parts = parsed.netloc.split('.')
        if len(domain_parts) > 2 and domain_parts[-2] in {'com', 'net', 'shop'}:
            return True
            
        return False