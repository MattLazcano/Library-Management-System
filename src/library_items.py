# --------------------------------------------
# Project 3 – Library Item Inheritance System
# --------------------------------------------

from abc import ABC, abstractmethod
from datetime import date, timedelta


class LibraryItem(ABC):
    """
    Abstract base class for all catalog items.
    Defines polymorphic method: calculate_loan_period().
    """

    def __init__(self, item_id: str, title: str, author: str, genre: str):
        if not item_id or not title:
            raise ValueError("item_id and title must not be empty")

        self._item_id = item_id
        self._title = title
        self._author = author
        self._genre = genre

    # ---- Required property for subclasses ----
    @property
    @abstractmethod
    def media_type(self) -> str:
        pass

    # ---- Polymorphic method ----
    @abstractmethod
    def calculate_loan_period(self) -> int:
        """Subclasses define different loan periods."""
        pass

    # ---- Concrete method using polymorphism ----
    def due_date_for(self, checkout_date: date) -> date:
        return checkout_date + timedelta(days=self.calculate_loan_period())

    # ---- Simple string helper ----
    def describe(self) -> str:
        return f"[{self.media_type}] {self._title} by {self._author} — {self._genre}"

    # Expose ID for Catalog storage
    @property
    def item_id(self) -> str:
        return self._item_id
    


class BookItem(LibraryItem):
    """Regular physical book"""

    def __init__(self, item_id: str, title: str, author: str, genre: str):
        super().__init__(item_id, title, author, genre)
    @property
    def media_type(self):
        return "Book"

    def calculate_loan_period(self) -> int:
        return 21  # 3 weeks
    
class EBookItem(LibraryItem):
    """Digital book"""

    def __init__(self, item_id: str, title: str, author: str, genre: str):
        super().__init__(item_id, title, author, genre)

    @property
    def media_type(self):
        return "E-Book"

    def calculate_loan_period(self) -> int:
        return 14  # 2 weeks


class DVDItem(LibraryItem):
    """DVD movie"""

    def __init__(self, item_id: str, title: str, author: str, genre: str):
        super().__init__(item_id, title, author, genre)
        
    @property
    def media_type(self):
        return "DVD"

    def calculate_loan_period(self) -> int:
        return 7  # 1 week


