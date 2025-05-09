import sqlite3
from typing import Optional, List, Dict


class BookDAO:
    def __init__(self, db_path: str):
        self.__conn = sqlite3.connect(db_path)
        self.__conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.__conn.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )""")
        self.__conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id)
        )""")
        self.__conn.commit()

    def create_book(self, name: str, description: str, author_id: int) -> int:
        cursor = self.__conn.execute(
            "INSERT INTO books (name, description, author_id) VALUES (?, ?, ?)",
            (name, description, author_id)
        )
        self.__conn.commit()
        return cursor.lastrowid

    def get_book(self, book_id: int) -> Optional[Dict]:
        cursor = self.__conn.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_books_by_author_name(self, author_name: str) -> List[Dict]:
        cursor = self.__conn.execute("""
            SELECT books.*
            FROM books
            JOIN authors ON books.author_id = authors.id
            WHERE authors.name = ?
        """, (author_name,))
        return [dict(row) for row in cursor.fetchall()]

    def list_books(self) -> List[Dict]:
        cursor = self.__conn.execute("SELECT * FROM books")
        return [dict(row) for row in cursor.fetchall()]

    def update_book(self, book_id: int, name: Optional[str] = None,
                    description: Optional[str] = None, author_id: Optional[int] = None) -> bool:
        current = self.get_book(book_id)
        if not current:
            return False
        name = name or current["name"]
        description = description if description is not None else current["description"]
        author_id = author_id if author_id is not None else current["author_id"]
        self.__conn.execute(
            "UPDATE books SET name = ?, description = ?, author_id = ? WHERE id = ?",
            (name, description, author_id, book_id)
        )
        self.__conn.commit()
        return True

    def delete_book(self, book_id: int) -> bool:
        cursor = self.__conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.__conn.commit()
        return cursor.rowcount > 0

    def _del__(self):
        self.__conn.close()
