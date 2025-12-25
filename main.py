"""
Main entry point for the Product Review Scraper.

This script orchestrates the scraping process across multiple sources (G2, Capterra, TrustRadius).
It handles command-line argument parsing, scraper instantiation, and JSON output generation.
"""
import argparse
import json
from datetime import datetime
from typing import List
from playwright.sync_api import sync_playwright
from scrapers.g2 import G2Scraper
from scrapers.capterra import CapterraScraper
from scrapers.trustradius import TrustRadiusScraper
from models import Review

def main():
    parser = argparse.ArgumentParser(description="Product Review Scraper")
    parser.add_argument("--company", required=True, help="Company or Product name")
    parser.add_argument("--start_date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end_date", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--source", choices=["g2", "capterra", "trustradius", "all"], default="all", help="Source to scrape")
    
    args = parser.parse_args()
    
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    reviews: List[Review] = []
    
    with sync_playwright() as p:
        scrapers = []
        if args.source in ["g2", "all"]:
            scrapers.append(G2Scraper(p))
        if args.source in ["capterra", "all"]:
            scrapers.append(CapterraScraper(p))
        if args.source in ["trustradius", "all"]:
            scrapers.append(TrustRadiusScraper(p))
            
        for scraper in scrapers:
            try:
                print(f"Starting scrape for {scraper.__class__.__name__}...")
                results = scraper.scrape(args.company, start_date, end_date)
                print(f"Found {len(results)} reviews from {scraper.__class__.__name__}")
                reviews.extend(results)
            except Exception as e:
                print(f"Error during scrape: {e}")
            finally:
                scraper.close()

    # Save to JSON
    output_file = "reviews.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in reviews], f, indent=4, default=str)
        
    print(f"Total reviews scraped: {len(reviews)}")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
