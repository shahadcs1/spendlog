# spendlog

A small command-line expense tracker written in Python. Expenses are stored locally in SQLite, so it has **no external dependencies**.

## Why
I wanted a fast way to log daily spending and see where my money goes each month, without opening a spreadsheet.

## Usage
```bash
python -m spendlog add 45.5 food -n "lunch"
python -m spendlog add 120 transport -d 2026-11-03
python -m spendlog list -m 2026-11
python -m spendlog summary -m 2026-11
python -m spendlog export -m 2026-11 > november.csv
python -m spendlog delete 3
```

Example `summary` output:
```
transport        120.00  72.5%  ##############################
food              45.50  27.5%  ###########
--------------------------------------------------
TOTAL            165.50
```

## Structure
- `spendlog/db.py` – SQLite schema and queries
- `spendlog/report.py` – table, summary bars and CSV formatting
- `spendlog/cli.py` – argparse command-line interface
- `tests/` – unit tests (`python -m unittest discover tests`)

## Ideas for next steps
Monthly budgets with warnings, recurring expenses, import from bank CSV.
