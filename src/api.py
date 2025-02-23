from http.client import responses

import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_vacancies(self, keyword: str, area: int = 1, per_page: int = 10) -> List[Dict[str, Any]]:
        """Метод получения вакансий. Должен быть реализован в наследниках"""
        pass

class HeadHunteAPI(BaseAPI):
    """Класс для работы с API HH.ru"""

    BASE_URL: str = "https://api.hh.ru/vacancies"

    def get_vacancies(self, keyword: str, area: int = 1, per_page: int = 10)-> List[Dict[str, Any]]:
        """получает вакансии по ключевому слову"""
        params: Dict[str, Any] = {
            "text": keyword,
            "area": area,
            "per_page": per_page
        }

        response: requests.Response = requests.get(self.BASE_URL, params=params)\

        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            return []

        data: Dict[str,Any] = response.json()
        vacancies: List[Dict[str, Any]] = []

        for item in data.get("items", []):
            vacancies.append({
                "name": item.get("name", "Без названия"),
                "url": item.get("alternate_url", "Нет ссылки"),
                "salary": item.get("salary"),
                "employer": item.get("employer", {}).get("name", "Не указан"),
                "requirement": item.get("snippet", {}).get("requirement", "Не указано"),
                "responsibility": item.get("snippet", {}).get("responsibility", "Не указано")
            })

        return vacancies

if __name__ == "__main__":
    hh = HeadHunteAPI()
    vacancies = hh.get_vacancies("Python разработчик", area=2, per_page=5)

    for v in vacancies:
        print(v)


