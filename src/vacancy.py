from typing import Optional


class Vacancy:
    """Класс для представления вакансии."""

    def __init__(self, name: str, url: str, salary_from: Optional[int], salary_to: Optional[int],
                 currency: Optional[str], employer: str, requirement: str, responsibility: str):
        self.name = name
        self.url = url
        self.salary_from = salary_from if salary_from is not None else 0
        self.salary_to = salary_to if salary_to is not None else 0
        self.currency = currency if currency is not None else "Не указано"
        self.employer = employer
        self.requirement = requirement
        self.responsibility = responsibility

    def __str__(self) -> str:
        salary_info = f"{self.salary_from} - {self.salary_to} {self.currency}" \
            if self.salary_from or self.salary_to else "зарплата не указана"
        return (f"Вакансия: {self.name}\n"
                f"Компания: {self.employer}\n"
                f"Зарплата: {salary_info}\n"
                f"Требования: {self.requirement}\n"
                f"Обязанности: {self.responsibility}\n"
                f"Ссылка: {self.url}\n")

    def __lt__(self, other: "Vacancy") -> bool:
        return self.salary_from < other.salary_from

    def __gt__(self, other: "Vacancy") -> bool:
        return self.salary_from > other.salary_from