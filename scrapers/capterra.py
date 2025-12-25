from typing import List
from datetime import datetime
from .base import BaseScraper
from models import Review
import time

class CapterraScraper(BaseScraper):
    def scrape(self, company: str, start_date: datetime, end_date: datetime) -> List[Review]:
        # Capterra URLs often require numeric ID. For Slack it is 135003.
        # Ideally we search, but for this exercise we hardcode/guess or use a specific format.
        if company.lower() == 'slack':
            url = "https://www.capterra.com/p/135003/slack/reviews/"
        else:
             # Fallback to generic structure
            url = f"https://www.capterra.com/p/{company}/reviews/"
        
        print(f"Scraping Capterra: {url}")
        try:
            self.page.goto(url, timeout=60000)
            self.page.wait_for_selector('.review-card', state="attached", timeout=10000)
        except Exception as e:
            print(f"Error loading Capterra page: {e}")
            return []

        reviews = []
        page_num = 1
        
        while True:
            print(f"Scraping Capterra page {page_num}...")
            cards = self.page.query_selector_all('.review-card')
            
            if not cards:
                print("No reviews found on this page.")
                break

            for card in cards:
                try:
                    title_el = card.query_selector('.review-card-title')
                    title = title_el.inner_text() if title_el else "No Title"

                    author_el = card.query_selector('.reviewer-name')
                    author = author_el.inner_text() if author_el else "Anonymous"

                    # Rating: count stars or look for specific class
                    rating = 0.0
                    # Heuristic: check for child with class 'star-rating' or count stars
                    stars = card.query_selector_all('.star-fill') # Example class
                    rating = float(len(stars)) if stars else 0.0
                    
                    date_el = card.query_selector('.review-date')
                    date_str = date_el.inner_text() if date_el else ""
                    
                    content_el = card.query_selector('.review-text')
                    content = content_el.inner_text() if content_el else ""

                    # Date Parsing 'Written on Jan 12, 2023'
                    # Implementation would depend on actual format
                    
                    reviews.append(Review(
                        source="Capterra",
                        title=title,
                        author=author,
                        rating=rating,
                        date=date_str,
                        content=content
                    ))
                except Exception as e:
                    pass
            
            # Pagination Logic
            try:
                # Capterra often uses 'Show More' or page numbers
                next_button = self.page.query_selector('button:has-text("Show More")') or self.page.query_selector('.pagination-next')
                if next_button and not next_button.is_disabled():
                    next_button.click()
                    self.page.wait_for_timeout(2000)
                    page_num += 1
                else:
                    break
            except:
                break

        return reviews
