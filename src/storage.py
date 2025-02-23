import json
import os
from typing import List
from vacancy import Vacancy


class JSONStorage:
    """Класс для сохранения и загрузки вакансий в JSON"""

    def __init__(self, filename: str = "../output/vacansies.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def save_vacansies(self, vacancies: List[Vacancy]) -> None:
        """Сохраняет вакансии в JSON-файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([vacancy.__dict__ for vacancy in vacancies], file, ensure_ascii=False, indent=4)

    def load_vacancies(self) -> List[Vacancy]:
        """Загружает список вакансий из JSON-файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Vacancy(**vacancy) for vacancy in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def clear_storage(self) -> None:
        """Очищает хранилище вакансий."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

