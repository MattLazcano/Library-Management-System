from __future__ import annotations

from datetime import datetime
from src import library_functions as lib
from class_lib_items import BookItem, EBookItem, DVDItem
from class_member import Member
from class_search import Search
from class_loan import Loan


class LibrarySystem:
    """
    High-level facade for the whole library system.

    - Uses LibraryItem subclasses (BookItem, EBookItem, DVDItem) for catalog items
    - Uses Member for patron accounts
    - Uses Search for catalog search, reservations, recommendations
    - Uses Loan for representing individual borrow transactions
    - All of this is backed by the shared globals in library_functions.py
    """

    def __init__(self):
        # Just convenient references to the shared state
        self.catalog = lib.catalog
        self.members = lib.members
        self.loans = lib.loans
        self.ratings = lib.ratings
        self.average_ratings = lib.average_ratings

        # Composition: LibrarySystem HAS a Search controller
        self.search = Search()

    # ---------------------------
    # Item creation (Book / E-Book / DVD)
    # ---------------------------
    def add_book(
        self,
        item_id: str,
        title: str,
        author: str,
        genre: str,
        copies_total: int = 1,
    ) -> BookItem:
        """
        Create a physical book item and register it in the global catalog.

        Under the hood, BookItem.__init__ validates the ID and
        appends a record to lib.catalog.
        """
        return BookItem(item_id, title, author, genre, copies_total=copies_total)

    def add_ebook(
        self,
        item_id: str,
        title: str,
        author: str,
        genre: str,
        copies_total: int = 1,
    ) -> EBookItem:
        """Create an e-book item and register it in the global catalog."""
        return EBookItem(item_id, title, author, genre, copies_total=copies_total)

    def add_dvd(
        self,
        item_id: str,
        title: str,
        author: str,
        genre: str,
        copies_total: int = 1,
    ) -> DVDItem:
        """Create a DVD item and register it in the global catalog."""
        return DVDItem(item_id, title, author, genre, copies_total=copies_total)

    # ---------------------------
    # Member creation
    # ---------------------------
    def add_member(self, member_id: str, name: str, email: str) -> Member:
        """
        Create a Member object and register it in the global members dict.

        This assumes your Member.__init__ either:
        - adds itself to lib.members, OR
        - you manually do that after constructing it.
        """
        m = Member(member_id, name, email)
        # If your Member doesn't auto-register, you could do:
        # lib.members[member_id] = {"name": name, "email": email, "active": True}
        return m

    # ---------------------------
    # Loan creation helper
    # ---------------------------
    def create_loan(
        self,
        member_id: str,
        item_id: str,
        borrow_date: datetime | None = None,
        loan_days: int | None = None,
    ) -> Loan:
        """
        Convenience wrapper to create a Loan object.

        This delegates to your Loan class, which should handle:
        - computing due date (maybe using calculate_due_date or loan period)
        - updating lib.loans or whatever structure you're using
        """
        if borrow_date is None:
            borrow_date = datetime.now()

        if loan_days is None:
        # Let Loan use its own default (14)
            return Loan(member_id, item_id, borrow_date=borrow_date)
        else:
            return Loan(member_id, item_id, borrow_date=borrow_date, loan_days=loan_days)

    """
    # ---------------------------
    # Convenience wrappers to Search / function library
    # ---------------------------
    def search_catalog(self, query: str = "", author: str = "", genre: str = "", available: bool | None = None):
        # Thin wrapper around the Search controller.
        return self.search.find_books(query=query, author=author, genre=genre, available=available)

    def reserve_item(self, member_id: str, item_id: str) -> str:
        # Reserve an item for a member (delegates to library_functions).
        return lib.reserve_book(member_id, item_id)"""

    def rate_item(self, member_id: str, item_id: str, rating: int) -> str:
        # Rate an item (delegates to library_functions.rate_book).
        return lib.rate_book(member_id, item_id, rating)

    def __str__(self) -> str:
        return (
            f"LibrarySystem — {len(self.catalog)} items, "
            f"{len(self.members)} members, "
            f"{len(self.loans)} loans."
        )