"""Command-line interface for the Personal Expense Tracker."""
from datetime import date
from pathlib import Path
import json

from expense_tracker import add_expense, load_expenses, category_totals, monthly_total

DATA_FILE = Path(__file__).with_name("expenses.csv")
BUDGET_FILE = Path(__file__).with_name("budget.json")


def read_budget():
    if not BUDGET_FILE.exists():
        return None
    try:
        return float(json.loads(BUDGET_FILE.read_text(encoding="utf-8"))["monthly_budget"])
    except (ValueError, KeyError, OSError, TypeError):
        return None


def set_budget():
    try:
        amount = float(input("Enter monthly budget: ₹"))
        if amount <= 0:
            raise ValueError
        BUDGET_FILE.write_text(
            json.dumps({"monthly_budget": amount}, indent=2), encoding="utf-8"
        )
        print("Monthly budget saved.")
    except ValueError:
        print("Please enter a valid amount greater than zero.")


def add_new_expense():
    today = date.today().isoformat()
    expense = {
        "date": input(f"Date [{today}]: ").strip() or today,
        "category": input("Category (e.g. Food, Travel, Bills): "),
        "amount": input("Amount in ₹: "),
        "description": input("Description: "),
    }
    try:
        saved = add_expense(DATA_FILE, expense)
        print(f"Saved ₹{saved['amount']:.2f} under {saved['category']}.")
    except ValueError as error:
        print(f"Could not save expense: {error}")


def show_expenses():
    expenses = load_expenses(DATA_FILE)
    if not expenses:
        print("No expenses recorded yet.")
        return
    print("\nDATE       CATEGORY       AMOUNT       DESCRIPTION")
    print("-" * 65)
    for item in expenses:
        print(f"{item['date']}  {item['category']:<13} ₹{float(item['amount']):>9.2f}  {item['description']}")


def show_monthly_summary():
    today = date.today()
    expenses = load_expenses(DATA_FILE)
    totals = category_totals(expenses, today.year, today.month)
    total = monthly_total(expenses, today.year, today.month)
    print(f"\nSpending summary for {today.strftime('%B %Y')}")
    if not totals:
        print("No expenses recorded for this month.")
    else:
        for category, amount in totals.items():
            print(f"{category:<18} ₹{amount:,.2f}")
        print("-" * 30)
        print(f"{'TOTAL':<18} ₹{total:,.2f}")
    budget = read_budget()
    if budget is not None:
        remaining = budget - total
        print(f"Budget: ₹{budget:,.2f}")
        print(f"Remaining: ₹{remaining:,.2f}")
        if remaining < 0:
            print("Alert: You have exceeded your monthly budget.")


def main():
    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Monthly spending summary")
        print("4. Set monthly budget")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_new_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            show_monthly_summary()
        elif choice == "4":
            set_budget()
        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1 to 5.")


if __name__ == "__main__":
    main()
