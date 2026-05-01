import sys
import scrapy
import csv
import importlib
import fitz
from os.path import dirname, abspath
import unicodedata
sys.path.append(abspath(dirname(__file__)))
from pwscrape.cookie_handler import get_cookiebot_handling_methods

# XPath character-map constants used for case/accent-insensitive link matching
_XPATH_FROM = 'ABCDEFGHIJKLMNOPQRSTUVWXYZéÉöÖåÅäÄ'
_XPATH_TO   = 'abcdefghijklmnopqrstuvwxyzeeooaaaa'


class CompanySpider(scrapy.Spider):
    name = 'company_spider'

    def start_requests(self):
        company_data = self.read_company_data('100_de.csv')
        self.log(f"Total companies loaded from CSV: {len(company_data)}")
        for company in company_data:
            isin = company['ISIN']
            base_url = company['Company URL']
            self.log(f"Processing {base_url} - ISIN: {isin}")
            yield scrapy.Request(
                base_url,
                meta={
                    "playwright": True,
                    "playwright_timeout": 900000,
                    "playwright_page_methods": get_cookiebot_handling_methods(),
                    "navigated_from_investor": False,
                    "isin": isin,
                    "base_url": base_url,
                    "country_code": isin[:2].lower()
                },
                callback=self.navigate_to_reports,
                errback=self.handle_error
            )

    def read_company_data(self, csv_file):
        company_data = []
        with open(csv_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                url = row['Company URL'].strip()
                isin = row['ISIN'].strip()
                if not url or url.lower() == "no url found":
                    self.log(f"Skipping entry with missing or invalid URL: {row}")
                    continue
                if isin:
                    company_data.append({'Company URL': url, 'ISIN': isin})
        return company_data

    def load_keywords(self, country_code):
        try:
            module = importlib.import_module(f'keywords.{country_code}_keywords')
            investor_keywords = getattr(module, 'INVESTOR_KEYWORDS', [])
            reports_keywords  = getattr(module, 'REPORTS_KEYWORDS', [])
            interim_keywords  = getattr(module, 'INTERIM_KEYWORDS', [])
            annual_keywords   = getattr(module, 'ANNUAL_KEYWORDS', [])
            self.log(f"Loaded keywords for country code: {country_code.upper()}")
            return investor_keywords, reports_keywords, interim_keywords, annual_keywords
        except (ModuleNotFoundError, AttributeError):
            self.log(f"Keywords for {country_code.upper()} not found. Using default empty lists.")
            return [], [], [], []

    def handle_error(self, failure):
        self.log(f"Request failed: {failure.request.url} - {failure.value}")
        yield {
            "ISIN": failure.request.meta.get("isin", "Unknown"),
            "Website URL": failure.request.url,
            "Reports/Investors URL": "Error: Skipped due to connection or other failure",
            "Interim Reports": [],
            "Annual Reports": []
        }

    def _keyword_xpath(self, keyword):
        """Returns an XPath that matches <a> tags containing keyword in text, href, span, or small — case/accent insensitive."""
        f, t = _XPATH_FROM, _XPATH_TO
        return f"""
            //a[contains(translate(text(), '{f}', '{t}'), '{keyword}')
            or contains(translate(@href, '{f}', '{t}'), '{keyword}')
            or descendant::span[contains(translate(text(), '{f}', '{t}'), '{keyword}')]
            or descendant::small[contains(translate(text(), '{f}', '{t}'), '{keyword}')]
            ]/@href
        """

    def navigate_to_reports(self, response):
        country_code = response.meta.get("country_code", "gb")
        _, reports_keywords, _, _ = self.load_keywords(country_code)
        isin = response.meta['isin']
        base_url = response.meta['base_url']

        reports_link = None
        found_keyword = None
        for keyword in reports_keywords:
            reports_link = response.xpath(self._keyword_xpath(keyword)).get()
            if reports_link:
                found_keyword = keyword
                break

        if reports_link:
            reports_url = response.urljoin(reports_link)
            self.log(f"Found reports section: {reports_url} for {base_url} using keyword: '{found_keyword}'")
            yield scrapy.Request(
                reports_url,
                callback=self.retrieve_pdfs,
                meta={
                    "isin": isin,
                    "base_url": base_url,
                    "reports_url": reports_url,
                    "country_code": country_code
                },
                dont_filter=True
            )
        elif not response.meta.get("navigated_from_investor"):
            self.log(f"No reports section found on {base_url}. Trying to find investor section.")
            yield from self.navigate_to_investors(response)
        else:
            investor_url = response.meta.get("investor_url", "Investor or Reports section not found")
            self.log(f"No reports found on {base_url} even after visiting investor section.")
            yield {
                "ISIN": isin,
                "Website URL": base_url,
                "Reports/Investors URL": investor_url,
                "Interim Reports": [],
                "Annual Reports": []
            }

    def navigate_to_investors(self, response):
        country_code = response.meta.get("country_code", "gb")
        investor_keywords, _, _, _ = self.load_keywords(country_code)

        investor_link = None
        found_keyword = None
        for keyword in investor_keywords:
            investor_link = response.xpath(self._keyword_xpath(keyword)).get()
            if investor_link:
                found_keyword = keyword
                break

        if investor_link:
            investor_url = response.urljoin(investor_link)
            self.log(f"Found investor section: {investor_url} for {response.url} using keyword: '{found_keyword}'")
            yield scrapy.Request(
                investor_url,
                callback=self.navigate_to_reports,
                meta={
                    "isin": response.meta['isin'],
                    "base_url": response.meta['base_url'],
                    "investor_url": investor_url,
                    "navigated_from_investor": True,
                    "country_code": country_code
                }
            )
        else:
            self.log(f"No investor section found on {response.url}")
            yield {
                "ISIN": response.meta['isin'],
                "Website URL": response.meta['base_url'],
                "Reports/Investors URL": "Investor or Reports section not found",
                "Interim Reports": [],
                "Annual Reports": []
            }

    def retrieve_pdfs(self, response):
        isin = response.meta['isin']
        base_url = response.meta['base_url']
        reports_url = response.meta['reports_url']
        country_code = response.meta.get("country_code", "gb")

        pdf_links = response.xpath("//a[contains(@href, '.pdf') or @class='col d-flex']/@href").getall()
        pdf_links = [response.urljoin(link) for link in pdf_links]
        self.log(f"Found {len(pdf_links)} PDF files in reports section for {base_url}")

        _, _, interim_keywords, annual_keywords = self.load_keywords(country_code)

        if not pdf_links:
            yield {
                "ISIN": isin,
                "Website URL": base_url,
                "Reports/Investors URL": reports_url,
                "Interim Reports": [],
                "Annual Reports": []
            }
            return

        yield scrapy.Request(
            pdf_links[0],
            callback=self.process_pdf,
            meta={
                "isin": isin,
                "base_url": base_url,
                "reports_url": reports_url,
                "country_code": country_code,
                "interim_keywords": interim_keywords,
                "annual_keywords": annual_keywords,
                "remaining_pdfs": pdf_links[1:],
                "interim_reports": [],
                "annual_reports": [],
            },
            dont_filter=True,
        )

    def process_pdf(self, response):
        interim_reports = list(response.meta['interim_reports'])
        annual_reports  = list(response.meta['annual_reports'])

        classification = self._classify_pdf(
            response.body, response.url,
            response.meta['interim_keywords'],
            response.meta['annual_keywords'],
        )
        if classification == 'interim':
            interim_reports.append(response.url)
        elif classification == 'annual':
            annual_reports.append(response.url)

        remaining = response.meta['remaining_pdfs']
        shared_meta = {
            "isin": response.meta['isin'],
            "base_url": response.meta['base_url'],
            "reports_url": response.meta['reports_url'],
            "country_code": response.meta['country_code'],
            "interim_keywords": response.meta['interim_keywords'],
            "annual_keywords": response.meta['annual_keywords'],
            "interim_reports": interim_reports,
            "annual_reports": annual_reports,
        }

        if remaining:
            yield scrapy.Request(
                remaining[0],
                callback=self.process_pdf,
                meta={**shared_meta, "remaining_pdfs": remaining[1:]},
                dont_filter=True,
            )
        else:
            yield {
                "ISIN": shared_meta['isin'],
                "Website URL": shared_meta['base_url'],
                "Reports/Investors URL": shared_meta['reports_url'],
                "Interim Reports": interim_reports,
                "Annual Reports": annual_reports,
            }

    def _classify_pdf(self, pdf_body, pdf_url, interim_keywords, annual_keywords):
        """Returns 'interim', 'annual', or None based on keyword matches in the first 5 pages."""
        try:
            with fitz.open(stream=pdf_body, filetype="pdf") as pdf:
                if pdf.page_count <= 8:
                    return None
                pages_text = [
                    self.normalize_text(pdf[i].get_text()).lower()
                    for i in range(min(5, pdf.page_count))
                ]
            for page_text in pages_text:
                for keyword in interim_keywords:
                    if keyword in page_text[:200] or keyword in page_text[-200:]:
                        self.log(f"Interim keyword '{keyword}' found in {pdf_url}")
                        return 'interim'
            for page_text in pages_text:
                for keyword in annual_keywords:
                    if keyword in page_text[:200] or keyword in page_text[-200:]:
                        self.log(f"Annual keyword '{keyword}' found in {pdf_url}")
                        return 'annual'
        except Exception as e:
            self.log(f"Error processing PDF {pdf_url}: {e}")
        return None

    def normalize_text(self, txt):
        normalized = unicodedata.normalize('NFKD', txt)
        normalized = "".join(char for char in normalized if not unicodedata.combining(char))
        table = str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZéÉöÖåÅäÄ-",
            "abcdefghijklmnopqrstuvwxyzeeooaaaa "
        )
        return normalized.translate(table)
