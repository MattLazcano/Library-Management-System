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
from pathlib import Path

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
from src.library_system import LibrarySystem
from src import library_functions as lib
from src import persistence


# ------------------------------------------------------------
# SAMPLE DATA SETUP
# ------------------------------------------------------------
def setup_sample_data():
    """Populate the catalog and members with demo data."""

    # Clear all global structures so the demo is repeatable
    lib.catalog.clear()
    lib.members.clear()
    lib.loans.clear()
    lib.ratings.clear()
    lib.average_ratings.clear()
    lib.reminders.clear()
    lib.reservations.clear()

    # Same sample catalog as before, now including media_type and waitlist fields
    lib.catalog[:] = [
        {
            "id": "BK101",
            "title": "Dune",
            "author": "Frank Herbert",
            "genre": "sci-fi",
            "media_type": "Book",
            "tags": {"sci-fi", "classic", "space"},
            "copies_total": 3,
            "copies_available": 0,
            "waitlist": ["M2"],  # Rood waiting for Dune
        },
        {
            "id": "BK102",
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "genre": "programming",
            "media_type": "Book",
            "tags": {"programming", "software", "best-practices"},
            "copies_total": 2,
            "copies_available": 0,
            "waitlist": ["M3", "M5"],
        },
        {
            "id": "BK103",
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "genre": "fantasy",
            "media_type": "Book",
            "tags": {"fantasy", "adventure", "classic"},
            "copies_total": 4,
            "copies_available": 2,
            "waitlist": [],
        },
        {
            "id": "BK104",
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "genre": "programming",
            "media_type": "Book",
            "tags": {"programming", "craft", "career"},
            "copies_total": 3,
            "copies_available": 1,
            "waitlist": [],
        },
        {
            "id": "BK105",
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "genre": "fiction",
            "media_type": "Book",
            "tags": {"fiction", "classic", "literature"},
            "copies_total": 2,
            "copies_available": 2,
            "waitlist": [],
        },
        {
            "id": "BK106",
            "title": "1984",
            "author": "George Orwell",
            "genre": "fiction",
            "media_type": "Book",
            "tags": {"dystopia", "classic", "political"},
            "copies_total": 5,
            "copies_available": 3,
            "waitlist": [],
        },
    ]

    # Same sample members as before
    lib.members.update(
        {
            "M1": {
                "name": "Matthew",
                "email": "matthew@example.com",
                "active": True,
                "balance": 0.0,
                "preferences_tags": {"sci-fi", "fantasy"},
                "preferences_authors": {"Frank Herbert"},
                "loans": {},
            },
            "M2": {
                "name": "Rood",
                "email": "rood@example.com",
                "active": True,
                "balance": 0.0,
                "loans": {},
            },
            "M3": {
                "name": "Kaliza",
                "email": "kaliza@example.com",
                "active": True,
                "balance": 0.0,
                "loans": {},
            },
            "M4": {
                "name": "Abi",
                "email": "abi@example.com",
                "active": True,
                "balance": 0.0,
                "loans": {},
            },
            "M5": {
                "name": "Dempwolf",
                "email": "dempwolf@example.com",
                "active": True,
                "balance": 0.0,
                "loans": {},
            },
        }
    )

    print("Sample dataset initialized: 6 items and 5 members.\n")


# ------------------------------------------------------------
# DEMO SECTIONS
# ------------------------------------------------------------
def demo_items_and_members():
    """Demonstrate creation and basic validation of LibraryItem subclasses and Member."""
    print("ITEM & MEMBER DEMO")
    print("=" * 50)

    print("Catalog before:", [b["title"] for b in lib.catalog])
    print("Member count before:", len(lib.members))
    print()

    print("Adding new items and member via classes...\n")
    new_book = BookItem(
        "BK110",
        "Artificial Intelligence: A Modern Approach",
        "Russell & Norvig",
        "computer science",
        copies_total=5,
    )
    new_ebook = EBookItem("EB200", "Python Tricks", "Dan Bader", "programming", copies_total=2)
    new_dvd = DVDItem("DV300", "The Matrix", "Wachowski", "sci-fi", copies_total=1)
    new_member = Member("M100", "Jane Doe", "jane@example.com")

    print(f"Added item: {new_book}")
    print(f"Added item: {new_ebook}")
    print(f"Added item: {new_dvd}")
    print(f"Added member: {new_member}\n")

    print("Catalog after:", [b["id"] + ' - ' + b["title"] for b in lib.catalog])
    print("Member count after:", len(lib.members))
    print()

    print("Validating one of the new member accounts via user_account():")
    print("  validate_account(M100) ->", new_member.validate_account())
    print()


