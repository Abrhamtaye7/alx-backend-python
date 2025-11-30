class Book:
    """
    Represents a book with a title, author, and availability status.
    """

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self._is_checked_out = False

    def check_out(self):
        """Mark the book as checked out."""
        self._is_checked_out = True

    def return_book(self):
        """Mark the book as available again."""
        self._is_checked_out = False

    def is_available(self):
        """Return True if the book is not checked out."""
        return not self._is_checked_out


class Library:
    """
    Represents a library that manages a collection of books.
    """

    def __init__(self):
        self._books = []

    def add_book(self, book):
        """Add a Book object to the library."""
        self._books.append(book)

    def check_out_book(self, title):
        """
        Check out a book by title if it is available.
        """
        for book in self._books:
            if book.title == title and book.is_available():
                book.check_out()
                return
        # If not found or already checked out, do nothing

    def return_book(self, title):
        """
        Return a book by title.
        """
        for book in self._books:
            if book.title == title and not book.is_available():
                book.return_book()
                return
        # If not found or already returned, do nothing

    def list_available_books(self):
        """Print all available books in '<title> by <author>' format."""
        for book in self._books:
            if book.is_available():
                print(f"{book.title} by {book.author}")
