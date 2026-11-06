import tempfile
import unittest
from pathlib import Path

from expense_tracker import add_expense, load_expenses, category_totals, monthly_total


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.temp_dir.name) / "expenses.csv"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_load_expense(self):
        add_expense(self.csv_path, {
            "date": "2026-11-06", "category": "food",
            "amount": "120.50", "description": "Lunch"
        })
        records = load_expenses(self.csv_path)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["category"], "Food")
        self.assertEqual(records[0]["amount"], 120.5)

    def test_reject_non_positive_amount(self):
        with self.assertRaises(ValueError):
            add_expense(self.csv_path, {
                "date": "2026-11-06", "category": "Food",
                "amount": "0", "description": "Invalid"
            })

    def test_monthly_summary(self):
        records = [
            {"date": "2026-11-01", "category": "Food", "amount": 100},
            {"date": "2026-11-02", "category": "Travel", "amount": 50},
            {"date": "2026-10-02", "category": "Food", "amount": 75},
        ]
        self.assertEqual(category_totals(records, 2026, 11),
                         {"Food": 100.0, "Travel": 50.0})
        self.assertEqual(monthly_total(records, 2026, 11), 150.0)


if __name__ == "__main__":
    unittest.main()
