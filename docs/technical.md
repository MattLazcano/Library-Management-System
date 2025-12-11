# Technical Documentation

---

## System Architecture Overview

The system is organized around shared global state and object-oriented interfaces.

### 1. Global Function Library (library_functions.py)

This module stores:

* catalog — list of dictionaries describing all items
* members — dictionary of member profiles
* loans — list of loan dictionaries
* ratings, average_ratings — rating engine data
* helper functions used everywhere (searching, borrowing logic, reporting, recommendations)

This acts as the single source of truth for all system data.

### 2. LibraryItem Hierarchy
```python
LibraryItem (abstract)
 ├── BookItem
 ├── EBookItem
 └── DVDItem
```

Each subclass:

* validates IDs (BK###, EB###, DV###)
* auto-registers itself into the global catalog
* defines media_type
* overrides calculate_loan_period() (21/14/7 days)
* provides consistent polymorphic behavior to anything that handles items

### 3. Domain Wrapper Classes

**Member**

Wraps all user-account behavior:

* borrow/return via check_in_out_operations
* pay balance via user_account
* auto-registers into global members dictionary

**Loan**

Represents a single borrowing event:

* stores borrow date and due date
* appends record into global loans
* supports overdue calculation
* provides report + notification helpers

**Search**

Wraps catalog-searching + reservations + waitlists + recommendations.

### 4. LibrarySystem (Facade Layer)

This is the high-level interface for end-to-end workflows.
It provides:

* add_book, add_ebook, add_dvd
* add_member
* create_loan
* save_state / load_state
* export_borrowing_report_csv

It owns a Search instance (composition) and exposes clean methods for external users.

---

## Key Design Decisions

**Keep global data as the authoritative state**

Avoids duplication of catalog/member/loan data in each class.

**Classes wrap global logic rather than re-implement it**

Preserves compatibility with earlier project work.

**Use polymorphism for loan periods**

Allows the system to use item types interchangeably.

**Use JSON for persistence**

Simple, human-readable, and supports nested structures.

**Category-based ID system (BK101, EB200, DV300)**

Removes ISBN complexity while enforcing structure.

---

## Known Limitations / Future Enhancements

* No GUI; interaction is terminal or scripts.
* Concurrency (multiple users simultaneously) not supported.
* CSV import currently handles catalog items but not member/loan history.
* Future versions could integrate a database instead of globals.