from datetime import datetime
from src import library_functions as lib

class Loan:
    """Represents a loan transaction."""
    
    def __init__(self, member_id: str, item_id: str, borrow_date: datetime = None, loan_days: int = 14):
        """Initialize a Loan record and append to the global loan list."""
        if not member_id.strip() or not item_id.strip():
            raise ValueError("Member ID and Item ID cannot be empty.")
        
        self._member_id = member_id
        self._item_id = item_id
        self._borrow_date = borrow_date or datetime.now()
        self._loan_days = loan_days
        self._due_date = lib.calculate_due_date(self._borrow_date, loan_days)
        self._returned = False

        # Automatically add to the global loans list
        loan_record = {
            "member_id": self._member_id,
            "item_id": self._item_id,
            "borrow_date": self._borrow_date,
            "due_date": self._due_date,
            "returned": self._returned
        }
        lib.loans.append(loan_record)

    
    # -------------------------------
    # Properties
    # -------------------------------
    @property
    def member_id(self):
        return self._member_id

    @property
    def item_id(self):
        return self._item_id

    @property
    def due_date(self):
        return self._due_date

    # -------------------------------
    # Methods (Integrated)
    # -------------------------------
    def is_overdue(self):
        """Check if this loan is overdue."""
        return datetime.now() > self._due_date

    @staticmethod
    def generate_reports():
        """Generate full borrowing report."""
        return lib.generate_borrowing_report()

    @staticmethod
    def overdue_notifications():
        """Trigger automated overdue notifications."""
        return lib.automated_overdue_notifications()
    
    def __str__(self):
        status = "Overdue" if self.is_overdue() else "On time"
        return f"Loan(Member: {self._member_id}, Item: {self._item_id}, Due: {self._due_date.date()}, Status: {status})"
