import library_functions as lib

class Member:
    """Represents a library member and account actions."""
    
    def __init__(self, member_id: str, name: str, email: str, active: bool = True, tags: set = None, authors: set = None):
        """Initialize a Member."""
        if not member_id.strip():
            raise ValueError("Member ID cannot be empty.")
        if not name.strip():
            raise ValueError("Member name cannot be empty.")
        if "@" not in email:
            raise ValueError("Invalid email address.")
        
        self._member_id = member_id
        self._name = name
        self._email = email
        self._active = active
        self._balance = 0.0
        self._loans = {}
        self._preferences_tags = tags if tags else set()
        self._preferences_authors = authors if authors else set()

        # --- Append to global members dictionary ---
        lib.members[self._member_id] = {
            "name": self._name,
            "email": self._email,
            "active": self._active,
            "balance": self._balance,
            "loans": self._loans,
            "preferences_tags": self._preferences_tags,
            "preferences_authors": self._preferences_authors
        }
    
    # -------------------------------
    # Properties
    # -------------------------------
    @property
    def member_id(self):
        return self._member_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
    
    @property
    def active(self):
        return self._active

    # -------------------------------
    # Methods (Integrated)
    # -------------------------------
    def validate_account(self):
        """Validate member account using user_account()."""
        return lib.user_account(action="validate", user_id=self._member_id)

    def borrow_book(self, item_id: str):
        """Borrow a book."""
        result = lib.check_in_out_operations(self._member_id, item_id, action="borrow")
        return f"{self._name} borrowed {item_id}, due {result['due_at'].date()}"

    def return_book(self, item_id: str):
        """Return a borrowed book."""
        result = lib.check_in_out_operations(self._member_id, item_id, action="return")
        return f"{self._name} returned {item_id} on {result['returned_at'].date()}"

    def pay_balance(self, amount):
        """Pay a fine or balance using user_account()."""
        return lib.user_account(action="pay", user_id=self._member_id, pay_amount=amount)

    @staticmethod
    def total_active_members():
        """Return total count of active members."""
        return lib.member_count(active_only=True)
    
    def __str__(self):
        return f"{self._name} ({self._email}) - Active: {self._active}"
