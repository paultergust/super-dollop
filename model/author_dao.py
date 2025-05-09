import sqlite3
from typing import Optional, List, Dict


class AuthorDAO:
    def __init__(self, db_path: str):
        self.__conn = sqlite3.connect(db_path)
        self.__conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.__conn.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )""")
        self.__conn.commit()

    def create_author(self, name: str) -> int:
        cursor = self.__conn.execute(
            "INSERT INTO authors (name) VALUES (?)",
            (name,)
        )
        self.__conn.commit()
        return cursor.lastrowid

    def get_author(self, author_id: int) -> Optional[Dict]:
        cursor = self.__conn.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def list_authors(self) -> List[Dict]:
        cursor = self.__conn.execute("SELECT * FROM authors")
        return [dict(row) for row in cursor.fetchall()]

    def update_author(self, author_id: int, name: str) -> bool:
        cursor = self.__conn.execute(
            "UPDATE authors SET name = ? WHERE id = ?",
            (name, author_id)
        )
        self.__conn.commit()
        return cursor.rowcount > 0

    def delete_author(self, author_id: int) -> bool:
        cursor = self.__conn.execute("DELETE FROM authors WHERE id = ?", (author_id,))
        self.__conn.commit()
        return cursor.rowcount > 0

    def __del__(self):
        self.__conn.close()
