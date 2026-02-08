"""Modèles de données."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any
import uuid
import json


@dataclass
class Product:
    """Modèle représentant un produit cosmétique."""

    source: str  # sephora, nocibe, marionnaud
    product_id: str  # ID du site source
    name: str
    brand: str
    price: float
    currency: str = "EUR"
    url: str = ""
    image_url: str = ""
    category: str = ""
    is_new: bool = False
    metadata: Dict[str, Any] = None
    id: str = None
    scraped_at: str = None

    def __post_init__(self):
        """Initialise les champs auto-générés."""
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.scraped_at is None:
            self.scraped_at = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convertit le produit en dictionnaire."""
        data = asdict(self)
        data['metadata'] = json.dumps(self.metadata)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Crée un produit depuis un dictionnaire."""
        if isinstance(data.get('metadata'), str):
            data['metadata'] = json.loads(data['metadata'])
        return cls(**data)

    def __repr__(self) -> str:
        return f"Product(source={self.source}, brand={self.brand}, name={self.name[:30]}..., price={self.price}€)"
