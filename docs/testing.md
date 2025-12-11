# Testing Documentation

---

## Testing Strategy Overview

Our test suite includes unit, integration, and system-level tests, covering:

### Unit Tests

Test individual classes and functions in isolation:

* ID validation (validate_code)
* loan period polymorphism (calculate_loan_period)
* member registration and account validation
* search functionality
* rating updates and averages
* report generation building correct structures

### Integration Tests

Verify components working together:

* borrowing → loan record → copies_available update
* return flow → overdue handling
* waitlist integration via reserve_book + waitlist_management
* recommendations combining tags, authors, and loan history
* persistence save/load restoring catalog/members/loans

### System Tests

Full workflows (end-to-end):

* Add item → add member → borrow → return → verify counts
* Borrow item → add to waitlist → notify overdue → generate report
* Save entire system → clear state → reload → system continues functioning

### Persistence Tests

Verify that the system correctly saves and restores data:

* save/load keeps catalog, members, and loans consistent
* round-trip tests confirm copies_available, balances, and loan dates remain accurate
* CSV export creates a valid borrowing-report file with expected fields
* end-to-end workflow still works after a full save, reset, and reload

---

## Coverage Rationale

We focused testing on:

* shared globals (catalog, members, loans)
* high-risk workflows (borrowing/return, waitlists)
* data correctness (copies_available, fines, due dates)
* persistence integrity (round-trip load/save)
* business rules (availability checks, duplicate borrow prevention)

---

## How to Run the Test Suite

From the project root:
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test Results Summary

All required tests pass, including:

* Unit tests for core functions and classes
* Integration tests validating cross-module behavior
* System-level tests confirming end-to-end workflows
* Persistence tests demonstrating correct save/load behavior

Test output confirms that the system is coherent, stable, and behaves correctly under expected scenarios.