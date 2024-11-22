import json
import os
from typing import Optional


class Storage:
    def __init__(self, data_file: str):
        """
        Класс для работы с хранилищем данных.
        """
        self.data_file = data_file

    def load_data(self) -> list[Optional[dict]]:
        """
        Загружает данные из файла.
        """
        if not os.path.exists(self.data_file):
            return []

        try:
            with open(self.data_file, mode="r", encoding="UTF-8") as file:
                data = json.load(file)
                return data
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(
                f"Ошибка при загрузке данных из файла '{self.data_file}': {e}"
            )

    def save_data(self, data: list[Optional[dict]]) -> None:
        """
        Сохраняет данные в файл.
        """
        try:
            with open(self.data_file, mode="w", encoding="UTF-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except IOError as e:
            raise RuntimeError(
                f"Ошибка при сохранении данных в файл '{self.data_file}': {e}"
            )
