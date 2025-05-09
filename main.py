from model import AuthorDAO, BookDAO, Author, Book
from view import AuthorView, BookView, MainMenuView


def main():
    db_path = "library.db"
    author_dao = AuthorDAO(db_path)
    book_dao = BookDAO(db_path)

    Author.set_dao(author_dao)
    Book.set_dao(book_dao)

    while True:
        MainMenuView.show_options()  # Display the options from the view

        choice = input("Choose an option: ")

        if choice == "1":
            authors = Author.all()
            AuthorView.show_authors(authors)

        elif choice == "2":
            name = AuthorView.prompt_new_author()
            author = Author(None, name)
            author.save()
            AuthorView.show_author_added()

        elif choice == "3":
            books = Book.all()
            BookView.show_books(books)

        elif choice == "4":
            name, description, author_id = BookView.prompt_new_book()
            author = Author.get(author_id)
            if author:
                book = Book(None, name, description, author)
                book.save()
                BookView.show_book_added()
            else:
                BookView.show_invalid_author()

        elif choice == "5":
            name = input("Enter author name: ")
            books = Book.by_author_name(name)
            BookView.show_books(books)

        elif choice == "0":
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
