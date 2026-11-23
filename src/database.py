import sqlite3

class TriangleDatabase:
    def __init__(self, db_path="triangle.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side_a TEXT NOT NULL,
                side_b TEXT NOT NULL,
                side_c TEXT NOT NULL,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (side_a, side_b, side_c)
            )
        """)
        self.conn.commit()

    def add_record(self, side_a, side_b, side_c, triangle_type, error_message=""):
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
            (side_a, side_b, side_c, triangle_type, error_message),
        )
        self.conn.commit()

    def get_record(self, side_a, side_b, side_c):
        cur = self.conn.execute(
            "SELECT triangle_type, error_message FROM triangles "
            "WHERE side_a=? AND side_b=? AND side_c=?",
            (side_a, side_b, side_c),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return {"triangle_type": row["triangle_type"], "error_message": row["error_message"]}

    def delete_record(self, side_a, side_b, side_c):
        self.conn.execute(
            "DELETE FROM triangles WHERE side_a=? AND side_b=? AND side_c=?",
            (side_a, side_b, side_c),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()