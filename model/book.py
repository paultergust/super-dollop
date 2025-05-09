from typing import Optional
from book_dao import BookDAO
from author_model import Author


class Book:
    dao = None  # to be set with a BookDAO instance

    def __init__(self, id: Optional[int], name: str, description: str, author: Author):
        self.id = id
        self.name = name
        self.description = description
        self.author = author  # this is an Author instance

    @classmethod
    def set_dao(cls, dao: BookDAO):
        cls.dao = dao

    def save(self):
        if not self.author or not self.author.id:
            raise ValueError("Author must be saved before saving a Book")
        if self.id is None:
            self.id = self.dao.create_book(self.name, self.description, self.author.id)
        else:
            self.dao.update_book(self.id, self.name, self.description, self.author.id)

    def delete(self):
        if self.id is not None:
            self.dao.delete_book(self.id)
            self.id = None

    @classmethod
    def get(cls, book_id: int) -> Optional["Book"]:
        data = cls.dao.get_book(book_id)
        if data:
            author = Author.get(data["author_id"])
            return cls(data["id"], data["name"], data["description"], author)
        return None

    @classmethod
    def all(cls) -> list["Book"]:
        books = cls.dao.list_books()
        return [
            cls(b["id"], b["name"], b["description"], Author.get(b["author_id"]))
            for b in books
        ]

    @classmethod
    def by_author_name(cls, author_name: str) -> list["Book"]:
        books = cls.dao.get_books_by_author_name(author_name)
        return [
            cls(b["id"], b["name"], b["description"], Author.get(b["author_id"]))
            for b in books
        ]
