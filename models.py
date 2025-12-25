"""
Data models for the Product Review Scraper.
Defines the structure for scraped review data to ensure consistency across sources.
"""
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Review:
    source: str
    title: str
    author: str
    rating: float
    date: str
    content: str
    
    def to_dict(self):
        return asdict(self)
