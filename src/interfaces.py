import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

try:
    import curses

    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False

from typing import Optional
from library_manager import LibraryManager


@dataclass
class StatusMessageCurses:
    text: str = ""
    color_pair: int = 0


class BaseInterface(ABC):
    MENU_ITEMS = [
        "1. Добавить книгу",
        "2. Удалить книгу",
        "3. Найти книгу",
        "4. Показать все книги",
        "5. Изменить статус книги",
        "6. Выйти",
    ]

    def __init__(self, lib_manager):
        self.lib_manager = lib_manager

    @abstractmethod
    def show_main_menu(self, message: Optional[str] = None):
        """
        Отображает главное меню с дополнительным сообщением.
        """
        pass

    @abstractmethod
    def add_book(self):
        """
        Добавляет книгу, собирая данные от пользователя.
        """
        pass

    @abstractmethod
    def get_value(self):
        """
        Получает ввод пользователя.
        """
        pass

    @abstractmethod
    def delete_book_by_id(self):
        """
        Удаляет книгу по ID.
        """
        pass

    @abstractmethod
    def change_book_status(self):
        """
        Изменяет статус книги по ID.
        """
        pass

    @abstractmethod
    def show_all_books(self):
        """
        Пагинация списка всех книг.
        """
        pass

    @abstractmethod
    def show_books_search(self):
        """
        Пагинация списка книг по результатам поиска.
        """
        pass

    @abstractmethod
    def _show_books_with_pagination(self, books: list[dict]):
        """
        Унифицированный метод для отображения книг с пагинацией.
        """
        pass

    @abstractmethod
    def _get_user_input(self, prompt: str) -> str:
        """
        Запрашивает ввод у пользователя с подсказкой.
        """
        pass

    @abstractmethod
    def _clear_screen(self):
        """
        Очищает экран.
        """
        pass

    @abstractmethod
    def _add_text(self, *args, **kwargs):
        """
        Добавляет текст на экран.
        """
        pass


class InterfacePython(BaseInterface):
    def show_main_menu(self, message: str = None):
        self._clear_screen()
        self._add_text("Управление библиотекой:\n")

        for item in self.MENU_ITEMS:
            self._add_text(item)

        if message:
            self._add_text(f"\n{message}")

    def get_value(self) -> str:
        return input()

    def add_book(self) -> str:
        self._clear_screen()
        title = self._get_user_input("Введите название книги:")
        author = self._get_user_input("Введите автора книги:")
        year = self._get_user_input("Введите год издания книги:")

        while not year.isdigit():
            year = self._get_user_input("Введите корректный год издания книги:")

        while True:
            self._clear_screen()
            self._add_text("Данные книги:")
            self._add_text(f"Название: {title}")
            self._add_text(f"Автор: {author}")
            self._add_text(f"Год издания: {year}")
            self._add_text("\n1. Сохранить книгу")
            self._add_text("2. Отменить")
            choice = self.get_value()
            if choice == "1":
                self.lib_manager.add_book(title, author, year)
                return "Книга успешно добавлена"
            elif choice == "2":
                return "Добавление книги отменено"

    def delete_book_by_id(self) -> str:
        book_id = self._get_user_input("Введите ID книги, которую необходимо удалить:")
        try:
            self.lib_manager.delete_book_by_id(int(book_id))
            return "Книга успешно удалена"
        except ValueError:
            return "Ошибка: некорректный ID"
        except KeyError:
            return "Книга с таким ID не найдена"

    def change_book_status(self) -> str:
        book_id = self._get_user_input(
            "Введите ID книги, у которой нужно изменить статус:"
        )
        try:
            book = self.lib_manager.get_book_by_id(int(book_id))
        except (ValueError, KeyError):
            return StatusMessageCurses("Ошибка: некорректный или несуществующий ID", 2)

        current_status = book["status"]
        new_status = "выдана" if current_status == "в наличии" else "в наличии"
        self._clear_screen()
        self._add_text(f"Название книги: {book['title']}")
        self._add_text(f"Автор книги: {book['author']}")
        self._add_text(f"Текущий статус: {current_status}")
        self._add_text(f"\n1. Изменить статус на '{new_status}'")
        self._add_text("2. Отменить")

        while True:
            choice = self.get_value()
            if choice == "1":
                self.lib_manager.update_status_by_book_id(book["id"], new_status)
                return "Статус успешно изменен"
            elif choice == "2":
                return "Изменение статуса отменено"

    def show_all_books(self):
        self._show_books_with_pagination(self.lib_manager.get_all_books())

    def show_books_search(self):
        query = self._get_user_input("Введите строку для поиска:\n")
        books = self.lib_manager.search_books_by_value(query)
        self._show_books_with_pagination(books)

    def _show_books_with_pagination(self, books: list[dict]):
        """
        Унифицированный метод для отображения книг с пагинацией.
        """
        total_books = len(books)
        books_per_page = 5
        current_page = 0
        total_pages = (total_books - 1) // books_per_page + 1

        while True:
            self._clear_screen()
            self._add_text(
                f"Книги: страница {current_page + bool(total_books)} из {total_pages}\n"
            )

            start = current_page * books_per_page
            end = min(start + books_per_page, total_books)
            for idx, book in enumerate(books[start:end], start=2):
                self._add_text(
                    f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                    f"Год: {book['year']}, Статус: {book['status']}",
                )

            self._add_text("\n1. Следующая страница")
            self._add_text("2. Предыдущая страница")
            self._add_text("3. Вернуться в главное меню")

            key = self.get_value()
            if key == "1" and current_page < total_pages - 1:
                current_page += 1
            elif key == "2" and current_page > 0:
                current_page -= 1
            elif key == "3":
                break

    def _get_user_input(self, prompt: str) -> str:
        self._clear_screen()
        print(prompt)
        user_input = input()
        return user_input

    def _add_text(self, text: str):
        print(text)

    def _clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")


