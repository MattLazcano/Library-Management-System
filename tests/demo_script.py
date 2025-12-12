"""
Library Management System - Demo Script

This script demonstrates how the library system classes (Lib_item, Member, Search, Loan)
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
            "id": "EB103",
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "genre": "fantasy",
            "media_type": "Ebook",
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
            "id": "DV105",
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "genre": "fiction",
            "media_type": "DVD",
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
def demo_items_and_members(system: LibrarySystem):
    """Demonstrate creation and validation of LibraryItem subclasses and Members via the facade."""
    print("ITEM & MEMBER DEMO")
    print("=" * 50)

    print("Catalog before:", [b["title"] for b in lib.catalog])
    print("Member count before:", len(lib.members))
    print()

    print("Adding new items and member via LibrarySystem facade...\n")
    new_book = system.add_book(
        "BK110",
        "Artificial Intelligence: A Modern Approach",
        "Russell & Norvig",
        "computer science",
        copies_total=5,
    )
    new_ebook = system.add_ebook(
        "EB200", "Python Tricks", "Dan Bader", "programming", copies_total=2
    )
    new_dvd = system.add_dvd(
        "DV300", "The Matrix", "Wachowski", "sci-fi", copies_total=1
    )
    new_member = system.add_member("M6", "Jane Doe", "jane@example.com")

    print(f"Added item: {new_book}")
    print(f"Added item: {new_ebook}")
    print(f"Added item: {new_dvd}")
    print(f"Added member: {new_member}\n")

    print("Catalog after:", [f'{b["id"]} - {b["title"]}' for b in lib.catalog])
    print("Member count after:", len(lib.members))
    print()

    print("Validating one of the new member accounts via Member.validate_account():")
    print("  validate_account(M6) ->", new_member.validate_account())
    print()


def demo_search_and_reservations(system: LibrarySystem):
    """Showcase searching, reserving, waitlists, query normalization, and recommendations via LibrarySystem.search."""
    print("SEARCH & RESERVATION DEMO")
    print("=" * 50)

    s: Search = system.search

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


def demo_loans_and_reports(system: LibrarySystem):
    """Demonstrate borrowing and returning using existing members/books and show reports."""
    print("LOAN & REPORT DEMO")
    print("=" * 50)

    # Before borrowing
    rec = next(r for r in lib.catalog if r["id"] == "EB103")
    print(f"Before borrowing, copies_available for {"EB103"}: {rec['copies_available']}")

    # Borrow EBOOK
    print(f"\nBorrowing {"EB103"} via system.borrow_item('{"M2"}', '{"EB103"}'):")
    borrow_msg = system.borrow_item("M2", "EB103")
    print("  ", borrow_msg)

    rec = next(r for r in lib.catalog if r["id"] == "EB103")
    print(f"After borrowing, copies_available for {"EB103"}: {rec['copies_available']}")

    # Return EBOOK
    print(f"\nReturning {"EB103"} via system.return_item('{"M2"}', '{"EB103"}'):")
    return_msg = system.return_item("M2", "EB103")
    print("  ", return_msg)

    rec = next(r for r in lib.catalog if r["id"] == "EB103")
    print(f"After returning, copies_available for {"EB103"}: {rec['copies_available']}")

    # Show borrowing report
    print("\nBorrowing report after this cycle:")
    report = lib.generate_borrowing_report()
    print("  ", report)
    print()

def demo_ratings_and_recommendations(system: LibrarySystem):
    """Demonstrate rating an item and how that connects with recommendations."""
    print("RATING & RECOMMENDATION DEMO")
    print("=" * 50)

    dune_id = "BK101"
    print("Initial average ratings:", lib.average_ratings)

    print("\nAdding new rating for Dune (BK101) by M1:")
    print(" ", system.rate_item("M1", dune_id, 5))

    print("Adding another rating for Dune by M3:")
    print(" ", system.rate_item("M3", dune_id, 4))

    print("\nUpdated averages:", lib.average_ratings)

    print("\nRecommendations for Matthew (M1) after rating Dune:")
    print(" ", lib.recommend_books(member_id="M1", limit=5))
    print()


def demo_library_system_and_persistence(system: LibrarySystem):
    """
    Demonstrate the LibrarySystem facade and persistence:
    - Show current counts via __str__
    - Save state to disk
    - Clear in-memory data
    - Reload from disk and show that it comes back
    - Export a borrowing report to CSV
    """
    print("LIBRARYSYSTEM & PERSISTENCE DEMO")
    print("=" * 50)

    print("Initial system summary:")
    print(" ", system)

    # Choose a path in the project root for demo persistence
    state_path = Path(project_root) / "/Users/matthewlazcano/Documents/GitHub/Group-5/tests/data/demo_state.json"

    print(f"\nSaving state to: {state_path}")
    persistence.save_state(state_path)

    # Clear everything to prove that load_state restores it
    lib.catalog.clear()
    lib.members.clear()
    lib.loans.clear()

    print("\nAfter clearing globals manually:")
    print(" ", system)  # same LibrarySystem object, but backing data is now empty

    print("\nLoading state back from disk...")
    persistence.load_state(state_path)

    print("After load_state:")
    print(" ", system)

    # Export a borrowing report to CSV to show export feature
    print("\nCSV EXPORT")
    report_csv = Path(project_root) / "/Users/matthewlazcano/Documents/GitHub/Group-5/tests/data/demo_borrowing_report.csv"
    print(f"\nExporting borrowing report CSV to: {report_csv}")
    persistence.export_borrowing_report_csv(report_csv)

    # Import catlog csv file
    print("\nCSV IMPORT")
    csv_path = Path(project_root) / "/Users/matthewlazcano/Documents/GitHub/Group-5/tests/data/sample_catalog_import.csv" 

    print("\nCatalog size BEFORE import:", len(lib.catalog))
    print(f"Importing catalog from: {csv_path}")

    try:
        imported_count = persistence.import_catalog_from_csv(csv_path)
        print(f"Successfully imported {imported_count} new items.")
    except Exception as e:
        print("Import failed:", e)
        return

    print("Catalog size AFTER import:", len(lib.catalog))

    # Show a preview of the last imported items
    print("\nRecently imported items:")
    for item in lib.catalog[-imported_count:]:
        print(f"  {item['id']}: {item['title']} ({item['media_type']})")

    print()

    print("\nPersistence demo complete.\n")


# ------------------------------------------------------------
# MAIN FUNCTION
# ------------------------------------------------------------
def main():
    print("LIBRARY MANAGEMENT SYSTEM - DEMO SCRIPT")
    print("=" * 60)
    print("This demo illustrates how LibrarySystem and our classes\n"
        "interact with the shared global data and persistence layer.\n")

    system = LibrarySystem()

    setup_sample_data()
    demo_items_and_members(system)
    demo_search_and_reservations(system)
    demo_loans_and_reports(system)
    demo_ratings_and_recommendations(system)
    demo_library_system_and_persistence(system)

    print("=" * 60)
    print("DEMO COMPLETE! The library system is fully integrated and functional.")
    print("=" * 60)


if __name__ == "__main__":
    main()