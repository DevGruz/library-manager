import sys
import unittest
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.library_manager import LibraryManager
from src.storage import Storage


class TestLibraryManager(unittest.TestCase):
    def setUp(self):
        self.storage = Storage("test_books.json")
        self.library_manager = LibraryManager(self.storage)

    def tearDown(self):
        if os.path.exists("test_books.json"):
            os.remove("test_books.json")

    def test_add_book(self):
        """Тест добавления книги."""
        self.library_manager.add_book("Test Book", "Author", "2024")
        books = self.library_manager.get_all_books()
        self.assertEqual(len(books), 1)

    def test_delete_book(self):
        """Тест удаления книги."""
        self.library_manager.add_book("Test Book", "Author", "2024")
        self.library_manager.delete_book_by_id(1)
        self.assertEqual(len(self.library_manager.get_all_books()), 0)

    def test_change_book_status(self):
        """Тест изменения статуса книги."""
        self.library_manager.add_book("Test Book", "Author", "2024")
        self.library_manager.update_status_by_book_id(1, "выдана")
        books = self.library_manager.get_all_books()
        self.assertEqual(books[0]["status"], "выдана")


if __name__ == "__main__":
    unittest.main()
