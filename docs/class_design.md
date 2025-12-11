# Library Management System - Class Design Documentation
## This was for project 2 so the information will be outdated


This document describes the architecture and relationships between the classes in the Library Management System.

---

## Overview

The system uses an **object-oriented architecture** with shared global data structures (`catalog`, `members`, `loans`, `reservations`, `waitlists`, `ratings`, `average_ratings`, `reminders`) defined in `library_functions.py`.  
Each class interacts with these structures to ensure all operations are synchronized across the system.

---

## Class Overview

| Class | Primary Role | Interacts With |
|:------|:--------------|:----------------|
| **Item** | Represents a single library item and manages copies, metadata, and ratings | `catalog`, `ratings`, `average_ratings` |
| **Member** | Represents a library user with balance, preferences, and loan records | `members` |
| **Search** | Handles catalog lookups, recommendations, and waitlist operations | `catalog`, `members`, `waitlists`, `reservations` |
| **Loan** | Manages borrowing activity and overdue calculations | `loans` |

---

## Class Relationships

- Each **Book** object registers itself in the global catalog upon creation.  
- Each **Member** object is added to the `members` dictionary and may hold active **Loan** objects.  
- The **Search** class reads the `catalog` and `members` structures to return matches and generate recommendations.  
- **Loan** objects reference both the member and book IDs for tracking purposes.

---

## Object Interaction Diagram (Textual Form)

Member ─── borrows ───► Loan ─── references ───► Book                                                                                  
▲                                                                                                                                                 
└────────── interacts with Search ──────────┘


---

## Design Principles

- **Encapsulation:** Each class maintains its own internal state (e.g., copies, balance).
- **Abstraction:** Classes expose clean, high-level methods such as `borrow_book()` or `rate_book()`.
- **Reusability:** Functions in `library_functions.py` are shared utilities across all classes.
- **Data Consistency:** Global structures ensure all operations reflect system-wide state.

---

## Example Data Flow

1. A `Book` is created → added to `catalog`.  
2. A `Member` borrows it → `Loan` is created and added to `loans`.  
3. Book copies decrease → due date assigned → notifications handled via `library_functions`.  
4. When returned, availability updates system-wide.
