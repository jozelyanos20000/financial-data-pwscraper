# settings.py

BOT_NAME = "pwscrape"
SPIDER_MODULES = ["pwscrape.spiders"]
NEWSPIDER_MODULE = "pwscrape.spiders"

# Download Handlers for Playwright
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Set timeouts and concurrency
DOWNLOAD_TIMEOUT = 90  # 1.5 minutes
CONCURRENT_REQUESTS = 12
CONCURRENT_REQUESTS_PER_DOMAIN = 4
REDIRECT_MAX_TIMES = 10
COOKIES_ENABLED = False

# Playwright settings
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 360000  # 6 minutes
PLAYWRIGHT_ABORT_TIMEOUT = 900000  # Abort after 5 minutes if hanging

# Delay between requests and retry strategy
DOWNLOAD_DELAY = 4
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]

# AutoThrottle to manage server-side delays
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 3  # Start with a 3-second delay
AUTOTHROTTLE_MAX_DELAY = 60   # Maximum delay of 1 minute
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# User-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'

# Log and output settings
FEED_EXPORT_ENCODING = "utf-8"
LOG_FILE = 'txt_logs/nlt_scrapy_log.txt'
