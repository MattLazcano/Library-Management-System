# Main function library (fully flattened version — no class wrapper)
from datetime import datetime, timedelta, timezone
from collections import defaultdict, Counter
import re, unicodedata
from decimal import Decimal, ROUND_HALF_UP

# -------------------------------------
# Global Data Structures
# -------------------------------------
catalog = []         # list of {"id","title","author","genre","media_type", "tags", "copies_total","copies_available"}
members = {}         # dict of member_id: {"name","email","phone"}
reminders = []       # list of {"member_id","item_id","due_date", "message"}
loans = []           # list of {"member_id","item_id","loan_date","due_date","returned": bool}
reservations = {}    # member_id -> list of item_ids
ratings = {}         # item_id -> {member_id: rating}
average_ratings = {} # item_id -> average_rating


# ----------------------------------------------------
# SIMPLE function (5-10 lines) BOOK AVAILABILITY CHECK (Matthew)
# ----------------------------------------------------
def is_book_available(title):
    t = title.strip().lower()
    for item in catalog:
        if item["title"].strip().lower() == t:
            return item["copies_available"] > 0
    return False


# ----------------------------------------------------
# SIMPLE function (5-10 lines) Reminder Scheduling (Matthew)
# ----------------------------------------------------
def schedule_reminder(member_id, item_id, due_date):
    if member_id in members and any(b["id"] == item_id for b in catalog):
        message = f"Reminder: Item ID {item_id} is due on {due_date}."
        reminders.append({"member_id": member_id, "item_id": item_id, "due_date": due_date, "message": message})
        return True
    return False


# ----------------------------------------------------
# MEDIUM (15–25 lines) Search and Filter Catalog (Matthew)
# ----------------------------------------------------
def search_catalog(query: str = "", author: str = "", genre: str = "", available: bool = None):
    results = []
    q = query.strip().lower()
    a = author.strip().lower()
    g = genre.strip().lower()
    
    for item in catalog:
        title_match = (q in item["title"].strip().lower()) or (q in item["author"].strip().lower()) if q else True
        author_match = a in item["author"].strip().lower() if a else True
        genre_match = (g == item["genre"].strip().lower()) if g else True
        availability_match = (item["copies_available"] > 0) if available is True else (item["copies_available"] == 0) if available is False else True

        if title_match and author_match and genre_match and availability_match:
            results.append(item)
    return results


# ----------------------------------------------------
# COMPLEX (30+ lines) Automated Overdue Notifications (Matthew)
# ----------------------------------------------------
def automated_overdue_notifications(today: datetime | None = None, daily_fee: float = 0.25, grace_days: int = 0):
    if today is None:
        today = datetime.now().date()
    cutoff_date = today - timedelta(days=grace_days)

    messages = [] # list of {"member_id", "message", "fee"}  
    total_overdue_items = 0
    notified_member_ids = set()

    for loan in loans:
        if loan["returned"]:
            continue
        due_date = loan["due_date"]
        if not isinstance(due_date, datetime):
            continue
        due_date_only = due_date.date()
        if due_date_only >= cutoff_date:
            continue

        book = None
        for b in catalog:
            if b["id"] == loan["item_id"]:
                book = b
                break
        title = book.get("title","Unknown Title") if book else str(loan["item_id"])

        member = members.get(loan["member_id"], {"name": "Member"})
        member_id = loan["member_id"]

        days_overdue = (today - due_date_only).days
        fee = max(0, days_overdue) * daily_fee
        total_overdue_items += 1
        notified_member_ids.add(member_id)

        text = (
            f"Hello {member.get('name','Member')}, "
            f"'{title}' is overdue by {days_overdue} day(s). "
            f"Estimated fee so far: ${fee:.2f}. "
            f"Due date was {due_date.date()}. Please return or renew."
        )
        messages.append({"member_id": member_id, "text": text, "fee": round(fee, 2)})

    return {
        "total_overdue_items": total_overdue_items,
        "notified_member_count": len(notified_member_ids),
        "messages": messages
    }


