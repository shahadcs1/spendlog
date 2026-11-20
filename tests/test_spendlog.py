import unittest

from spendlog import db, report


class SpendlogTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect(":memory:")
        db.add_expense(self.conn, 50, "Food", "lunch", "2026-11-02")
        db.add_expense(self.conn, 150, "transport", "", "2026-11-03")
        db.add_expense(self.conn, 25, "food", "coffee", "2026-12-01")

    def test_category_is_normalized(self):
        self.assertEqual(len(db.list_expenses(self.conn, category="FOOD")), 2)

    def test_month_filter(self):
        self.assertEqual(len(db.list_expenses(self.conn, month="2026-11")), 2)

    def test_summary_sorted_by_total(self):
        rows = db.summary_by_category(self.conn, "2026-11")
        self.assertEqual([r["category"] for r in rows], ["transport", "food"])

    def test_rejects_bad_amount_and_date(self):
        with self.assertRaises(ValueError):
            db.add_expense(self.conn, -5, "food")
        with self.assertRaises(ValueError):
            db.add_expense(self.conn, 5, "food", spent_on="02/11/2026")

    def test_delete(self):
        self.assertTrue(db.delete_expense(self.conn, 1))
        self.assertFalse(db.delete_expense(self.conn, 999))

    def test_csv_export_has_header(self):
        out = report.to_csv(db.list_expenses(self.conn))
        self.assertTrue(out.startswith("id,date,amount,category,note"))


if __name__ == "__main__":
    unittest.main()
