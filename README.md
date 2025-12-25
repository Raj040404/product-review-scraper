# Product Review Scraper

A Python-based tool to scrape product reviews from **G2**, **Capterra**, and **TrustRadius** (Bonus Source).

## Features

- **Multi-Source Scraping**: Support for G2, Capterra, and TrustRadius.
- **Date Filtering**: Filter reviews by a specific date range.
- **JSON Output**: Exports scraped data to a structured JSON file.
- **Modular Design**: Extensible architecture for adding new scrapers.

## Installation

1. **Clone the repository** (or navigate to the project directory).
2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Install Playwright browsers**:

    ```bash
    playwright install
    ```

## Usage

Run the script using `main.py` with the following arguments:

```bash
python main.py --company <company_name> --start_date <YYYY-MM-DD> --end_date <YYYY-MM-DD> --source <source>
```

### Arguments

- `--company`: Name of the company/product (e.g., `slack`).
- `--start_date`: Start date for reviews (YYYY-MM-DD).
- `--end_date`: End date for reviews (YYYY-MM-DD).
- `--source`: Source of reviews. Options: `g2`, `capterra`, `trustradius`, `all`.

### Example

```bash
python main.py --company slack --start_date 2023-01-01 --end_date 2023-12-31 --source all
```

## Output

The script generates a `reviews.json` file in the current directory containing the scraped reviews.

**Sample Output Structure:**

```json
[
    {
        "source": "G2",
        "title": "Great tool for team collaboration",
        "author": "Jane Doe",
        "rating": 4.5,
        "date": "2023-05-15",
        "content": "Slack has revolutionized..."
    }
]
```

*(See `sample_output.json` for a full example)*

## Bonus: Third Source Integration

**TrustRadius** has been integrated as the third source for SaaS app reviews. It is implemented in `scrapers/trustradius.py` and shares the same interface and capabilities as the G2 and Capterra scrapers.

## Known Limitations

Scraping high-profile review sites like G2 and Capterra is heavily restricted by anti-bot technologies (Cloudflare, DataDome). During testing, this scraper successfully navigates to pages but may yield 0 results if the IP is blocked. In a production environment, this would require integration with residential proxies or stealth plugins.