# ----------------------------------------------------
# SIMPLE function (5-10 lines) RESERVE BOOK (ABI)
# ----------------------------------------------------
def reserve_book(member_id: str, item_id: str) -> str:
    book = None
    for item in catalog:
        if item["id"] == item_id:
            book = item
            break
    if book is None:
        return f"Item '{item_id}' not found in catalog."

    if member_id not in reservations:
        reservations[member_id] = []

    if item_id in reservations[member_id]:
        return f"You have already reserved book '{item_id}'."

    copies_left = int(book.get("copies_available", 0))

    # Case 1: copies are available → immediate reservation
    if copies_left > 0:
        reservations[member_id].append(item_id)
        book["copies_available"] = copies_left - 1
        return f"Item '{item_id}' reserved for member '{member_id}'."
    
    # Case 2: no copies available → use per-item waitlist in the catalog record
    waitlist = book.setdefault("waitlist", [])

    if member_id in waitlist:
        return f"You are already on the waitlist for book '{item_id}'."

    waitlist.append(member_id)
    return (
        f"No copies available. Member '{member_id}' added to the waitlist "
        f"for '{item_id}'."
    )


# ----------------------------------------------------
# SIMPLE function (5-10 lines) Book Rating System (ABI)
# ----------------------------------------------------
def rate_book(member_id, item_id, rating):
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5 stars.")

    if item_id not in ratings:
        ratings[item_id] = {}

    has_previous_rating = False
    if member_id in ratings[item_id]:
        has_previous_rating = True

    ratings[item_id][member_id] = rating

    rating_values = [user_rating for user_rating in ratings[item_id].values()]
    total_ratings = len(rating_values)
    sum_of_ratings = sum(rating_values)
    new_average = round(sum_of_ratings / total_ratings, 2)
    average_ratings[item_id] = new_average

    if has_previous_rating:
        message = f"Updated rating for book '{item_id}' to {rating} stars. New average: {new_average}"
    else:
        message = f"Rated book '{item_id}' with {rating} stars. Average now: {new_average}"

    return message


# ----------------------------------------------------
# MEDIUM (15–25 lines) Validate item id (ABI)
# ----------------------------------------------------
def validate_code(item_id: str) -> bool:
    """
    Validates library item codes.
    Acceptable formats:
        BK###  Books
        EB###  E-Books
        DV###  DVDs

    Must be:
        - Exactly 5 characters long
        - Prefix is BK, EB, or DV
        - Followed by 3 digits
    """

    if not isinstance(item_id, str):
        raise TypeError("Code must be a string.")

    code = item_id.strip().upper()

    # Must be exactly 5 characters
    if len(code) != 5:
        return False

    prefix = code[:2]
    digits = code[2:]

    # Prefix must be valid
    if prefix not in {"BK", "EB", "DV"}:
        return False

    # Must end with 3 digits
    if not digits.isdigit():
        return False

    return True



# ----------------------------------------------------
# COMPLEX (30+ lines) Generating Borrowing Report (ABI)
# ----------------------------------------------------
def generate_borrowing_report(fine_per_day=0.5):
    total_borrowed = len(loans)
    overdue_count = 0
    total_fines = 0.0

    users = defaultdict(lambda: {"borrowed": 0, "overdue": 0, "fines": 0.0})
    book_counts = Counter()
    current_date = datetime.now(timezone.utc)

    for record in loans:
        user_id = record.get("user_id") or record.get("member_id")
        item_id = record.get("item_id")
        if not user_id or not item_id:
            continue

        # --- parse due date into a datetime ---
        due_field = record.get("due_date")
        if isinstance(due_field, datetime):
            due_on = due_field
        elif isinstance(due_field, str):
            # assume simple YYYY-MM-DD string
            due_on = datetime.strptime(due_field, "%Y-%m-%d")
        else:
            # if we can't interpret due date, skip this record
            continue

        # --- parse returned date (if any) into a datetime ---
        returned_field = record.get("return_date") or record.get("returned_at")

        if returned_field is not None:
            if isinstance(returned_field, datetime):
                returned_on = returned_field
            elif isinstance(returned_field, str):
                returned_on = datetime.strptime(returned_field, "%Y-%m-%d")
            else:
                # unexpected type, treat as returned on due date
                returned_on = due_on
        else:
            # If no explicit return date:
            if record.get("returned") is True:
                returned_on = due_on
            else:
                # still out; treat "now" as the effective return date for fine calc
                returned_on = current_date

        # Normalize both to plain dates
        due_date = due_on.date()
        returned_date = returned_on.date()

        users[user_id]["borrowed"] += 1
        book_counts[item_id] += 1

        if returned_date > due_date:
            days_late = (returned_date - due_date).days
            fine_amount = days_late * fine_per_day
            users[user_id]["overdue"] += 1
            users[user_id]["fines"] += fine_amount
            overdue_count += 1
            total_fines += fine_amount

    most_active = max(users, key=lambda u: users[u]["borrowed"], default=None)
    top_book = book_counts.most_common(1)[0][0] if book_counts else None

    report = {
        "total_books_borrowed": total_borrowed,
        "total_overdue_books": overdue_count,
        "total_fines_collected": round(total_fines, 2),
        "user_activity": dict(users),
        "most_active_user": most_active,
        "most_borrowed_book": top_book,
    }
    return report

