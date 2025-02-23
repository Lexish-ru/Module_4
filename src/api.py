import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from vacancy import Vacancy
from storage import JSONStorage


class BaseAPI(ABC):
    """Абстрактный класс для работы с API вакансий"""

    @abstractmethod
    def get_vacancies(self, keyword: str, area: int = 1, per_page: int = 10) -> List[Vacancy]:
        """Метод для получения вакансий. Должен быть реализован в наследниках."""
        pass


class HeadHunterAPI(BaseAPI):
    """Класс для работы с API hh.ru"""

    BASE_URL: str = "https://api.hh.ru/vacancies"

    def get_vacancies(self, keyword: str, area: int = 2, per_page: int = 10) -> List[Vacancy]:
        """Получает вакансии с hh.ru по ключевому слову и возвращает список объектов Vacancy"""
        params: Dict[str, Any] = {
            "text": keyword,
            "area": area,
            "per_page": per_page
        }

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
                responsibility=item.get("snippet", {}).get("responsibility", "Не указано")
            )
            vacancies.append(vacancy)

        return vacancies


if __name__ == "__main__":
    hh = HeadHunterAPI()
    vacancies = hh.get_vacancies("Python разработчик", area=2, per_page=5)

    storage = JSONStorage()
    storage.save_vacansies(vacancies)
    print("Вакансии сохранены в vacansies.json")

    loaded_vacancies = storage.load_vacancies()
    print("Загруженные вакансии из JSON:")

    for vacancy in loaded_vacancies:
        print(vacancy)