if CURSES_AVAILABLE:

    class InterfaceCurses(BaseInterface):
        def __init__(self, stdscr, lib_manager: LibraryManager):
            self.stdscr = stdscr
            self.lib_manager = lib_manager

        def show_main_menu(self, message: StatusMessageCurses = None):
            self._clear_screen()
            self._add_text(0, 0, "Управление библиотекой:")
            for idx, item in enumerate(self.MENU_ITEMS, start=2):
                self._add_text(idx, 0, item)

            if message:
                self._add_text(
                    len(self.MENU_ITEMS) + 3,
                    0,
                    message.text,
                    color_pair=message.color_pair,
                )
            
            self.stdscr.refresh()

        def get_value(self) -> str:
            curses.curs_set(0)
            return self.stdscr.getkey()

        def add_book(self) -> str:
            self._clear_screen()
            title = self._get_user_input("Введите название книги:\n")
            author = self._get_user_input("Введите автора книги:\n")
            year = self._get_user_input("Введите год издания книги:\n")

            while not year.isdigit():
                year = self._get_user_input("Введите корректный год издания книги:\n")

            self._clear_screen()
            self._add_text(0, 0, "Данные книги:")
            self._add_text(2, 0, f"Название: {title}")
            self._add_text(3, 0, f"Автор: {author}")
            self._add_text(4, 0, f"Год издания: {year}")
            self._add_text(6, 0, "1. Сохранить книгу")
            self._add_text(7, 0, "2. Отменить")

            curses.noecho()
            while True:
                choice = self.get_value()
                if choice == "1":
                    self.lib_manager.add_book(title, author, year)
                    return StatusMessageCurses("Книга успешно добавлена", 1)
                elif choice == "2":
                    return StatusMessageCurses("Добавление книги отменено", 1)

        def delete_book_by_id(self) -> str:
            book_id = self._get_user_input(
                "Введите ID книги, которую необходимо удалить:\n"
            )
            try:
                self.lib_manager.delete_book_by_id(int(book_id))
                return StatusMessageCurses("Книга успешно удалена", 1)
            except ValueError:
                return StatusMessageCurses("Ошибка: некорректный ID", 2)
            except KeyError:
                return StatusMessageCurses("Книга с таким ID не найдена", 2)

        def change_book_status(self) -> str:
            book_id = self._get_user_input(
                "Введите ID книги, у которой нужно изменить статус:\n"
            )
            try:
                book = self.lib_manager.get_book_by_id(int(book_id))
            except (ValueError, KeyError):
                return StatusMessageCurses(
                    "Ошибка: некорректный или несуществующий ID", 2
                )

            current_status = book["status"]
            new_status = "выдана" if current_status == "в наличии" else "в наличии"
            self._clear_screen()
            self._add_text(0, 0, f"Название книги: {book['title']}")
            self._add_text(1, 0, f"Автор книги: {book['author']}")
            self._add_text(2, 0, f"Текущий статус: {current_status}")
            self._add_text(4, 0, f"1. Изменить статус на '{new_status}'")
            self._add_text(5, 0, "2. Отменить")

            while True:
                choice = self.get_value()
                if choice == "1":
                    self.lib_manager.update_status_by_book_id(book["id"], new_status)
                    return StatusMessageCurses("Статус успешно изменен", 1)
                elif choice == "2":
                    return StatusMessageCurses("Изменение статуса отменено", 1)

        def show_all_books(self):
            self._show_books_with_pagination(self.lib_manager.get_all_books())

        def show_books_search(self):
            query = self._get_user_input("Введите строку для поиска:\n")
            books = self.lib_manager.search_books_by_value(query)
            self._show_books_with_pagination(books)

        def _clear_screen(self):
            self.stdscr.clear()
            self.stdscr.refresh()

        def _add_text(self, y: int, x: int, text: str, color_pair: int = 0):
            self.stdscr.addstr(y, x, text, curses.color_pair(color_pair))

        def _get_user_input(self, prompt: str) -> str:
            curses.echo()
            curses.curs_set(1)
            self._clear_screen()
            self._add_text(0, 0, prompt)
            user_input = self.stdscr.getstr().decode()
            curses.noecho()
            return user_input

        def _show_books_with_pagination(self, books: list[dict]):
            total_books = len(books)
            books_per_page = 5
            current_page = 0
            total_pages = (total_books - 1) // books_per_page + 1

            while True:
                self._clear_screen()
                self._add_text(
                    0,
                    0,
                    f"Книги: страница {current_page + bool(total_books)} из {total_pages}",
                )

                start = current_page * books_per_page
                end = min(start + books_per_page, total_books)
                for idx, book in enumerate(books[start:end], start=2):
                    self._add_text(
                        idx,
                        0,
                        f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                        f"Год: {book['year']}, Статус: {book['status']}",
                    )

                self._add_text(8, 0, "1. Следующая страница")
                self._add_text(9, 0, "2. Предыдущая страница")
                self._add_text(10, 0, "3. Вернуться в главное меню")

                key = self.get_value()
                if key == "1" and current_page < total_pages - 1:
                    current_page += 1
                elif key == "2" and current_page > 0:
                    current_page -= 1
                elif key == "3":
                    break
