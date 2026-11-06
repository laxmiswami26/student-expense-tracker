# Personal Expense Tracker

A beginner-friendly Python command-line project that solves a real-life problem: tracking daily spending and keeping expenses within a monthly budget.

## Features
- Add expenses with date, category, amount, and description
- Store records in a CSV file (no external packages required)
- View all expenses
- Summarize spending by category
- Check spending against a monthly budget
- Export-friendly CSV storage

## Requirements
- Python 3.9+
- No third-party packages

## Run
```bash
python main.py
```

On first run, the app creates `expenses.csv` automatically. Choose **Set monthly budget** to configure a budget.

## Example
1. Choose `1` to add an expense.
2. Enter date as `YYYY-MM-DD` (press Enter for today).
3. Enter category, amount, and description.
4. Choose `3` to view category totals.

## Project structure
```text
personal_expense_tracker/
├── main.py
├── expense_tracker.py
├── expenses.csv
├── README.md
└── tests/
    └── test_expense_tracker.py
```

## Learning outcomes
- Functions and modules
- Input validation and exception handling
- CSV file handling
- Dates and data aggregation
- Unit testing

## Future improvements
- GUI using Tkinter
- Charts using Matplotlib
- SQLite database
- Recurring expenses and receipt attachments

## License
MIT
