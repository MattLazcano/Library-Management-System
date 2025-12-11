"""
Comprehensive Test Suite for Library Management System

Demonstrates:
- Unit testing for individual functions and classes
- Integration testing for interactions between classes and global data
- System testing for full end-to-end workflows
- Use of unittest framework with clear organization

Covers:
- Global function library (library_functions.py)
- OOP classes: LibraryItem hierarchy, Member, Loan, Search, LibrarySystem
- Persistence helpers (save/load/import/export)
"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "src"))


from src.class_lib_items import BookItem, EBookItem, DVDItem
from src.class_member import Member
from src.class_loan import Loan
from src.class_search import Search
from src.library_system import LibrarySystem
from src import persistence
from src import library_functions as lib 

import unittest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta, timezone
from decimal import Decimal


# ---------------------------------------------------------
# Helper: reset all global data between tests
# ---------------------------------------------------------
def reset_globals():
    lib.catalog.clear()
    lib.members.clear()
    lib.reminders.clear()
    lib.loans.clear()
    lib.reservations.clear()
    lib.ratings.clear()
    lib.average_ratings.clear()


# =========================================================
# UNIT TESTS – INDIVIDUAL FUNCTIONS & CLASSES
# =========================================================

class TestValidateCodeAndLibraryItems(unittest.TestCase):
    """Unit tests for validate_code and LibraryItem subclasses."""

    def setUp(self):
        reset_globals()

    def test_validate_code_valid_patterns(self):
        """Codes with BK/EB/DV + 3 digits should be valid."""
        self.assertTrue(lib.validate_code("BK123"))
        self.assertTrue(lib.validate_code("EB001"))
        self.assertTrue(lib.validate_code("DV999"))

    def test_validate_code_invalid_patterns(self):
        """Invalid prefixes/lengths should be rejected."""
        self.assertFalse(lib.validate_code("B1234"))   # wrong prefix
        self.assertFalse(lib.validate_code("BK12"))    # too short
        self.assertFalse(lib.validate_code("BK12A"))   # last 3 not all digits
        self.assertFalse(lib.validate_code("BOOK1"))   # wrong format

    def test_bookitem_registers_in_catalog(self):
        """Creating a BookItem should auto-register into global catalog with media_type."""
        item = BookItem("BK101", "Dune", "Frank Herbert", "Sci-Fi")
        self.assertEqual(len(lib.catalog), 1)
        record = lib.catalog[0]
        self.assertEqual(record["id"], "BK101")
        self.assertEqual(record["title"], "Dune")
        self.assertEqual(record["author"], "Frank Herbert")
        self.assertEqual(record["genre"], "Sci-Fi")
        self.assertEqual(record["media_type"], "Book")
        self.assertEqual(record["copies_total"], 1)
        self.assertEqual(record["copies_available"], 1)
        self.assertIn("[Book]", item.describe())

    def test_ebook_and_dvd_types(self):
        """EBookItem and DVDItem should set different media_type values."""
        BookItem("BK100", "X", "A", "G")
        EBookItem("EB123", "Digital Literacy", "Smith", "Education")
        DVDItem("DV101", "The Matrix", "Wachowski", "Sci-Fi")
        media_types = sorted({rec["media_type"] for rec in lib.catalog})
        self.assertIn("Book", media_types)
        self.assertIn("E-Book", media_types)
        self.assertIn("DVD", media_types)

    def test_calculate_loan_periods_polymorphic(self):
        """Each subclass implements its own loan period."""
        b = BookItem("BK200", "A", "X", "G")
        e = EBookItem("EB200", "B", "Y", "G")
        d = DVDItem("DV200", "C", "Z", "G")
        self.assertEqual(b.calculate_loan_period(), 21)
        self.assertEqual(e.calculate_loan_period(), 14)
        self.assertEqual(d.calculate_loan_period(), 7)


class TestMemberAndAccountUnit(unittest.TestCase):
    """Unit tests for Member and account-related functions."""

    def setUp(self):
        reset_globals()
        BookItem("BK001", "Clean Code", "Martin", "Programming")
        self.member = Member("M1", "Alex", "alex@example.com")

    def test_member_auto_registers(self):
        """Member __init__ should insert into global members dict."""
        self.assertIn("M1", lib.members)
        data = lib.members["M1"]
        self.assertEqual(data["name"], "Alex")
        self.assertEqual(data["email"], "alex@example.com")
        self.assertTrue(data["active"])

    def test_validate_account_success(self):
        """validate_account uses user_account('validate') under the hood."""
        self.assertTrue(self.member.validate_account())

    def test_member_count_active_only(self):
        """member_count should handle active-only vs all-members."""
        Member("M2", "Inactive User", "inactive@example.com", active=False)
        self.assertEqual(Member.total_active_members(), 1)
        self.assertEqual(lib.member_count(active_only=False), 2)

    def test_borrow_and_return_book_via_member(self):
        """Borrow and return through Member, ensuring copies_available syncs with global catalog."""
        msg = self.member.borrow_book("BK001")
        self.assertIn("borrowed BK001", msg)
        rec = lib.catalog[0]
        self.assertEqual(rec["copies_available"], 0)

        msg2 = self.member.return_book("BK001")
        self.assertIn("returned BK001", msg2)
        rec = lib.catalog[0]
        self.assertEqual(rec["copies_available"], 1)

    def test_pay_balance_through_member(self):
        """Member.pay_balance should reduce global balance."""
        lib.members["M1"]["balance"] = Decimal("5.00")
        result = self.member.pay_balance(Decimal("2.50"))
        self.assertEqual(result["balance"], Decimal("2.50"))


class TestSearchUnit(unittest.TestCase):
    """Unit tests for Search wrapper class."""

    def setUp(self):
        reset_globals()
        BookItem("BK100", "Python Basics", "Guido", "Programming")
        BookItem("BK101", "Clean Architecture", "Martin", "Programming")
        BookItem("BK102", "The Hobbit", "Tolkien", "Fantasy")
        self.search = Search()

    def test_find_books_by_title(self):
        """Search by title substring."""
        results = self.search.find_books(query="python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Python Basics")

    def test_find_books_by_genre(self):
        """Search filtered by genre."""
        results = self.search.find_books(genre="fantasy")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["author"], "Tolkien")

    def test_normalize_query(self):
        """format_search_query should return tokens including phrases."""
        q = self.search.normalize_query('  "data science" and AI in libraries ')
        self.assertIn("data science", q["tokens"])
        self.assertIn("ai", q["tokens"])


class TestLoanAndReportUnit(unittest.TestCase):
    """Unit tests for Loan + borrowing report."""

    def setUp(self):
        reset_globals()
        BookItem("BK900", "Test Book", "Author", "Test")
        Member("M9", "Test User", "test@example.com")

    def test_loan_adds_to_global_loans(self):
        """Loan __init__ should append a record to global loans list."""
        before = len(lib.loans)
        Loan("M9", "BK900")
        self.assertEqual(len(lib.loans), before + 1)
        record = lib.loans[-1]
        self.assertEqual(record["member_id"], "M9")
        self.assertEqual(record["item_id"], "BK900")
        self.assertIn("due_date", record)

    def test_generate_borrowing_report_structure(self):
        """Borrowing report should include high-level stats."""
        Loan("M9", "BK900")
        report = lib.generate_borrowing_report()
        self.assertIn("total_books_borrowed", report)
        self.assertIn("user_activity", report)
        self.assertIn("most_active_user", report)


# =========================================================
# PERSISTENCE UNIT TESTS – FILE I/O ONLY
# =========================================================

class TestPersistenceUnit(unittest.TestCase):
    """Unit tests for persistence helpers (save/load/import/export)."""

    def setUp(self):
        reset_globals()
        BookItem("BK001", "Dune", "Frank Herbert", "Sci-Fi")
        Member("M1", "Alex", "alex@example.com")
        Loan("M1", "BK001")

    def test_save_and_load_state_roundtrip(self):
        """save_state + load_state should preserve catalog/members/loans."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "state.json"

            persistence.save_state(tmp_path)

            reset_globals()
            self.assertEqual(len(lib.catalog), 0)
            self.assertEqual(len(lib.members), 0)
            self.assertEqual(len(lib.loans), 0)

            persistence.load_state(tmp_path)

            self.assertEqual(len(lib.catalog), 1)
            self.assertEqual(len(lib.members), 1)
            self.assertEqual(len(lib.loans), 1)
            self.assertEqual(lib.catalog[0]["title"], "Dune")
            self.assertIn("M1", lib.members)

    def test_export_borrowing_report_csv(self):
        """export_borrowing_report_csv should create a CSV file with summary data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "borrowing_report.csv"
            path = persistence.export_borrowing_report_csv(csv_path)
            self.assertTrue(path.exists())
            text = path.read_text(encoding="utf-8")
            self.assertIn("total_books_borrowed", text)

    def test_import_catalog_from_csv(self):
        """import_catalog_from_csv should populate global catalog from a CSV file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "catalog_import.csv"
            csv_path.write_text(
                "id,title,author,genre,media_type,copies_total\n"
                "BK111,Book One,Author A,Fiction,Book,2\n"
                "EB222,Ebook Two,Author B,Education,E-Book,3\n",
                encoding="utf-8",
            )

            lib.catalog.clear()
            imported = persistence.import_catalog_from_csv(csv_path)

            self.assertEqual(imported, 2)
            self.assertEqual(len(lib.catalog), 2)
            ids = {b["id"] for b in lib.catalog}
            self.assertEqual(ids, {"BK111", "EB222"})


