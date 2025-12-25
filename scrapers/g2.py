from typing import List
from datetime import datetime
from .base import BaseScraper
from models import Review
import time

class G2Scraper(BaseScraper):
    def scrape(self, company: str, start_date: datetime, end_date: datetime) -> List[Review]:
        url = f"https://www.g2.com/products/{company}/reviews"
        print(f"Scraping G2: {url}")
        
        try:
            self.page.goto(url, timeout=60000)
            # Handle potential bot checks manually or via retry
            # self.page.wait_for_selector('.review-card', timeout=10000) 
        except Exception as e:
            print(f"Error loading page: {e}")
            return []

        reviews = []
        page_num = 1
        
        while True:
            print(f"Scraping G2 page {page_num}...")
            # Selectors (approximate, these change often)
            review_elements = self.page.query_selector_all('.paper') or self.page.query_selector_all('[itemprop="review"]')
            
            if not review_elements:
                print("No reviews found on this page.")
                break

            for el in review_elements:
                try:
                    # Title
                    title_el = el.query_selector('[itemprop="headline"]')
                    title = title_el.inner_text() if title_el else "No Title"
                    
                    # Author
                    author_el = el.query_selector('[itemprop="author"]')
                    author = author_el.inner_text() if author_el else "Anonymous"
                    
                    # Rating
                    rating = 0.0
                    rating_el = el.query_selector('[itemprop="reviewRating"] [itemprop="ratingValue"]')
                    if rating_el:
                        rating = float(rating_el.get_attribute('content') or rating_el.inner_text())
                        
                    # Date
                    date_el = el.query_selector('[itemprop="datePublished"]')
                    date_str = ""
                    if date_el:
                        date_str = date_el.get_attribute('content') # ISO format usually
                    
                    # Content
                    content_el = el.query_selector('[itemprop="reviewBody"]')
                    content = content_el.inner_text() if content_el else ""

                    # Date Filtering
                    if date_str:
                        try:
                            # Normalize date format if needed
                            r_date = datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")
                            if r_date < start_date:
                                # reviews often sorted by date, if we hit older data we can stop
                                # return reviews # Optional optimization
                                pass
                            if not (start_date <= r_date <= end_date):
                                continue
                        except:
                            pass 

                    reviews.append(Review(
                        source="G2",
                        title=title,
                        author=author,
                        rating=rating,
                        date=date_str,
                        content=content
                    ))
                except Exception as e:
                    print(f"Error parsing a review: {e}")
                    continue
            
            # Pagination Logic
            next_button = self.page.query_selector('.pagination__named-link--next') # hypothetical selector
            if next_button and not next_button.is_disabled():
                try:
                    next_button.click()
                    self.page.wait_for_timeout(2000) # Wait for load
                    page_num += 1
                except:
                    break
            else:
                break
                
        return reviews
                
        return reviews
