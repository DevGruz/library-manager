import sys

from library_manager import LibraryManager
from storage import Storage
from interfaces import InterfacePython, CURSES_AVAILABLE

if CURSES_AVAILABLE:
    from interfaces import InterfaceCurses


def init_curses(stdscr):
    import curses

    min_height = 11

    while True:
        stdscr.clear()
        max_y, _ = stdscr.getmaxyx()

        if max_y < min_height:
            stdscr.addstr(
                0, 0, f"Увеличьте высоту терминала минимум до {min_height} строк."
            )
            stdscr.addstr(1, 0, f"Текущая высота: {max_y}.")
            stdscr.refresh()
            curses.napms(100)
        else:
            break
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.keypad(True)

def create_interface(library_manager):
    """
    Создает интерфейс в зависимости от доступности curses.
    """
    try:
        import curses

        curses.wrapper(lambda stdscr: InterfaceCurses(stdscr, library_manager))
        return lambda: curses.wrapper(main_with_curses)
    except ImportError:
        return lambda: main_with_python(library_manager)


def main_with_curses(stdscr):
    """
    Основной цикл работы с использованием curses.
    """
    import curses

    init_curses(stdscr)
    storage = Storage("books.json")
    library_manager = LibraryManager(storage)
    interface = InterfaceCurses(stdscr, library_manager)
    try:
        run_application(interface)
    except curses.error:
        ...


def main_with_python(library_manager):
    """
    Основной цикл работы без использования curses.
    """
    interface = InterfacePython(library_manager)
    run_application(interface)


def run_application(interface):
    status_message = None

    while True:
        interface.show_main_menu(status_message)
        choice = interface.get_value()
        status_message = None

        match choice:
            case "1":
                status_message = interface.add_book()
            case "2":
                status_message = interface.delete_book_by_id()
            case "3":
                interface.show_books_search()
            case "4":
                interface.show_all_books()
            case "5":
                status_message = interface.change_book_status()
            case "6":
                break


if __name__ == "__main__":
    try:
        storage = Storage("books.json")
        library_manager = LibraryManager(storage)
        selected_interface = create_interface(library_manager)
        selected_interface()
    except KeyboardInterrupt:
        sys.exit()
