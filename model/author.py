from typing import Optional
from author_dao import AuthorDAO


class Author:
    dao = None  # to be set with an AuthorDAO instance

    def __init__(self, id: Optional[int], name: str):
        self.id = id
        self.name = name

    @classmethod
    def set_dao(cls, dao: AuthorDAO):
        cls.dao = dao

    def save(self):
        if self.id is None:
            self.id = self.dao.create_author(self.name)
        else:
            self.dao.update_author(self.id, self.name)

    def delete(self):
        if self.id is not None:
            self.dao.delete_author(self.id)
            self.id = None

    @classmethod
    def get(cls, author_id: int) -> Optional["Author"]:
        data = cls.dao.get_author(author_id)
        return cls(data["id"], data["name"]) if data else None

    @classmethod
    def all(cls) -> list["Author"]:
        return [cls(a["id"], a["name"]) for a in cls.dao.list_authors()]
