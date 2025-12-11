# Library Management System - API Reference
## This was for project 2 so the information will be outdated

This document lists the public methods and attributes for each major class.

---

## Book Class
**Module:** `src.book_class`

**Constructor:**
```python
Book(item_id, title, author, genre, copies_total)
```
### Attributes:

- `item_id` (str)
- `title` (str)
- `author` (str)
- `genre` (str)
- `copies_total` (int)
- `copies_available` (int)

### Key Methods:

- `check_availability()`
- `add_rating(member_id, rating)`
- `adjust_copies(change)`
- `validate_isbn10()`
- `validate_isbn13()`

## Member Class
**Module:** `src.member_class`

**Constructor:**

```python
Member(member_id, name, email, active=True, tags=None, authors=None)
```

### Attributes:

- `member_id `(str)
- `name` (str)
- `email` (str)
- `active` (bool)
- `balance` (float)
- `loans` (dict)
- `preferences_tags` (set)
- `preferences_authors` (set)

### Key Methods:

- `validate_account()`
- `pay_balance(amount)`
- `borrow_book(item_id)`
- `return_book(item_id)`
- `total_active_members()`

## Search Class
**Module:** `src.search_class`

### Constructor:

```python
Search()
```

### Key Methods:

- `find_books(query)`
- `reserve(member_id, item_id)`
- `manage_waitlist(item_id, member_id, action)`
- `recommend_for_member(member_id, limit)`
- `normalize_query(query)`

## Loan Class
**Module:** `src.loan_class`

**Constructor:**

```python
Loan(member_id, item_id, borrow_date, loan_days)
```

### Attributes:

- `member_id` (str)
- `item_id` (str)
- `borrow_date` (datetime)
- `loan_days` (int)
- `due_date` (datetime)
- `returned` (bool)

### Key Methods:

- `is_overdue()`
- `generate_reports()`
- `calculate_fine()`