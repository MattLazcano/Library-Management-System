"""
Library Management System - Demo Script

This script demonstrates how the library system classes (Book, Member, Search, Loan)
interact with the shared data in library_functions.py. It simulates realistic library
operations such as searching, borrowing, reserving, rating, and generating reports.

Author: Group 5 - Library Management System
"""

import sys
import os
from datetime import datetime, timedelta

# Dynamically locate the project root and add it to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "src"))

# Import the main classes and global data
from src.class_lib_items import BookItem, EBookItem, DVDItem
from src.class_member import Member
from src.class_search import Search
from src.class_loan import Loan
from src import library_functions as lib


# ------------------------------------------------------------
# SAMPLE DATA SETUP
# ------------------------------------------------------------
def setup_sample_data():
    """Populate the catalog and members with demo data."""
    lib.catalog[:] = [
        {"id": "1000000001", "title": "Dune", "author": "Frank Herbert", "genre": "sci-fi",
        "tags": {"sci-fi", "classic", "space"}, "copies_total": 3, "copies_available": 1,
        "waitlist": ["M2"]},  # Rood waiting for Dune
        {"id": "1000000002", "title": "Clean Code", "author": "Robert C. Martin", "genre": "programming",
        "tags": {"programming", "software", "best-practices"}, "copies_total": 2, "copies_available": 0,
        "waitlist": ["M3", "M5"]},
        {"id": "1000000003", "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "fantasy",
        "tags": {"fantasy", "adventure", "classic"}, "copies_total": 4, "copies_available": 2},
        {"id": "1000000004", "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "genre": "programming",
        "tags": {"programming", "craft", "career"}, "copies_total": 3, "copies_available": 1},
        {"id": "1000000005", "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "fiction",
        "tags": {"fiction", "classic", "literature"}, "copies_total": 2, "copies_available": 2},
        {"id": "1000000006", "title": "1984", "author": "George Orwell", "genre": "fiction",
        "tags": {"dystopia", "classic", "political"}, "copies_total": 5, "copies_available": 3},
    ]

    lib.members.clear()
    lib.members.update({
        "M1": {"name": "Matthew", "email": "matthew@example.com", "active": True, "balance": 0.0,
        "preferences_tags": {"sci-fi", "fantasy"},
        "preferences_authors": {"Frank Herbert"}, "loans": {}},
        "M2": {"name": "Rood", "email": "rood@example.com", "active": True, "balance": 0.0, "loans": {}},
        "M3": {"name": "Kaliza", "email": "kaliza@example.com", "active": True, "balance": 0.0, "loans": {}},
        "M4": {"name": "Abi", "email": "abi@example.com", "active": True, "balance": 0.0, "loans": {}},
        "M5": {"name": "Dempwolf", "email": "dempwolf@example.com", "active": True, "balance": 0.0, "loans": {}},
    })

    print("Sample dataset initialized: 6 books and 5 members.\n")


# ------------------------------------------------------------
# DEMO SECTIONS
# ------------------------------------------------------------
def demo_books_and_members():
    """Demonstrate creation and basic validation of Book and Member classes."""
    print("BOOK & MEMBER DEMO")
    print("=" * 50)

    print("Book Catalog before:", [b["title"] for b in lib.catalog])
    print("Member count before:", len(lib.members))
    print()

    print("adding new book and member...\n")
    new_book = BookItem("1000000010", "Artificial Intelligence: A Modern Approach",
                    "Russell & Norvig", "Computer Science", copies_total=5)
    new_member = Member("M100", "Jane Doe", "jane@example.com")

    print(f"Added book: {new_book}")
    print(f"Added member: {new_member}\n")
    print("Book Catalog after:", [b["title"] for b in lib.catalog])
    print("Member count after:", len(lib.members))
    print()

    print("Testing book validation:")
    print("Valid ISBN-10 for '1000000010':", new_book.validate_isbn10())

    print("\nCurrent catalog size:", len(lib.catalog))
    print("Current member count:", len(lib.members))
    print()


def demo_search_and_reservations():
    """Showcase searching, reserving, and query normalization."""
    print("SEARCH & RESERVATION DEMO")
    print("=" * 50)
    s = Search()

    print("\nSearch results for keyword 'code':")
    results = s.find_books(query="code")
    for r in results:
        print(" ", r)

    print("\nReserving unavailable book (Clean Code) for M1:")
    print(s.reserve("M1", "1000000002"))

    print("\nAdding M4 to waitlist for 'Dune':")
    print(s.manage_waitlist("1000000001", "M4", "add"))

    print("\nNormalized query example:")
    print(s.normalize_query('"data science" in modern AI'))

    print("\nRecommendations for Matthew (M1):")
    print(s.recommend_for_member("M1"))
    print()


def demo_loans_and_reports():
    """Demonstrate loan creation, overdue checks, and reporting."""
    print("LOAN & REPORT DEMO")
    print("=" * 50)
    l = Loan(member_id="M1", item_id="1000000003")  # Matthew borrows The Hobbit
    print("Loan record created:", l)

    print("Is loan overdue?", l.is_overdue())

    print("\nBorrowing report:")
    print(l.generate_reports())

    # Simulate an overdue book by adjusting due date
    l._due_date = datetime.now() - timedelta(days=10)
    print("\nOverdue notifications after date adjustment:")
    print(Loan.overdue_notifications())
    print()


def demo_ratings():
    """Demonstrate book rating and average updates."""
    print("RATING SYSTEM DEMO")
    print("=" * 50)

    dune = next((b for b in lib.catalog if b["id"] == "1000000001"), None)
    if dune:
        print("Initial average ratings:", lib.average_ratings)

        print("\nAdding new rating for Dune by M1:")
        print(lib.rate_book("M1", "1000000001", 5))

        print("Adding another rating for Dune by M3:")
        print(lib.rate_book("M3", "1000000001", 4))

        print("Updated averages:", lib.average_ratings)
    print()


# ------------------------------------------------------------
# MAIN FUNCTION
# ------------------------------------------------------------
def main():
    print("LIBRARY MANAGEMENT SYSTEM - DEMO SCRIPT")
    print("=" * 60)
    print("This demo illustrates how our classes interact with the shared global data.\n")

    setup_sample_data()
    demo_books_and_members()
    demo_search_and_reservations()
    demo_loans_and_reports()
    demo_ratings()

    print("=" * 60)
    print("DEMO COMPLETE! The library system is fully functional.")
    print("=" * 60)


if __name__ == "__main__":
    main()