# ----------------------------------------------------
# Simple Function (5-10 lines) Calculate Due Date (kaliza)
# Calculate the due date for a borrowed library item.
# ----------------------------------------------------
def calculate_due_date(borrow_date: datetime, loan_days: int = 14, skip_weekends: bool = True) -> datetime:
    """Calculate the due date for a borrowed library item."""

    if not isinstance(borrow_date, datetime):
        raise TypeError("borrow_date must be a datetime object")
    # checks that the borrow_date is actually a datetime object, not a string or number
    
    if loan_days <= 0:
        raise ValueError("loan_days must be greater than 0")
    # makes sure the number of loan days is positive (you can’t borrow for 0 or negative days)
    
    due_date = borrow_date
    # start counting from the date the book was borrowed

    days_added = 0
    # keeps track of how many valid days have been counted so far

    while days_added < loan_days:
        due_date += timedelta(days=1)
        # move forward by one day

        if skip_weekends and due_date.weekday() in (5, 6):
            continue
        # if skip_weekends is True, skip Saturdays (5) and Sundays (6)

        days_added += 1
        # only count this day if it’s not a weekend

    return due_date
    # once we’ve added all valid loan days, return the due date


# ----------------------------------------------------
# SIMPLE Function (5-10 lines) Member Count (Kaliza)
# Return the total number of registered library members.
# ----------------------------------------------------
def member_count(active_only: bool = True) -> int:
    """Count how many library members exist in the system."""
    
    users = members
    # use the global members dictionary as the data source

    if not isinstance(users, dict):
        raise TypeError("users must be a dictionary")
    # ensures that the input is a dictionary like {user_id: {info}}

    count = 0
    # start a counter at zero to count members

    for udata in users.values():
        # loop through every user’s information inside the dictionary
        
        if not active_only or udata.get("active", True):
            count += 1
        # if we’re counting everyone, add all users
        # if we’re counting only active ones, check if “active” is True

    return count
    # return the total number of users found


# ----------------------------------------------------
# MEDIUM (15–25 lines) check in/ check out operations (Kaliza)
# Used to track exact borrow and return times
# ----------------------------------------------------
def check_in_out_operations(user_id: str, item_id: str, action: str = "borrow", loan_days: int = 14) -> dict:
    """Manage check-in and check-out operations for library books."""
    
    users = members
    catalog_list = catalog

    if user_id not in users:
        raise KeyError(f"User {user_id} not found")
    # makes sure the user exists in the system

    book = None
    for item in catalog_list:
        if item.get("id") == item_id:
            book = item
            break
    if book is None:
        raise KeyError(f"Book {item_id} not found")
    # makes sure the book exists in the catalog

    user = users[user_id]
    # get that specific user’s data

    if action == "borrow":
        if book.get("copies_available", 0) <= 0:
            raise ValueError(f"No available copies of {book.get('title', 'Unknown')}")
        book["copies_available"] -= 1

        loans_by_user = user.setdefault("loans", {})
        if item_id in loans_by_user and loans_by_user[item_id].get("returned_at") is None:
            raise ValueError("This book is already borrowed and not yet returned.")

        borrowed_at = datetime.now(timezone.utc)
        due_at = calculate_due_date(borrowed_at, loan_days)

        # Store on the member
        loans_by_user[item_id] = {
            "borrowed_at": borrowed_at,
            "due_at": due_at,
            "returned_at": None
        }

        # ALSO store in the global loans list for reports/notifications
        loans.append({
            "member_id": user_id,
            "item_id": item_id,
            "borrow_date": borrowed_at,
            "due_date": due_at,
            "returned": False,
        })

        return {"user": user_id, "book": item_id, "status": "borrowed", "due_at": due_at}

    elif action == "return":
        loans_by_user = user.get("loans", {})
        if item_id not in loans_by_user or loans_by_user[item_id].get("returned_at"):
            raise ValueError("Book not currently borrowed or already returned.")

        book["copies_available"] = book.get("copies_available", 0) + 1
        returned_at = datetime.now(timezone.utc)
        loans_by_user[item_id]["returned_at"] = returned_at

        # Also mark matching global loan as returned, if present
        for entry in loans:
            if (
                entry.get("member_id") == user_id
                and entry.get("item_id") == item_id
                and not entry.get("returned", False)
            ):
                entry["returned"] = True
                entry["return_date"] = returned_at
                break

        return {"user": user_id, "book": item_id, "status": "returned", "returned_at": returned_at}

    else:
        raise ValueError("Invalid action. Use 'borrow' or 'return'.")


