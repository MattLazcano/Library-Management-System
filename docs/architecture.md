# Library Management System – Architecture Diagram

## Complete System Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          ABSTRACT BASE LAYER                             │
│                     (Defines Interface Contracts)                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────────────────────┐                                       │
│  │        LibraryItem (ABC)      │                                       │
│  ├───────────────────────────────┤                                       │
│  │ + item_id                     │                                       │
│  │ + title                       │                                       │
│  │ + author                      │                                       │
│  │ + genre                       │                                       │
│  │                                                                       │
│  │ @property (abstract)          │                                       │
│  │ + media_type()                │                                       │
│  │                                                                       │
│  │ @abstractmethod               │                                       │
│  │ + calculate_loan_period()     │  ← Polymorphic behavior               │
│  │                                                                       │
│  │ (concrete)                    │                                       │
│  │ + describe()                  │                                       │
│  │ + due_date_for(checkout_date) │                                       │
│  └───────────────────────────────┘                                       │
│                       ▲                                                  │
│                       │ inherits                                         │
└───────────────────────┼──────────────────────────────────────────────────┘
                        │
┌───────────────────────┼──────────────────────────────────────────────────┐
│                       │      CONCRETE IMPLEMENTATION LAYER               │
│                       │       (Inheritance & Polymorphism)               │
├───────────────────────┴──────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐     │
│   │      Book        │   │      EBook       │   │       DVD        │     │
│   ├──────────────────┤   ├──────────────────┤   ├──────────────────┤     │
│   │ media_type=Book  │   │ media_type=EBook │   │ media_type=DVD   │     │
│   │ loan → 21 days   │   │ loan → 14 days   │   │ loan → 7 days    │     │
│   │ describe()       │   │ describe()       │   │ describe()       │     │
│   └──────────────────┘   └──────────────────┘   └──────────────────┘     │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ used by
                                  ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                         COMPOSITION LAYER                                 │
│                        (System Coordination)                              │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   ┌─────────────────────────────────────────────────────────────────┐     │
│   │                            Catalog                              │     │
│   ├─────────────────────────────────────────────────────────────────┤     │
│   │ + _items {}  ◄──────────── HAS-MANY LibraryItem objects         │     │
│   │                                                                 │     │
│   │ + add_item(item)                                                │     │
│   │ + get_item(id)                                                  │     │
│   │ + all_items()                                                   │     │
│   │ + search(query, author, genre)                                  │     │
│   └─────────────────────────────────────────────────────────────────┘     │
│                                    │                                      │
│                                    │ used by                              │
│                                    ▼                                      │
│   ┌─────────────────────────────────────────────────────────────────┐     │
│   │                              Search                             │     │
│   ├─────────────────────────────────────────────────────────────────┤     │
│   │ + _catalog  ◄────────────── composition: Search HAS-A Catalog   │     │
│   │ + _members                                                      │     │
│   │ + _reservations                                                 │     │
│   │ + _waitlists                                                    │     │
│   │                                                                 │     │
│   │ + find_books()                                                  │     │
│   │ + reserve()                                                     │     │
│   │ + manage_waitlist()                                             │     │
│   │ + recommend_for_member()                                        │     │
│   │ + normalize_query()                                             │     │
│   └─────────────────────────────────────────────────────────────────┘     │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

## Key Relationships

### INHERITANCE (is-a)
- **Book is-a LibraryItem**
- **EBook is-a LibraryItem**
- **DVD is-a LibraryItem**

### COMPOSITION (has-a)
- **Catalog has-many LibraryItem objects**
- **Search has-a Catalog**
- **Search has-a reference to members, reservations, and waitlists**

### POLYMORPHISM
Each subclass implements `calculate_loan_period()` differently:
- Book → 21 days  
- EBook → 14 days  
- DVD → 7 days  

## Data Flow Example

```
1. System creates Catalog
   └─→ Catalog._items = {}

2. System loads LibraryItem subclasses
   └─→ catalog.add_item(Book("B1", ...))
   └─→ catalog.add_item(EBook("E1", ...))
   └─→ catalog.add_item(DVD("D1", ...))

3. User performs a search
   └─→ Search.find_books()
       └─→ Catalog.search()

4. User reserves items
   └─→ Search.reserve()
       └─→ calls library_functions.reserve_book()

5. System calculates due dates
   └─→ LibraryItem.due_date_for()
       └─→ uses polymorphic loan periods

6. System prints summaries
   └─→ summarize_items()
       └─→ item.describe()
```

## Why This Architecture Works

### Abstract Layer Benefits
✓ Enforces consistent interfaces  
✓ Prevents incomplete objects  
✓ Ensures every item defines loan‑period logic  

### Concrete Layer Benefits
✓ Specialized formats (Book, EBook, DVD)  
✓ Polymorphism simplifies system code  
✓ Easy to add new item types later  

### Composition Layer Benefits
✓ Catalog organizes many LibraryItem objects  
✓ Search interacts with Catalog + members + waitlists  
✓ Flexible, realistic relationships  

## Design Pattern Summary

| Pattern | Where Used | Why |
|--------|------------|------|
| **Abstract Base Class** | LibraryItem | Enforces interface |
| **Inheritance** | Book/EBook/DVD | Shared interface, specialized behavior |
| **Polymorphism** | calculate_loan_period() | Dynamic behavior |
| **Composition** | Catalog, Search | Proper “has‑a” structure |
| **Template Method** | due_date_for() | Algorithm depending on subclass |