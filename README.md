# PWScrape: Financial Report Scraper for Publicly Traded Companies

PWScrape is a web scraping pipeline that automatically collects annual and interim financial reports from the investor relations pages of publicly traded European companies. Given a list of companies with their website URLs and ISINs, it navigates each company's site, locates the relevant reports section, and downloads and classifies the PDF documents it finds.

The motivation is straightforward: financial research on a large number of companies requires gathering earnings reports that are published on each company's own website. Doing this manually across hundreds of stocks is impractical. PWScrape automates the navigation, classification, and data collection so that reports can be retrieved at scale.

---

## How It Works

The spider processes each company through a multi-stage pipeline:

1. **Homepage navigation** — loads the company's website using a real Chromium browser (via Playwright) to handle JavaScript-rendered pages and cookie consent dialogs.
2. **Reports section discovery** — searches for links to the financial reports section using a library of localized keywords (e.g. *Finanzberichte*, *rapports financiers*, *annual reports*).
3. **Investor relations fallback** — if no reports section is found directly, the spider first navigates to the investor relations page and retries from there.
4. **PDF extraction** — collects all PDF links from the reports page.
5. **Document classification** — downloads the first five pages of each PDF and scans them for keywords to classify each document as either an **interim report** (half-year / quarterly) or an **annual report**.
6. **Structured output** — results are written to a JSON file, one entry per company.

### Output format

```json
{
  "ISIN": "DE000A3E5E55",
  "Website URL": "https://ringmetall.de",
  "Reports/Investors URL": "https://ringmetall.de/investor-relations/finanzberichte",
  "Interim Reports": ["https://ringmetall.de/.../h1_2023.pdf"],
  "Annual Reports":  ["https://ringmetall.de/.../annual_2022.pdf"]
}
```

---

## Multi-Country Support

The spider determines which keyword set to load from the first two characters of the company's ISIN (the country code). Keyword files currently exist for:

| Country | ISIN Prefix | Keyword file |
|---------|-------------|--------------|
| Germany | DE | `keywords/de_keywords.py` |
| United Kingdom | GB | `keywords/gb_keywords.py` |
| Sweden | SE | `keywords/se_keywords.py` |
| Netherlands | NL | `keywords/nl_keywords.py` |
| France | FR | `keywords/fr_keywords.py` |

To add support for a new country, create a `keywords/{cc}_keywords.py` file that defines `INVESTOR_KEYWORDS`, `REPORTS_KEYWORDS`, `INTERIM_KEYWORDS`, and `ANNUAL_KEYWORDS`. No other changes are needed.

---

## Tech Stack

- **[Scrapy](https://scrapy.org/)** — async crawling framework that handles concurrency, retries, and rate limiting.
- **[scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright)** — renders JavaScript-heavy investor relations pages using a real Chromium browser.
- **[PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)** — reads the first pages of each PDF to extract text for keyword classification.

---

## Input Format

The spider reads from `100_de.csv`, a CSV file where each row represents a publicly traded company. Required columns:

| Column | Description |
|--------|-------------|
| `ISIN` | International Securities Identification Number (country prefix used to select keyword language) |
| `Company URL` | The company's public website homepage |

A sample file with 100 German stocks is included for testing.

---

## Prerequisites

- Python 3.9+
- [Scrapy](https://scrapy.org/) (installed via requirements.txt)
- [Playwright](https://playwright.dev/) browser binaries (see Installation step 4)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/pwscrape.git
   cd pwscrape
   ```

2. **Set up the virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browser binaries**:
   ```bash
   playwright install chromium
   ```

---

## Usage

```bash
scrapy crawl company_spider -o output.json --logfile=scrapy_log.txt
```

Results are saved to `output.json`. The log file captures per-request detail useful for debugging navigation failures.

---

## Configuration

Key settings in `pwscrape/settings.py`:

| Setting | Default | Notes |
|---------|---------|-------|
| `CONCURRENT_REQUESTS` | 12 | Increase for faster runs; raises block risk |
| `DOWNLOAD_DELAY` | 4s | Delay between requests per domain |
| `AUTOTHROTTLE_ENABLED` | True | Automatically adjusts delay based on server response times |
| `ROBOTSTXT_OBEY` | True | Respects each site's robots.txt |

---

## Limitations & Future Improvements

- **Accuracy** — keyword matching is the current classification method; a trained classifier or LLM-based approach would improve precision on edge cases.
- **Sitemap navigation** — some sites organize reports under sitemap paths that the current link-following strategy misses.
- **Year tab toggling** — paginated report archives that split documents across year tabs are not yet handled.
- **URL validation** — adding a path-based check to confirm the spider has actually reached a reports page (rather than a general IR landing page) would reduce false positives.
