from storage import Storage


class LibraryManager:
    def __init__(self, storage: Storage):
        """
        Класс для управления библиотекой книг.
        """
        self.storage = storage

    def add_book(self, title: str, author: str, year: str) -> None:
        """
        Добавляет новую книгу в библиотеку.
        """
        if not year.isdigit():
            raise ValueError("Год должен быть числом.")

        books = self.get_all_books()
        new_book = {
            "id": self._generate_id(),
            "title": title.strip(),
            "author": author.strip(),
            "year": int(year),
            "status": "в наличии",
        }
        books.append(new_book)
        self.storage.save_data(books)

    def get_book_by_id(self, book_id: int) -> dict:
        """
        Получает книгу по её ID.
        """
        books = self.get_all_books()
        book = next((b for b in books if b["id"] == book_id), None)
        if book is None:
            raise KeyError(f"Книга с ID {book_id} не найдена.")
        return book

    def update_status_by_book_id(self, book_id: int, new_status: str) -> None:
        """
        Обновляет статус книги по её ID.
        """
        book = self.get_book_by_id(book_id)
        book["status"] = new_status
        self._save_books_with_update(book)

    def delete_book_by_id(self, book_id: int) -> None:
        """
        Удаляет книгу по её ID.
        """
        books = self.get_all_books()
        new_books = [book for book in books if book["id"] != book_id]
        if len(new_books) == len(books):
            raise KeyError(f"Книга с ID {book_id} не найдена.")
        self.storage.save_data(new_books)

    def search_books_by_value(self, value: str) -> list[dict]:
        """
        Ищет книги по значению в названии, авторе или году издания.
        """
        books = self.get_all_books()
        value = value.lower().strip()
        return [
            book
            for book in books
            if value in book["title"].lower()
            or value in book["author"].lower()
            or value == str(book["year"])
        ]

    def get_all_books(self) -> list[dict]:
        """
        Возвращает все книги из библиотеки.
        """
        return self.storage.load_data()

    def _generate_id(self) -> int:
        """
        Генерирует уникальный ID для новой книги.
        """
        books = self.get_all_books()
        return max((book["id"] for book in books), default=0) + 1

    def _save_books_with_update(self, updated_book: dict) -> None:
        """
        Сохраняет изменения книги в хранилище.
        """
        books = self.get_all_books()
        for i, book in enumerate(books):
            if book["id"] == updated_book["id"]:
                books[i] = updated_book
                break
        self.storage.save_data(books)
