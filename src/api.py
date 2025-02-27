from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests

from src.vacancy import Vacancy


class BaseAPI(ABC):
    """Абстрактный класс для работы с API вакансий"""

    @abstractmethod
    def _get_vacancies(self, keyword: str, area: int = 1, per_page: int = 10) -> List[Vacancy]:
        """Приватный метод для получения вакансий. Должен быть реализован в наследниках."""
        pass


class HeadHunterAPI(BaseAPI):
    """Класс для работы с API hh.ru"""

    BASE_URL: str = "https://api.hh.ru/vacancies"

    def _get_vacancies(self, keyword: str, area: int = 2, per_page: int = 10) -> List[Vacancy]:
        """Получает вакансии с hh.ru по ключевому слову и возвращает список объектов Vacancy"""
        params: Dict[str, Any] = {"text": keyword, "area": area, "per_page": per_page}

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            return []

        data: Dict[str, Any] = response.json()
        vacancies: List[Vacancy] = []

        for item in data.get("items", []):
            salary_info = item.get("salary") or {}
            vacancy = Vacancy(
                name=item.get("name", "Без названия"),
                url=item.get("alternate_url", "Нет ссылки"),
                salary_from=salary_info.get("from"),
                salary_to=salary_info.get("to"),
                currency=salary_info.get("currency"),
                employer=item.get("employer", {}).get("name", "Не указан"),
                requirement=item.get("snippet", {}).get("requirement", "Не указано"),
                responsibility=item.get("snippet", {}).get("responsibility", "Не указано"),
            )
            vacancies.append(vacancy)

        return vacancies
