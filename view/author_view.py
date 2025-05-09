
class AuthorView:
    @staticmethod
    def prompt_new_author():
        name = input("Enter author name: ")
        return name

    @staticmethod
    def show_authors(authors):
        if not authors:
            print("No authors found.")
        else:
            for author in authors:
                print(f"[{author.id}] {author.name}")

    @staticmethod
    def show_author_added():
        print("Author added.")
