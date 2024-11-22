import sys
import unittest
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = Storage("test_books.json")

    def tearDown(self):
        if os.path.exists("test_books.json"):
            os.remove("test_books.json")

    def test_save_and_load_books(self):
        """Тест сохранения и загрузки книг."""
        books = [
            {"id": 1, "title": "Book 1", "author": "Author", "status": "выдана"}
        ]
        self.storage.save_data(books)
        loaded_books = self.storage.load_data()
        self.assertEqual(loaded_books, books)

    def test_load_books_empty_file(self):
        """Тест загрузки из пустого файла."""
        books = self.storage.load_data()
        self.assertListEqual(books, [])


if __name__ == "__main__":
    unittest.main()
