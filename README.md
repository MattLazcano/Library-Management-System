# Library Management System — INST326 Project 4

**Group 5 — Matthew Lazcano, Rood Codet, Kaliza, Abinash Subedi**

---

## Project Overview

This project is a fully integrated Library Management System designed for INST326.
Our domain is Library and Information Management, and our goal was to build a system that can:

* store and manage catalog items (books, e-books, DVDs),
* manage members and their accounts,
* process borrowing and returning,
* handle waitlists and reservations,
* maintain ratings and recommendations,
* generate reports on borrowing activity,
* persist data across program runs.

Across Projects 1–4, we evolved a simple function-based system into a fully modular OOP architecture using shared global state, polymorphic LibraryItem subclasses, wrapped domain classes, and complete data persistence.

---

## Features

* Global shared data structures for catalog, members, loans, waitlists, ratings
* OOP classes: LibraryItem, BookItem, EBookItem, DVDItem, Member, Loan, Search, LibrarySystem
* Borrow/return operations with due dates and overdue detection
* Automatic waitlist handling when items are unavailable
* Ratings + recommendation engine based on tags/history
* Borrowing reports + overdue notifications
* Save/load full system state to JSON
* CSV export of borrowing summary
* Comprehensive unit, integration, and system tests

---

## Setup & Installation

1. Clone this repository:
```python
git clone https://github.com/MattLazcano/Library-Management-System
cd Group-5
```

2. Ensure Python 3.10+ is installed.

3. No external dependencies are required — the system uses only standard library modules.

---

## Basic Usage Example

Below is a minimal example of how to use the system:
```python
from src.library_system import LibrarySystem

sys = LibrarySystem()

# Add items
sys.add_book("BK101", "Dune", "Frank Herbert", "sci-fi", copies_total=3)
sys.add_ebook("EB200", "Python Tricks", "Dan Bader", "programming")
sys.add_dvd("DV300", "The Matrix", "Wachowski", "sci-fi")

# Add member
m = sys.add_member("M1", "Matthew", "m@example.com")

# Borrow a book
print(m.borrow_book("BK101"))

# Return it
print(m.return_book("BK101"))

# Search
results = sys.search.find_books(query="dune")
print(results)

# Save system state
sys_state = "state.json"
sys.save_state(sys_state)

# Load system state
sys.load_state(sys_state)
```

For a full demonstration, run:
```python
python demo/demo_script.py
```

---

## Running Tests

All tests use the unittest framework.

Run the full test suite:
```python
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Video Presentation

(Insert video link here — YouTube or Google Drive)


## Team Member Contributions

---

### Matthew Lazcano — Lead Developer, Systems Architect & Integration Engineer

* Directed the system architecture across all four projects, ensuring consistent design and functional integration
* Implemented and refined major domain classes (BookItem, EBookItem, DVDItem, Member, Search, Loan) and coordinated their interaction with the shared global data model
* Led the migration from a function-only system to a fully integrated OOP architecture with polymorphism, composition, and standardized item records
* Designed and implemented the persistence layer, including save_state, load_state, CSV import/export features, and error-handling mechanisms
* Performed extensive debugging and refactoring to ensure all unit, integration, and system tests passed successfully
* Created the demo script, sample datasets, and presentation walkthrough showcasing core workflows, recommendations, overdue notifications, and persistence
* Organized repository structure, enforced coding standards, resolved merge conflicts, and ensured project completeness
* Acted as primary integrator, connecting all team components into a cohesive, functional system

---

### Abinash Subedi — Project Coordinator, Function Developer & Presentation Lead

* Managed team communication, deadlines, meeting structure, and task distribution throughout the multi-week development cycle
* Expanded and refined core functional modules such as reserve_book, rate_book, validate_code, validate_isbn10_format, validate_isbn13_format, and generate_borrowing_report
* Contributed significantly to the design of the Search class by integrating it with global functions and extending support for features like query normalization and filtering
* Assisted in persistence planning and helped connect reporting structures with export features used in Project 4
* Led the presentation script drafting for domain requirements, system design, and architectural rationale
* Helped shape early architecture decisions and ensured consistent alignment with the team charter

---

### Kaliza Mvunganyi — Member System Developer, Workflow Logic Engineer

* Designed and implemented the upgraded Member class and its end-to-end borrowing and returning workflows
* Authored critical system functions: calculate_due_date, member_count, check_in_out_operations, and waitlist_management, ensuring synchronization with catalog state and loan operations
* Improved data validation, error handling, and edge-case logic for account management and borrowing rules
* Provided reliable and consistently correct code that required minimal revision, supporting integration stability
* Participated in testing effort, verifying correct behavior of member workflows, waitlists, overdue logic, and user rules
* Contributed to the video demo preparation by helping validate workflows shown on screen

---

### Rood Cadet — Loan System Developer, Recommendation Logic & Testing Assistant

* Developed core components of the Loan class, including due-date calculations, overdue checks, and reporting hooks
* Authored major supporting functions: format_search_query, user_account, and recommend_books, enabling the recommendation engine and unified account operations
* Participated in shaping the text-processing and token-normalization logic of the search system
* Assisted in the creation and refinement of the integration test scenarios and validated the final end-to-end behavior
* Contributed to conceptual architecture discussions and supported debugging during integration phases
* Helped test recommendation scoring, overdue notifications, and borrowing rules in preparation for the final demo