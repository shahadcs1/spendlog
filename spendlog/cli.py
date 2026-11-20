import argparse
import sys

from . import db, report


def build_parser():
    p = argparse.ArgumentParser(prog="spendlog", description="Track your spending from the terminal.")
    p.add_argument("--db", default=str(db.DEFAULT_DB), help="path to the SQLite database file")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="record an expense")
    a.add_argument("amount", type=float)
    a.add_argument("category")
    a.add_argument("-n", "--note", default="")
    a.add_argument("-d", "--date", help="YYYY-MM-DD (default: today)")

    l = sub.add_parser("list", help="list expenses")
    l.add_argument("-m", "--month", help="filter by month, YYYY-MM")
    l.add_argument("-c", "--category")

    s = sub.add_parser("summary", help="totals per category")
    s.add_argument("-m", "--month", help="filter by month, YYYY-MM")

    e = sub.add_parser("export", help="print expenses as CSV")
    e.add_argument("-m", "--month")

    d = sub.add_parser("delete", help="delete an expense by id")
    d.add_argument("id", type=int)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    conn = db.connect(args.db)
    try:
        if args.command == "add":
            new_id = db.add_expense(conn, args.amount, args.category, args.note, args.date)
            print(f"Added expense #{new_id}")
        elif args.command == "list":
            print(report.format_table(db.list_expenses(conn, args.month, args.category)))
        elif args.command == "summary":
            print(report.format_summary(db.summary_by_category(conn, args.month)))
        elif args.command == "export":
            print(report.to_csv(db.list_expenses(conn, args.month)), end="")
        elif args.command == "delete":
            ok = db.delete_expense(conn, args.id)
            print("Deleted." if ok else "No expense with that id.")
            return 0 if ok else 1
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