def demo_search_and_reservations():
    """Showcase searching, reserving, waitlists, query normalization, and recommendations."""
    print("SEARCH & RESERVATION DEMO")
    print("=" * 50)
    s = Search()

    print("\nSearch results for keyword 'code':")
    results = s.find_books(query="code")
    for r in results:
        print(" ", r["id"], "-", r["title"])

    print("\nReserving unavailable book (Clean Code, BK102) for M1:")
    print(" ", s.reserve("M1", "BK102"))

    print("\nAdding M4 to waitlist for 'Dune' (BK101):")
    print(" ", s.manage_waitlist("BK101", "M4", "add"))
    dune = next(b for b in lib.catalog if b["id"] == "BK101")
    print("  Current waitlist for BK101:", dune.get("waitlist", []))

    print("\nNormalized query example for: \"data science\" in modern AI")
    print(" ", s.normalize_query('"data science" in modern AI'))

    print("\nRecommendations for Matthew (M1):")
    print(" ", s.recommend_for_member("M1"))
    print()


def demo_loans_and_reports():
    """Demonstrate loan creation, overdue checks, and borrowing reports."""
    print("LOAN & REPORT DEMO")
    print("=" * 50)

    # Member M1 borrows The Hobbit (BK103)
    loan = Loan(member_id="M1", item_id="BK103")
    print("Loan record created:", loan)
    print("Is loan overdue right now?", loan.is_overdue())

    print("\nBorrowing report after one loan:")
    print(lib.generate_borrowing_report())

    # Make that loan overdue by editing the stored loan record
    # (This simulates time passing for demo purposes.)
    if lib.loans:
        lib.loans[0]["due_date"] = datetime.now() - timedelta(days=5)

    print("\nOverdue notifications after simulating an overdue loan:")
    print(Loan.overdue_notifications())
    print()


def demo_ratings_and_recommendations():
    """Demonstrate book rating and how it connects with recommendations."""
    print("RATING & RECOMMENDATION DEMO")
    print("=" * 50)

    dune_id = "BK101"
    print("Initial average ratings:", lib.average_ratings)

    print("\nAdding new rating for Dune (BK101) by M1:")
    print(" ", lib.rate_book("M1", dune_id, 5))

    print("Adding another rating for Dune by M3:")
    print(" ", lib.rate_book("M3", dune_id, 4))

    print("\nUpdated averages:", lib.average_ratings)

    print("\nRecommendations for Matthew (M1) after rating Dune:")
    print(" ", lib.recommend_books(member_id="M1", limit=5))
    print()


def demo_library_system_and_persistence():
    """
    Demonstrate the LibrarySystem facade and persistence:
    - Show current counts
    - Save state to disk
    - Clear in-memory data
    - Reload from disk and show that it comes back
    """
    print("LIBRARYSYSTEM & PERSISTENCE DEMO")
    print("=" * 50)

    system = LibrarySystem()
    print("Initial system summary:")
    print(" ", system)

    # Choose a path in the project root for demo persistence
    state_path = Path(project_root) / "demo_state.json"

    print(f"\nSaving state to: {state_path}")
    persistence.save_state(state_path)

    # Clear everything to prove that load_state restores it
    lib.catalog.clear()
    lib.members.clear()
    lib.loans.clear()

    print("\nAfter clearing globals manually:")
    print(" ", system)  # same object, but counts now reflect cleared lists

    print("\nLoading state back from disk...")
    persistence.load_state(state_path)

    print("After load_state:")
    print(" ", system)

    # Optional: export a borrowing report to CSV to show export feature
    report_csv = Path(project_root) / "demo_borrowing_report.csv"
    print(f"\nExporting borrowing report CSV to: {report_csv}")
    persistence.export_borrowing_report_csv(report_csv)

    print("\nPersistence demo complete.\n")


# ------------------------------------------------------------
# MAIN FUNCTION
# ------------------------------------------------------------
def main():
    print("LIBRARY MANAGEMENT SYSTEM - DEMO SCRIPT")
    print("=" * 60)
    print("This demo illustrates how our classes interact with the shared global data.\n")

    setup_sample_data()
    demo_items_and_members()
    demo_search_and_reservations()
    demo_loans_and_reports()
    demo_ratings_and_recommendations()
    demo_library_system_and_persistence()

    print("=" * 60)
    print("DEMO COMPLETE! The library system is fully integrated and functional.")
    print("=" * 60)


if __name__ == "__main__":
    main()