# ----------------------------------------------------
# MEDIUM (15–25 lines) Waitlist Management (Kaliza)
# Add users to waitlist when a book is unavailable and notify them when available
# ----------------------------------------------------
def waitlist_management(item_id: str, user_id: str, action: str = "add") -> dict:
    """Manage a book's waitlist for unavailable items."""
    
    book = None
    for item in catalog:
        if item.get("id") == item_id:
            book = item
            break
    if book is None:
        raise KeyError(f"Item {item_id} not found in catalog.")
    if user_id not in members:
        raise KeyError(f"User {user_id} not found.")

    waitlist = book.setdefault("waitlist", [])

    if action == "add":
        # If copies exist, no need for waitlist
        if book.get("copies_available", 0) > 0:
            return {
                "message": f"Book '{book.get('title', 'Unknown')}' is available; no need for waitlist."
            }
        # Avoid duplicates
        if user_id in waitlist:
            return {
                "message": f"User {user_id} is already on the waitlist for {item_id}."
            }

        waitlist.append(user_id)
        return {"item_id": item_id, "waitlist": waitlist}

    elif action == "notify":
        if not waitlist:
            return {"message": f"No users on the waitlist for {item_id}."}
        next_user = waitlist.pop(0)
        return {
            "item_id": item_id,
            "notify_user": next_user,
            "message": (
                f"Notify {next_user}: '{book.get('title', 'Unknown')}' "
                f"is now available."
            ),
        }

    else:
        raise ValueError("Invalid action. Use 'add' or 'notify'.")


# ----------------------------------------------------
# SIMPLE Function (5-10 lines)  Format Search Query (Rood)
# ----------------------------------------------------
def format_search_query(q):
    """
    Clean up a search query and return:
        - original text
        - normalized text (cleaned)
        - list of tokens (words/phrases)
    """
    s = (q or "").strip().lower()
    s = "".join(
        c for c in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(c)
    )
    phrases = [m.strip('"') for m in re.findall(r'"([^"]*)"', s)]
    s = re.sub(r'"[^"]*"', " ", s)
    s = re.sub(r"[^\w\-]+", " ", s).strip()
    stop = {"the","a","an","and","or","of","for","to","in","on","at","by","with","from"}
    toks = []
    for t in s.split():
        if t and t not in stop:
            toks.append(t)
    for p in phrases:
        if p:
            toks.append(p)
    return {"original": q or "", "normalized": " ".join(toks), "tokens": toks}


