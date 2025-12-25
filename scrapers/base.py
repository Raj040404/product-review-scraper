"""
Base scraper module.
Defines the abstract base class that all specific site scrapers must implement.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from models import Review
from playwright.sync_api import Playwright, sync_playwright

class BaseScraper(ABC):
    def __init__(self, playwright: Playwright):
        self.browser = playwright.chromium.launch(headless=True) # Use headless=False for debugging if needed
        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            }
        )
        self.page = self.context.new_page()

    @abstractmethod
    def scrape(self, company: str, start_date: datetime, end_date: datetime) -> List[Review]:
        pass

    def close(self):
        self.context.close()
        self.browser.close()

    def _is_date_in_range(self, review_date_str: str, start_date: datetime, end_date: datetime) -> bool:
        # Helper to parse dates common in these sites, implement specific parsing in subclasses if needed
        try:
            # Placeholder format, subclasses should handle specific parsing
            r_date = datetime.strptime(review_date_str, "%Y-%m-%d") 
            return start_date <= r_date <= end_date
        except:
            return False # Default to excluding if parsing fails
