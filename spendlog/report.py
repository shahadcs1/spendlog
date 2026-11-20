import csv
import io


def format_table(rows):
    if not rows:
        return "No expenses found."
    lines = [f"{'ID':<4} {'Date':<11} {'Amount':>9}  {'Category':<14} Note"]
    for r in rows:
        lines.append(
            f"{r['id']:<4} {r['spent_on']:<11} {r['amount']:>9.2f}  {r['category']:<14} {r['note']}"
        )
    return "\n".join(lines)


def format_summary(rows, width=30):
    if not rows:
        return "No expenses found."
    grand = sum(r["total"] for r in rows)
    biggest = max(r["total"] for r in rows)
    lines = []
    for r in rows:
        bar = "#" * max(1, round(r["total"] / biggest * width))
        pct = r["total"] / grand * 100
        lines.append(f"{r['category']:<14} {r['total']:>9.2f} {pct:>5.1f}%  {bar}")
    lines.append("-" * 50)
    lines.append(f"{'TOTAL':<14} {grand:>9.2f}")
    return "\n".join(lines)


def to_csv(rows):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "date", "amount", "category", "note"])
    for r in rows:
        writer.writerow([r["id"], r["spent_on"], r["amount"], r["category"], r["note"]])
    return buf.getvalue()
