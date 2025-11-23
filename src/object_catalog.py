# --------------------------------------------
# Project 3 – Composition Catalog
# Stores LibraryItem objects
# --------------------------------------------

from typing import Dict
from src.library_items import LibraryItem
import library_functions as lf


class ObjectCatalog:
    """
    Composition class.
    Stores LibraryItem objects and also syncs them into the global 'catalog' list.
    """

    def __init__(self):
        self._items: Dict[str, LibraryItem] = {}

    def add(self, item: LibraryItem):
        """Store LibraryItem AND push into global catalog as dict."""

        # store the object
        self._items[item.item_id] = item

        # Make sure it exists in P2-style global data
        lf.catalog.append({
            "id": item.item_id,
            "title": item._title,
            "author": item._author,
            "genre": item._genre,
            "copies_total": 1,
            "copies_available": 1
        })

    def get(self, item_id: str):
        return self._items.get(item_id)

    def all_items(self):
        return list(self._items.values())

    def __len__(self):
        return len(self._items)
