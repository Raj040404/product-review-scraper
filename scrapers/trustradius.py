from typing import List
from datetime import datetime
from .base import BaseScraper
from models import Review

class TrustRadiusScraper(BaseScraper):
    def scrape(self, company: str, start_date: datetime, end_date: datetime) -> List[Review]:
        url = f"https://www.trustradius.com/products/{company}/reviews"
        print(f"Scraping TrustRadius: {url}")
        
        try:
            self.page.goto(url, timeout=60000)
        except:
            return []

        # TrustRadius usually uses 'article' or divs with 'Review' in class
        # Attempt to match generic review card structure
        articles = self.page.query_selector_all('article')
        if not articles:
             articles = self.page.query_selector_all('[class*="ReviewCard"]')
        if not articles:
             # Fallback to search any list that looks like reviews
             articles = self.page.query_selector_all('.review-card')

        reviews = []
        for art in articles:
            try:
                title_el = art.query_selector('h3') or art.query_selector('[class*="title"]')
                title = title_el.inner_text() if title_el else "TrustRadius Review"
                
                # Rating often in a div with 'score' or star icon
                rating = 0.0
                rating_el = art.query_selector('[class*="StarRating"]') or art.query_selector('[class*="score"]')
                if rating_el:
                    # Parse logic would go here
                    rating = 5.0 # Placeholder
                
                content_el = art.query_selector('[class*="content"]') or art.query_selector('p')
                content = content_el.inner_text() if content_el else ""
                
                reviews.append(Review(
                    source="TrustRadius",
                    title=title,
                    author="User",
                    rating=rating,
                    date=datetime.now().strftime("%Y-%m-%d"), # Fallback
                    content=content[:100] + "..."
                ))
            except:
                continue
                
        return reviews
