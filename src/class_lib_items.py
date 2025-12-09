from src import library_functions as lib

# Incororate library_items into this book class so that its not book class anymore instead just class_items? (DONE)
# Find a way to connext this integration class thingy to the global data so that everything still works together (DONE)
# Once you find a way to incororate the class to the global structures then polymorphism works (DONE)
# Next thing to do after that is rework the ABC and composition if they do need any rework after everything that i'll do (DONE)
# I need to fix up loan and all other classes that use book class since i will be making the changes DONE
# change isbn to just item_id, because using jsut number will be confusing, Im allowed to just delete the isbn functions (DONE)
# change validate code so that the item_id either starts with a BK, DV, or a EB and then has a total of 5 chars (ex: BK102) (DONE)
# change all book_id to item_id (DONE)

from abc import ABC, abstractmethod
from datetime import date, timedelta
from src import library_functions as lib


class LibraryItem(ABC):
    """
    Abstract base class for all catalog items.
    Each item automatically registers itself into the global catalog.
    """

    def __init__(self, item_id: str, title: str, author: str, genre: str, copies_total: int = 1):

        # ---- Global Validation ----
        if not lib.validate_code(item_id):
            raise ValueError(f"Invalid book/item ID or ISBN: {item_id}")
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if copies_total < 1:
            raise ValueError("copies_total must be at least 1.")

        self._item_id = item_id
        self._title = title
        self._author = author
        self._genre = genre
        self._copies_total = copies_total
        self._copies_available = copies_total

        # -----------------------------------------------
        # Register item into GLOBAL catalog
        # -----------------------------------------------
        record = {
            "id": self._item_id,
            "title": self._title,
            "author": self._author,
            "genre": self._genre,
            "media_type": self.media_type,   # polymorphic
            "tags": set(),
            "copies_total": self._copies_total,
            "copies_available": self._copies_available,
            "waitlist": []
        }

        lib.catalog.append(record)

    # --------------------------------------------------------------------
    # ABSTRACT INTERFACE (polymorphism)
    # --------------------------------------------------------------------
    @property
    @abstractmethod
    def media_type(self) -> str:
        pass

    @abstractmethod
    def calculate_loan_period(self) -> int:
        pass

    # --------------------------------------------------------------------
    # Shared logic for all item types
    # --------------------------------------------------------------------
    def due_date_for(self, checkout_date: date) -> date:
        return checkout_date + timedelta(days=self.calculate_loan_period())

    def describe(self):
        return f"[{self.media_type}] {self._title} by {self._author} — {self._genre}"


    # -------------------------------
    # Properties
    # -------------------------------
    @property
    def item_id(self):
        """str: The unique book ID."""
        return self._item_id
    
    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def genre(self):
        return self._genre
    
    # --------------------------------------------------------------------
    # Global-linked Functions
    # --------------------------------------------------------------------

    def adjust_copies(self, change: int):
        """Update availability in BOTH the object and the global catalog."""
        new_amount = self._copies_available + change
        if new_amount < 0 or new_amount > self._copies_total:
            raise ValueError("Copy count out of valid range.")

        self._copies_available = new_amount

        for item in lib.catalog:
            if item["id"] == self._item_id:
                item["copies_available"] = new_amount
                break

    def add_rating(self, member_id: str, rating: int):
        return lib.rate_book(member_id, self._item_id, rating)

    def check_availability(self):
        return lib.is_book_available(self._title)


    def __str__(self):
        status = "Available" if self.is_available else "Checked out"
        return f"{self.describe()} — {status} ({self._copies_available}/{self._copies_total})"


# ============================================================
# CONCRETE ITEM TYPES (Inheritance + Polymorphism)
# ============================================================

class BookItem(LibraryItem):

    def __init__(self, item_id: str, title: str, author: str, genre: str):
            super().__init__(item_id, title, author, genre)

    @property
    def media_type(self):
        return "Book"

    def calculate_loan_period(self) -> int:
        return 21  # 3 weeks


class EBookItem(LibraryItem):

    def __init__(self, item_id: str, title: str, author: str, genre: str):
            super().__init__(item_id, title, author, genre)
    
    @property
    def media_type(self):
        return "E-Book"

    def calculate_loan_period(self) -> int:
        return 14


class DVDItem(LibraryItem):

    def __init__(self, item_id: str, title: str, author: str, genre: str):
            super().__init__(item_id, title, author, genre)
    
    @property
    def media_type(self):
        return "DVD"

    def calculate_loan_period(self) -> int:
        return 7