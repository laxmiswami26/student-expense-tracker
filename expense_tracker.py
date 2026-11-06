"""Core logic for the Personal Expense Tracker."""
import csv
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

FIELDS = ["date", "category", "amount", "description"]


def validate_expense(expense):
    """Validate and normalize an expense dictionary."""
    try:
        parsed_date = datetime.strptime(expense["date"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        raise ValueError("Date must use YYYY-MM-DD format.")
    category = str(expense.get("category", "")).strip()
    description = str(expense.get("description", "")).strip()
    try:
        amount = float(expense["amount"])
    except (KeyError, TypeError, ValueError):
        raise ValueError("Amount must be a number.")
    if not category:
        raise ValueError("Category cannot be empty.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return {
        "date": parsed_date.isoformat(),
        "category": category.title(),
        "amount": round(amount, 2),
        "description": description,
    }


def add_expense(path, expense):
    """Append a validated expense to a CSV file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = validate_expense(expense)
    new_file = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(normalized)
    return normalized


def load_expenses(path):
    """Read expenses from CSV; return an empty list if it doesn't exist."""
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    expenses = []
    for row in rows:
        try:
            expenses.append(validate_expense(row))
        except (ValueError, KeyError):
            # Ignore malformed rows instead of crashing the application.
            continue
    return expenses


def category_totals(expenses, year=None, month=None):
    """Return total spending grouped by category for an optional month."""
    totals = defaultdict(float)
    for item in expenses:
        item_date = date.fromisoformat(item["date"])
        if year is not None and item_date.year != year:
            continue
        if month is not None and item_date.month != month:
            continue
        totals[item["category"]] += float(item["amount"])
    return {key: round(value, 2) for key, value in sorted(totals.items())}


def monthly_total(expenses, year, month):
    """Calculate total expenses for a given year and month."""
    return round(sum(
        float(item["amount"]) for item in expenses
        if date.fromisoformat(item["date"]).year == year
        and date.fromisoformat(item["date"]).month == month
    ), 2)
