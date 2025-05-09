
class BookView:
    @staticmethod
    def prompt_new_book():
        name = input("Enter book title: ")
        description = input("Enter book description: ")
        author_id = int(input("Enter author ID: "))
        return name, description, author_id

    @staticmethod
    def show_books(books):
        if not books:
            print("No books found.")
        else:
            for book in books:
                print(f"[{book.id}] {book.name} ({book.author.name}) - {book.description}")

    @staticmethod
    def show_book_added():
        print("Book added.")

    @staticmethod
    def show_invalid_author():
        print("Invalid author ID.")