# =========================================================
# INTEGRATION TESTS – CLASSES + GLOBALS + PERSISTENCE
# =========================================================

class TestIntegrationWorkflows(unittest.TestCase):
    """
    Integration tests:
    - LibrarySystem facade + domain classes + global data
    - Borrow/return + waitlist
    - Recommendations
    - Ratings + reports
    - Overdue notifications
    - Save/load full system state
    """

    def setUp(self):
        reset_globals()
        self.system = LibrarySystem()

        # Create items via facade
        self.system.add_book("BK100", "Dune", "Frank Herbert", "Sci-Fi", copies_total=1)
        self.system.add_ebook("EB200", "Digital Libraries", "Smith", "Information Science", copies_total=2)
        self.system.add_dvd("DV300", "The Matrix", "Wachowski", "Sci-Fi", copies_total=1)

        # Create members
        self.m1 = self.system.add_member("M1", "Alex", "alex@example.com")
        self.m2 = self.system.add_member("M2", "Jamie", "jamie@example.com")

    def test_integration_borrow_and_waitlist_flow(self):
        """Borrow via Member + reserve via Search should populate waitlist."""
        borrow_msg = self.m1.borrow_book("BK100")
        self.assertIn("borrowed BK100", borrow_msg)

        search = self.system.search
        response = search.reserve("M2", "BK100")
        self.assertIn("waitlist", response.lower())
        self.assertIn("M2", lib.catalog[0]["waitlist"])

    def test_integration_recommendations_based_on_tags(self):
        """Recommendations should use tags + history across catalog + members + loans."""
        for item in lib.catalog:
            if item["id"] == "BK100":
                item["tags"] = {"sci-fi", "classic"}
            if item["id"] == "EB200":
                item["tags"] = {"information", "library"}

        lib.members["M1"]["preferences_tags"] = {"sci-fi"}
        Loan("M1", "BK100")

        search = self.system.search
        recs = search.recommend_for_member("M1", limit=5)
        self.assertTrue(len(recs) >= 1)
        recommended_ids = {item_id for (item_id, score) in recs}
        catalog_ids = {b["id"] for b in lib.catalog}
        self.assertTrue(recommended_ids.issubset(catalog_ids))

    def test_integration_ratings_and_report(self):
        """rate_book + generate_borrowing_report should reflect shared state."""
        # Member M1 borrows EB200 then rates it
        self.m1.borrow_book("EB200")
        msg = lib.rate_book("M1", "EB200", 5)
        self.assertIn("Rated book 'EB200' with 5 stars", msg)
        self.assertIn("EB200", lib.average_ratings)

        report = lib.generate_borrowing_report()
        self.assertGreaterEqual(report["total_books_borrowed"], 1)
        self.assertIn("user_activity", report)

    def test_integration_overdue_notifications(self):
        """automated_overdue_notifications should read global loans + catalog + members."""
        # Create a clearly overdue loan
        past_due = datetime.now(timezone.utc) - timedelta(days=10)
        lib.loans.append({
            "member_id": "M1",
            "item_id": "BK100",
            "borrow_date": past_due - timedelta(days=7),
            "due_date": past_due,
            "returned": False,
        })

        # Ensure member + catalog match
        lib.members["M1"]["name"] = "Alex"
        result = lib.automated_overdue_notifications(today=datetime.now(timezone.utc).date(), daily_fee=0.5, grace_days=0)
        self.assertGreaterEqual(result["total_overdue_items"], 1)
        self.assertGreaterEqual(result["notified_member_count"], 1)
        self.assertTrue(any("Dune" in msg["text"] or "BK100" in msg["text"] for msg in result["messages"]))

    def test_integration_save_and_load_entire_system(self):
        """save_state + load_state should keep LibrarySystem statistics intact."""
        self.m1.borrow_book("EB200")
        self.m2.borrow_book("DV300")

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "state.json"

            persistence.save_state(path)

            item_count = len(lib.catalog)
            member_count = len(lib.members)
            loan_count = len(lib.loans)

            reset_globals()
            self.assertEqual(len(lib.catalog), 0)
            self.assertEqual(len(lib.members), 0)
            self.assertEqual(len(lib.loans), 0)

            persistence.load_state(path)
            self.assertEqual(len(lib.catalog), item_count)
            self.assertEqual(len(lib.members), member_count)
            self.assertEqual(len(lib.loans), loan_count)


