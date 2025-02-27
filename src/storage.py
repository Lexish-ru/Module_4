import json
import os
from typing import List

from src.vacancy import Vacancy


class JSONStorage:
    """Класс для работы с JSON-хранилищем вакансий."""

    def __init__(self, filename: str = "vacancies.json"):
        self._filename = filename
        os.makedirs(os.path.dirname(self._filename), exist_ok=True)

    def save_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Сохраняет вакансии в JSON-файл, избегая дублирования."""
        existing_vacancies = self.load_vacancies()
        unique_vacancies = {v.name: v for v in existing_vacancies}
        for vacancy in vacancies:
            unique_vacancies[vacancy.name] = vacancy

        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump([vacancy.to_dict() for vacancy in unique_vacancies.values()], file, ensure_ascii=False, indent=4)

    def load_vacancies(self) -> List[Vacancy]:
        """Загружает список вакансий из JSON-файла."""
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Vacancy.from_dict(vacancy) for vacancy in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def clear_storage(self) -> None:
        """Очищает хранилище вакансий."""
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    def filter_vacancies_by_salary(self, min_salary: int) -> List[Vacancy]:
        """Фильтрует вакансии, оставляя только те, где зарплата выше указанного минимума."""
        vacancies = self.load_vacancies()
        return [vacancy for vacancy in vacancies if (vacancy._salary_from and vacancy._salary_from >= min_salary)]

    def sort_vacancies_by_salary(self, descending: bool = True) -> List[Vacancy]:
        """Сортирует вакансии по зарплате (по умолчанию по убыванию)."""
        vacancies = self.load_vacancies()
        return sorted(vacancies, key=lambda v: v.salary_from or 0, reverse=descending)

    def delete_vacancy(self, vacancy_name: str) -> None:
        """Удаляет вакансию по названию."""
        vacancies = self.load_vacancies()
        vacancies = [vacancy for vacancy in vacancies if vacancy._name != vacancy_name]
        self.save_vacancies(vacancies)
