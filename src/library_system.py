# --------------------------------------------
# Project 3 – Integrated Library System
# Ties together:
#   - library_functions (Project 1 & 2)
#   - ObjectCatalog (composition)
#   - LibraryItem hierarchy (inheritance + polymorphism)
# --------------------------------------------

from datetime import date
from src.object_catalog import ObjectCatalog
from src.library_items import BookItem, EBookItem, DVDItem
import library_functions as lf


class LibrarySystem:
    """
    Wrapper that integrates all pieces:
    - Project 1 functions
    - Project 2 classes
    - Project 3 inheritance hierarchy
    - Project 3 composition catalog
    """

    def __init__(self):
        # Composition
        self.catalog = ObjectCatalog()

        # References to existing P1/P2 structures
        self.members = lf.members
        self.loans = lf.loans
        self.waitlists = lf.waitlists
        self.reservations = lf.reservations

    # --------------------------
    # Add object-oriented items
    # --------------------------
    def add_book(self, item_id, title, author, genre):
        book = BookItem(item_id, title, author, genre)
        self.catalog.add(book)
        return book

    def add_ebook(self, item_id, title, author, genre):
        ebook = EBookItem(item_id, title, author, genre)
        self.catalog.add(ebook)
        return ebook

    def add_dvd(self, item_id, title, author, genre):
        dvd = DVDItem(item_id, title, author, genre)
        self.catalog.add(dvd)
        return dvd

    # --------------------------
    # Delegate to existing P1 functions
    # --------------------------
    def reserve(self, member_id, item_id):
        return lf.reserve_book(member_id, item_id)

    def search_catalog(self, *args, **kwargs):
        return lf.search_catalog(*args, **kwargs)

    # Example polymorphic usage
    def get_due_date(self, item_id, checkout_date: date):
        item = self.catalog.get(item_id)
        if item:
            return item.due_date_for(checkout_date)
        return None