# =========================================================
# SYSTEM TESTS – FULL END-TO-END WORKFLOWS
# =========================================================

class TestSystemEndToEnd(unittest.TestCase):
    """
    System-level tests:
    - Full borrow/return workflow
    - High-level reporting + CSV export
    - Persistence across runs + continued usage
    """

    def setUp(self):
        reset_globals()
        self.system = LibrarySystem()

    def test_system_full_borrow_return_cycle(self):
        """
        End-to-end: add item + member, borrow once, return once, check counts.
        """
        sys = LibrarySystem()

        # Add a single-copy book and a member
        bk = sys.add_book("BK500", "Test Book", "Author", "Fiction", copies_total=1)
        member = sys.add_member("M500", "Test User", "user@example.com")

        # Borrow the book
        borrow_msg = member.borrow_book("BK500")
        self.assertIn("borrowed", borrow_msg)

        # After borrowing, there should be 0 copies available
        rec = next(r for r in lib.catalog if r["id"] == "BK500")
        self.assertEqual(rec["copies_available"], 0)

        # Return the book
        return_msg = member.return_book("BK500")
        self.assertIn("returned", return_msg)

        # After returning, copies_available should be back to 1
        rec = next(r for r in lib.catalog if r["id"] == "BK500")
        self.assertEqual(rec["copies_available"], 1)

        # And the borrowing report should show at least one borrowed book
        report = lib.generate_borrowing_report()
        self.assertGreaterEqual(report["total_books_borrowed"], 1)

    def test_system_report_and_export(self):
        """End-to-end: generate borrowing report and export it to CSV."""
        self.system.add_book("BK600", "Testing Software", "Myers", "CS", copies_total=1)
        self.system.add_member("M20", "Jordan", "jordan@example.com")
        Loan("M20", "BK600")

        report = lib.generate_borrowing_report()
        self.assertGreaterEqual(report["total_books_borrowed"], 1)

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "report.csv"
            out = persistence.export_borrowing_report_csv(csv_path)
            self.assertTrue(out.exists())
            text = out.read_text(encoding="utf-8")
            self.assertIn("total_books_borrowed", text)

    def test_system_persistence_with_workflow(self):
        """End-to-end: build system, save, reset, reload, then run search again."""
        self.system.add_book("BK700", "Data Science 101", "Smith", "Data", copies_total=1)
        m = self.system.add_member("M30", "Morgan", "morgan@example.com")
        m.borrow_book("BK700")

        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            persistence.save_state(state_path)

            reset_globals()
            persistence.load_state(state_path)

            search = Search()
            results = search.find_books(query="data science")
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["id"], "BK700")
            self.assertIn("M30", lib.members)


# =========================================================
# Test Runner Helper (similar to professor's style)
# =========================================================

def run_tests():
    """Run all tests in this module and print a short summary."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestValidateCodeAndLibraryItems))
    suite.addTests(loader.loadTestsFromTestCase(TestMemberAndAccountUnit))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchUnit))
    suite.addTests(loader.loadTestsFromTestCase(TestLoanAndReportUnit))
    suite.addTests(loader.loadTestsFromTestCase(TestPersistenceUnit))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWorkflows))
    suite.addTests(loader.loadTestsFromTestCase(TestSystemEndToEnd))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors:   {len(result.errors)}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    raise SystemExit(0 if success else 1)