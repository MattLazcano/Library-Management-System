# Library Management System - Function Reference Guide

This document provides comprehensive reference information for all core functions in **library_functions.py**.  
These functions power the backend logic of the Library Management System, handling cataloging, membership, loans, search, recommendations, and overdue processing.

---

## Table of Contents

1. [Global Data Structures](#global-data-structures)
2. [Book and Availability Functions](#book-and-availability-functions)
3. [Member and Loan Management Functions](#member-and-loan-management-functions)
4. [Search, Reservation, and Waitlist Functions](#search-reservation-and-waitlist-functions)
5. [Ratings and Validation Functions](#ratings-and-validation-functions)
6. [Reports and Notifications](#reports-and-notifications)
7. [Utility and Recommendation Functions](#utility-and-recommendation-functions)

---

## Global Data Structures

All functions in the system rely on a shared global state for data consistency across classes and operations.

| Name | Type | Description |
|:------|:------|:-------------|
| `catalog` | `list[dict]` | Stores all book records with metadata and copy counts |
| `members` | `dict` | Stores member information indexed by ID |
| `loans` | `list[dict]` | Tracks loan transactions and due dates |
| `reminders` | `list[dict]` | Holds scheduled reminder messages |
| `reservations` | `dict` | Maps members to their reserved book IDs |
| `waitlists` | `dict` | Maps book IDs to lists of waiting member IDs |
| `ratings` | `dict` | Holds per-member ratings for each book |
| `average_ratings` | `dict` | Stores average rating per book |

These shared structures ensure that all classes (`Book`, `Member`, `Search`, and `Loan`) access the same up-to-date library state.

---

## Book and Availability Functions

### is_book_available(title)

**Purpose:** Check if a book is currently available in the catalog.  
**Parameters:**
- `title` (str): The title of the book to check.  
**Returns:** `bool` — True if at least one copy is available.

**Example Usage:**
```python
available = is_book_available("Dune")
print(available)  # True if Dune has copies_available > 0
```

### schedule_reminder(member_id, item_id, due_date)

**Purpose:** Schedule a reminder message for a member’s borrowed book.  
**Parameters:**
- `member_id` (str): The member’s ID.
- `item_id` (str): The book’s ID.
- `due_date` (datetime): The due date for the borrowed item.  
**Returns:** `bool` — True if reminder was added successfully.

**Example Usage:**
```python
from datetime import datetime, timedelta
schedule_reminder("M1", "1000000001", datetime.now() + timedelta(days=14))
# Adds reminder to global reminders list
```

## Member and Loan Management Functions

### calculate_due_date(borrow_date, loan_days=14, skip_weekends=True)

**Purpose:** Calculate a due date for a borrowed book, optionally skipping weekends.  
**Parameters:**
- `borrow_date` (datetime): The borrow date.
- `loan_days` (int): Number of loan days (default 14).
- `skip_weekends` (bool): Skip Saturdays and Sundays (default True).  
**Returns:** `datetime` — Computed due date.

**Example Usage:**
```python
from datetime import datetime
due = calculate_due_date(datetime.now())
print("Due date:", due)
```

### member_count(active_only=True)

**Purpose:** Count the total number of registered library members.  
**Parameters:**
- `active_only` (bool): Whether to count only active members (default True).  
**Returns:** `int` — Number of members.

**Example Usage:**
```python
print("Active members:", member_count())
```

### check_in_out_operations(user_id, isbn, action='borrow', loan_days=14)

**Purpose:** Manage the borrowing or returning of books.  
**Parameters:**
- `user_id` (str): The member performing the transaction.
- `isbn`( str): Book ID.
- `action` (str): 'borrow' or 'return'.
- `loan_days` (int): Length of the loan in days (default 14).  
**Returns:** `dict` — Details of the operation.

**Example Usage:**
```python
check_in_out_operations("M1", "1000000003", "borrow")
check_in_out_operations("M1", "1000000003", "return")
```

## Search, Reservation, and Waitlist Functions

### search_catalog(query='', author='', genre='', available=None)

**Purpose:** Search the catalog for books by keyword, author, or genre.  
**Parameters:**
- `query` (str): Keyword in title or author.
- `author` (str): Filter by author name.
- `genre` (str): Filter by genre.
- `available` (bool): True for available only, False for unavailable, None for all.  
**Returns:** list[dict] — Matching book entries.

**Example Usage:**
```python
results = search_catalog(query="Code")
for r in results:
    print(r["title"], "-", r["author"])
```

### reserve_book(member_id, item_id)

**Purpose:** Reserve a book for a member or add them to the waitlist if unavailable.  
**Parameters:**
- `member_id` (str): The member’s ID.
- `item_id` (str): The book’s ID.  
**Returns:** str — Confirmation message.

**Example Usage:**
```python
msg = reserve_book("M3", "1000000002")
print(msg)
# Output: "No copies available. Member 'M3' added to the waitlist..."
```

### waitlist_management(isbn, user_id, action='add')

**Purpose:** Manage a book’s waitlist by adding or notifying users.  
**Parameters:**
- `isbn` (str): Book ID.
- `user_id` (str): Member ID.
- `action` (str): 'add' or 'notify'.  
**Returns:** dict — Updated waitlist information or notification details.

**Example Usage:**
```python
print(waitlist_management("1000000001", "M4", "add"))
print(waitlist_management("1000000001", "M4", "notify"))
```

## Ratings and Validation Functions

### rate_book(member_id, item_id, rating)

**Purpose:** Record and calculate average book ratings.  
**Parameters:**
- `member_id` (str)
- `item_id` (str)
- `rating` (int, 1–5)  
**Returns:** str — Message confirming update and average.

**Example Usage:**
```python
msg = rate_book("M1", "1000000001", 5)
print(msg)
# "Rated book '1000000001' with 5 stars. Average now: 5.0"
```

### validate_code(code_input)

**Purpose:** Validate whether a string is a valid ISBN or library ID.  
**Parameters:**
- `code_input` (str): Book code to validate.  
**Returns:** bool — True if valid format.
**Raises:** TypeError if input is not a string.

**Example Usage:**
```python
print(validate_code("1000000001"))  # True for valid library IDs
print(validate_code("9780132350884"))  # True for valid ISBN-13
```

### validate_isbn10_format(isbn_code)

**Purpose:** Validate checksum for a 10-digit ISBN.  
**Parameters:**
- `isbn_code` (str): ISBN-10 code.  
**Returns:** bool — True if checksum passes.

**Example Usage:**
```python
print(validate_isbn10_format("0306406152"))  # True if valid ISBN-10
```

### validate_isbn13_format(isbn_code)

**Purpose:** Validate checksum for a 13-digit ISBN.  
**Parameters:**
- `isbn_code` (str): ISBN-13 code.  
**Returns:** bool — True if valid.

**Example Usage:**
```python
print(validate_isbn13_format("9780306406157"))  # True if valid ISBN-13
```

## Reports and Notifications

### generate_borrowing_report(fine_per_day=0.5)

**Purpose:** Generate a statistical report summarizing borrowing activity and fines.  
**Parameters:**
- `fine_per_day` (float): Late fee per day.  
**Returns:** dict — Borrowing statistics.

**Example Usage:**
```python
report = generate_borrowing_report()
print(report["total_books_borrowed"], "books borrowed in total")
```

### automated_overdue_notifications(today=None, daily_fee=0.25, grace_days=0)

**Purpose:** Identify overdue books, calculate fees, and create overdue messages.  
**Parameters:**
- `today` (datetime, optional): Reference date for checking overdue items.
- `daily_fee` (float): Daily fine per day overdue.
- `grace_days` (int): Days allowed past due date before fine applies.  
**Returns:** dict — Overdue summary report.

**Example Usage:**
```python
notifications = automated_overdue_notifications()
print(notifications["total_overdue_items"], "items overdue.")
```

## Utility and Recommendation Functions

### format_search_query(q)

**Purpose:** Normalize and tokenize a user’s search query string.  
**Parameters:**
- `q` (str): The search input.  
**Returns:** `dict` — Contains:
    - `original`: Original query
    - `normalized`: Cleaned lowercase string
    - `tokens`: List of keywords

**Example Usage:**
```python
query = format_search_query('"data science" in modern AI')
print(query["tokens"])  # ['modern', 'ai', 'data science']
```

### user_account(action, user_id=None, isbn=None, ...)

**Purpose:** Manage basic user account operations such as borrowing, returning, validating, or paying balances.  
**Parameters:**
- `action` (str): One of `'validate'`, `'borrow'`, `'return'`, `'pay'`.
- Other optional parameters depending on action.  
**Returns:** `dict` — Summary of the account action.

**Example Usage:**
```python
user_account(action="borrow", user_id="M1", isbn="1000000003")
user_account(action="return", user_id="M1", isbn="1000000003")
user_account(action="pay", user_id="M1", pay_amount=5.00)
```

### recommend_books(member_id, limit=10)

**Purpose:** Recommend books based on a user’s history, preferences, and tag similarity.  
**Parameters:**
- `member_id` (str): Member ID to recommend for.
- `limit` (int): Maximum number of results (default 10).  
**Returns:** `list[tuple]` — List of `(item_id, score)` ranked by recommendation strength.

**Example Usage:**
```python
recommendations = recommend_books(member_id="M1", limit=5)
for book, score in recommendations:
    print(f"{book}: {score:.2f}")
```
