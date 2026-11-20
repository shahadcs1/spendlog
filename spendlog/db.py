import sqlite3
from datetime import date
from pathlib import Path

DEFAULT_DB = Path.home() / ".spendlog.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spent_on TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    category TEXT NOT NULL,
    note TEXT DEFAULT ''
);
"""


def connect(path=DEFAULT_DB):
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def add_expense(conn, amount, category, note="", spent_on=None):
    if amount <= 0:
        raise ValueError("amount must be positive")
    spent_on = spent_on or date.today().isoformat()
    date.fromisoformat(spent_on)  # validates format YYYY-MM-DD
    cur = conn.execute(
        "INSERT INTO expenses (spent_on, amount, category, note) VALUES (?, ?, ?, ?)",
        (spent_on, amount, category.strip().lower(), note),
    )
    conn.commit()
    return cur.lastrowid


def list_expenses(conn, month=None, category=None):
    query, params = "SELECT * FROM expenses WHERE 1=1", []
    if month:
        query += " AND substr(spent_on, 1, 7) = ?"
        params.append(month)
    if category:
        query += " AND category = ?"
        params.append(category.strip().lower())
    return conn.execute(query + " ORDER BY spent_on, id", params).fetchall()


def summary_by_category(conn, month=None):
    query, params = "SELECT category, SUM(amount) AS total, COUNT(*) AS n FROM expenses", []
    if month:
        query += " WHERE substr(spent_on, 1, 7) = ?"
        params.append(month)
    query += " GROUP BY category ORDER BY total DESC"
    return conn.execute(query, params).fetchall()


def delete_expense(conn, expense_id):
    cur = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    return cur.rowcount > 0
