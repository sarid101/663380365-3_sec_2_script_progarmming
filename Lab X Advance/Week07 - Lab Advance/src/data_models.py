# agentic-web-scraper/src/data_models.py
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Product:
    """Data model for a scraped product."""
    name: str
    price: str
    description: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
