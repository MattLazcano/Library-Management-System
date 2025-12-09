from src import library_functions as lib

class Search:
    """Handles all catalog searching, reservations, and recommendations."""
    
    def __init__(self):
        """Initialize the search controller and sync with global data."""
        self._catalog = lib.catalog
        self._members = lib.members
        self._reservations = lib.reservations
        self._waitlists = lib.waitlists


    # -------------------------------
    # Methods (Integrated)
    # -------------------------------
    def find_books(self, query="", author="", genre="", available=None):
        """Search the catalog for books."""
        return lib.search_catalog(query, author, genre, available)

    def reserve(self, member_id: str, item_id: str):
        """Reserve a book or add user to the waitlist."""
        return lib.reserve_book(member_id, item_id)

    def manage_waitlist(self, item_id: str, member_id: str, action="add"):
        """Add or notify members on waitlist."""
        return lib.waitlist_management(item_id, member_id, action)

    def recommend_for_member(self, member_id: str, limit: int = 10):
        """Recommend books using Project 1 algorithm."""
        return lib.recommend_books(member_id=member_id, limit=limit)

    def normalize_query(self, q: str):
        """Clean up and tokenize a search query."""
        return lib.format_search_query(q)

    def __str__(self):
        return "Search system ready for user queries."
