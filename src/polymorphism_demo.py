# --------------------------------------------
# Project 3 – Polymorphism Demonstration
# --------------------------------------------

from datetime import date
from library_items import BookItem, EBookItem, DVDItem


def summarize_items(items):
    """
    Demonstrates polymorphism by calling the same method
    on different item types.
    """
    summaries = []

    for item in items:
        desc = item.describe()
        days = item.calculate_loan_period()
        due = item.due_date_for(date.today())
        summaries.append(f"{desc} — Loan: {days} days, Due: {due}")

    return summaries


if __name__ == "__main__":
    book = BookItem("b1", "Dune", "Frank Herbert", "Sci-fi")
    ebook = EBookItem("e1", "Digital Literacy", "Smith", "Education")
    dvd = DVDItem("d1", "The Matrix", "Wachowski", "Sci-Fi")

    for line in summarize_items([book, ebook, dvd]):
        print(line)
