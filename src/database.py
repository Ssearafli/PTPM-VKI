import sqlite3


class TriangleDatabase:
    def __init__(self, database_path="triangles.sqlite3"):
        self.database_path = database_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _create_table(self):
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS triangles (
                    side_a TEXT NOT NULL,
                    side_b TEXT NOT NULL,
                    side_c TEXT NOT NULL,
                    triangle_type TEXT NOT NULL,
                    error_message TEXT NOT NULL,
                    coordinates TEXT NOT NULL,
                    PRIMARY KEY (side_a, side_b, side_c)
                )
            """)

    def add(self, side_a, side_b, side_c, triangle_type, error_message, coordinates):
        coordinates_text = repr(coordinates)

        with self._connect() as connection:
            connection.execute("""
                INSERT OR REPLACE INTO triangles
                (side_a, side_b, side_c, triangle_type,
                 error_message, coordinates)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                side_a,
                side_b,
                side_c,
                triangle_type,
                error_message,
                coordinates_text
            ))

    def get(self, side_a, side_b, side_c):
        with self._connect() as connection:
            row = connection.execute("""
                SELECT triangle_type, error_message, coordinates
                FROM triangles
                WHERE side_a = ? AND side_b = ? AND side_c = ?
            """, (side_a, side_b, side_c)).fetchone()

        if row is None:
            return None

        # Формат координат создан программой, а не пользователем.
        coordinates = eval(row[2], {"__builtins__": {}})
        return {
            "triangle_type": row[0],
            "error_message": row[1],
            "coordinates": coordinates
        }

    def delete(self, side_a, side_b, side_c):
        with self._connect() as connection:
            cursor = connection.execute("""
                DELETE FROM triangles
                WHERE side_a = ? AND side_b = ? AND side_c = ?
            """, (side_a, side_b, side_c))
            return cursor.rowcount > 0
