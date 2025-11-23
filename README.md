# Library Management System - Function Library

**Team:** Group 5  
**Domain:** Library and Information Management  
**Course:** INST326 - Object-Oriented Programming for Information Science  

---

## Project Overview

Our Library Management System is a fully integrated object-oriented platform designed across Projects 1, 2, and 3.
It combines:
- Global function library (Project 1)
- Encapsulated domain classes (Project 2)
- Inheritance hierarchy, polymorphism, and composition (Project 3)
The system manages:
- Catalog and library item metadata
- Members and account management
- Loans, due dates, and overdue checks
- Search, recommendations, and waitlist operations
- Polymorphic loan-period logic for different media types
All components operate as one cohesive architecture, where global structures maintain shared data, and classes provide a clean, reusable, object-oriented interface.

---

## Problem Statement

Libraries face common challenges with:

- Tracking books, members, and active loans in a consistent way  
- Managing availability and waitlists for popular titles  
- Recommending books based on user preferences and history  
- Processing checkouts, returns, and overdue notifications  
- Organizing a consistent catalog of metadata and ratings  

Our system addresses these by maintaining **global shared data structures** that all classes interact with — ensuring that catalog, member, and loan information stay synchronized throughout every operation.

---

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/library-management-system.git
   cd library-management-system
2. **No external dependencies required** — the project uses only the Python Standard Library.

3. **Import classes or functions in your code:**

```python
from src.book_class import Book
from src.member_class import Member
from src.search_class import Search
from src.loan_class import Loan
from src import library_functions as lib
```
## Key Relationships
### Inheritance (is-a)
- Book is a LibraryItem
- EBook is a LibraryItem
- DVD is a LibraryItem

These subclasses override `calculate_loan_period()` — the system uses polymorphism so each item type behaves differently using the same interface.

### Composition (has-a / has-many)
- Catalog HAS-MANY LibraryItems
- Search HAS-A Catalog
- Loan HAS-A member_id & book_id reference
- Member data stored in global members structure
Composition allows flexible coordination without unnecessary inheritance.

### Polymorphism
The same method behaves differently depending on media type:
| Media Type | Loan Period | Polymorphic Behavior                 |
| ---------- | ----------- | ------------------------------------ |
| Book       | 21 days     | `calculate_loan_period()` returns 21 |
| E-Book     | 14 days     | Returns 14                           |
| DVD        | 7 days      | Returns 7                            |

Any LibraryItem can be passed to functions like:
```item.due_date_for(today)```
and the correct subclass logic runs automatically.

## Quick Usage Examples
### Creating Items (Inheritance Demo)
``` python
from src.library_items import Book, EBook, DVD

b = Book("B1", "Dune", "Frank Herbert", "Sci-Fi")
e = EBook("E1", "Digital Literacy", "Smith", "Education")
d = DVD("D1", "The Matrix", "Wachowski", "Sci-Fi")
```

### Catalog + Search (Composition Demo)
```python
from src.catalog import Catalog
from src.search_class import Search

catalog = Catalog()
catalog.add_item(b)
catalog.add_item(e)
catalog.add_item(d)

s = Search(catalog)
results = s.find_books(query="dune")
```

### Reserving and Waitlisting
```python
print(s.reserve("M1", "1000000002"))
print(s.manage_waitlist("1000000001", "M4", "add"))
```

### Loan Polymorphism Demo
```python
from datetime import date

for item in catalog.all_items():
    print(item.describe(), "=>", item.due_date_for(date.today()))
```

### Ratings
```python
print(lib.rate_book("M1", "1000000001", 5))
print(lib.rate_book("M3", "1000000001", 4))
print(lib.average_ratings)
```


## Function Library Overview
The function library contains over 20 integrated utilities, organized across four main domains:

### Book Management
- `validate_code()` — Ensures valid book ID or ISBN format

- `is_book_available()` — Checks catalog for availability

- `rate_book()` — Adds and averages user ratings

- `update_catalog()` — Adds new book records to the global catalog

### Member Management
- `add_member()` — Adds new library members

- `update_member_balance()` — Adjusts user account balances

- `get_active_members()` — Lists all currently active members

- `pay_balance()` — Simulates payment processing

### Search and Recommendation
- `search_catalog()` — Keyword, author, and genre search

- `reserve_book()` — Places a member on a waitlist or reserves a copy

- `waitlist_management()` — Adds/removes users from waitlists

- `recommend_books()` — Recommends titles based on preferences and tags

### Loan and Reporting
- `calculate_due_date()` — Generates loan due dates

- `generate_borrowing_report() — Summarizes borrowing statistics

- `automated_overdue_notifications()` — Simulates overdue alerts

## Object-Oriented Design
The system includes four main classes that encapsulate these functions and maintain consistent state across all operations:

| Class | Responsibility | Connected Global Structures |
|:------|:----------------|:-----------------------------|
| **Book** | Represents a single library item and its availability, ratings, and metadata | `catalog`, `average_ratings` |
| **Member** | Represents an individual user, tracks balance, preferences, and loans | `members` |
| **Search** | Handles catalog search, reservations, and recommendation features | `catalog`, `members`, `waitlists` |
| **Loan** | Tracks borrowing, due dates, and overdue status | `loans` |

Each class interacts directly with shared global data structures imported from `library_functions`, ensuring all updates are reflected system-wide.

## Project 3 File Overview

Project 3 extended our library system by adding inheritance, polymorphism, abstract classes, and composition.  
Here is a basic overview of the major files created or updated:


### `library_items.py`

Defines the new inheritance hierarchy for library materials.

- `LibraryItem` (abstract base class)
- `Book`, `EBook`, `DVD` subclasses  
  Each subclass overrides `calculate_loan_period()`, giving us polymorphism.


### `catalog.py`

Implements composition.

- The `Catalog` has many `LibraryItem` objects.
- Supports adding items and simple searching.

This helps organize items without relying only on global data.


### `search_class.py` (updated)

Now uses composition by including a `Catalog` object inside.  
It also connects the new item system to our old global functions like:

- `reserve_book`
- `waitlist_management`
- `recommend_books`

This makes the system unified.


### Demo / Polymorphism Test

Shows that different item types return different values using the same method call, e.g.:

- Books: 21-day loan
- EBooks: 14-day loan
- DVDs: 7-day loan

This proves polymorphism is working.


## Team Member Contributions
### Matthew Lazcano — Lead Developer & Project Integrator
- Led the overall development, integration, and debugging of the system
- Managed GitHub repository, version control, and final code implementation
- Designed and implemented the `Book`, `Member`, `Search`, and `Loan` classes
- Oversaw function integration, testing, and demo script creation
- Coordinated bug fixes, code validation, and system synchronization

### Abinash Subedi — Project Coordinator & Function Developer
- Ensured team coordination by organizing meetings, managing deadlines, and maintaining communication
- Contributed to the development of the `Search` class and core functions including:
`reserve_book`, `rate_book`, `validate_code`, `validate_isbn10_format`, `validate_isbn13_format`, and `generate_borrowing_report`
- Provided leadership and accountability throughout the project timeline

### Kaliza Mvunganyi — Member System Developer
- Developed the `Member` class with well-structured methods and reliable functionality
- Authored key supporting functions: `calculate_due_date`, `member_count`, `check_in_out_operations`, and `waitlist_management`
- Consistently delivered accurate and on-time code submissions with minimal revision needed

### Rood Cadet — Function Contributor
- Contributed in making the `Loan` class and several functional components
- Authored functions including: `format_search_query`, `user_account`, and `recommend_books`
- Assisted in conceptual discussions and provided testing support during development phases