# ----------------------------------------------------
# MEDIUM (15–25 lines)  User Account Management (Rood)
# ----------------------------------------------------
def user_account(
    *,
    action,
    user_id=None,
    item_id=None,
    loan_days=14,
    daily_rate=Decimal("0.25"),
    grace_days=0,
    pay_amount=None,
    user_obj=None,
    ):
    """
    Manage basic account actions.
    catalog example (adapted from your list):
        catalog = [{"id": "B1", "title": "...", "author": "...", "tags": {"fantasy"}, "copies_available": 3}, ...]
    users example:
        members = {"u1": {"name": "Alex", "email": "a@b.com", "active": True, "loans": {}, "balance": Decimal("0.00")}}
    """
    def money(x):
        return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    catalog_dict = {b.get("id"): b for b in catalog}
    users = members

    if action == "validate":
        u = user_obj or (users.get(user_id) if user_id else None)
        if not u or not u.get("active", True):
            raise ValueError("Account disabled/missing")
        if not (u.get("name") or "").strip():
            raise ValueError("Name required")
        email = (u.get("email") or "").strip()
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Invalid email")
        return True

    if action == "borrow":
        u = users.get(user_id)
        b = catalog_dict.get(item_id)
        if not u or not b:
            raise KeyError("User or book not found")
        user_account(action="validate", user_obj=u)
        if b.get("copies_available", 0) <= 0:
            raise ValueError("No copies")
        loans = u.setdefault("loans", {})
        if item_id in loans and loans[item_id].get("returned_at") is None:
            raise ValueError("Already borrowed")
        now = datetime.now(timezone.utc)
        due = now + timedelta(days=loan_days)
        b["copies_available"] = int(b.get("copies_available", 0)) - 1
        loans[item_id] = {"borrowed_at": now, "due_at": due, "returned_at": None}
        return loans[item_id]

    if action == "return":
        u = users.get(user_id)
        b = catalog_dict.get(item_id)
        if not u:
            raise KeyError("User not found")
        loans = u.setdefault("loans", {})
        loan = loans.get(item_id)
        if not loan or loan.get("returned_at") is not None:
            raise KeyError("No active loan")
        now = datetime.now(timezone.utc)
        loan["returned_at"] = now
        due_date = loan["due_at"].date()
        days_late = (now.date() - due_date).days
        effective_late = max(0, days_late - max(0, grace_days))
        fine = Decimal("0.00")
        if effective_late > 0:
            fine = money(Decimal(effective_late) * money(daily_rate))
            u["balance"] = money(Decimal(u.get("balance", "0.00")) + fine)
        if b is not None:
            b["copies_available"] = int(b.get("copies_available", 0)) + 1
        return {
            "item_id": item_id,
            "returned_at": now,
            "days_late": max(0, days_late),
            "effective_late": effective_late,
            "fine": money(fine),
            "balance": money(Decimal(u.get("balance", "0.00"))),
        }

    if action == "pay":
        u = users.get(user_id)
        if not u:
            raise KeyError("User not found")
        amt = money(pay_amount or 0)
        if amt <= 0:
            raise ValueError("Payment must be > 0")
        current = money(Decimal(u.get("balance", "0.00")))
        new_balance = current - amt
        if new_balance < 0:
            new_balance = Decimal("0.00")
        u["balance"] = money(new_balance)
        return {"paid": amt, "balance": money(new_balance)}

    raise ValueError(f"Unknown action: {action!r}")


# ----------------------------------------------------
# COMPLEX (30+ lines)  Recommendation System (Rood)
# ----------------------------------------------------
def recommend_books(*, member_id, limit=10):
    """
    Recommend books based on:
        - Tags the user likes
        - Authors the user likes
        - Tags from books the user borrowed before
        - Prefer books that are in stock
    Returns a list of (item_id, score), highest score first.
    """
    catalog_dict = {b.get("id"): b for b in catalog}
    user = members.get(member_id, {})

    prefs_tags = set(user.get("preferences_tags", set()))
    prefs_authors = set(user.get("preferences_authors", set()))
    member_loans_dict = user.get("loans", {}) or {}

    borrowed_item_ids = set(member_loans_dict.keys())
    if not borrowed_item_ids:
        borrowed_item_ids = {ln["item_id"] for ln in loans if ln.get("member_id") == member_id}

    history_tag_counts = {}
    for item_id in borrowed_item_ids:
        b = catalog_dict.get(item_id)
        if not b:
            continue
        for t in set(b.get("tags", set())):
            history_tag_counts[t] = history_tag_counts.get(t, 0) + 1

    def score_book(b):
        tags = set(b.get("tags", set()))
        author = b.get("author", "")
        qty = b.get("copies_available", 0)
        tag_matches = sum(1 for t in tags if t in prefs_tags or t in history_tag_counts)
        score = float(tag_matches)
        if author in prefs_authors:
            score += 1.5
        if author and any((catalog_dict.get(i) or {}).get("author") == author for i in borrowed_item_ids):
            score += 0.5
        if qty and qty > 0:
            score += 0.3
        else:
            score -= 1.0
        return score

    scored = []
    for item_id, b in catalog_dict.items():
        if item_id in borrowed_item_ids:
            continue
        s = score_book(b)
        if s > 0:
            scored.append((item_id, s))

    scored.sort(
        key=lambda item: (item[1], (catalog_dict[item[0]].get("title") or ""), item[0]),
        reverse=True
    )
    return scored[:limit]
