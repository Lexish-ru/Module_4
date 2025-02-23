import pytest
from unittest.mock import patch, Mock
from src.api import HeadHunterAPI
from src.vacancy import Vacancy
import requests


def test_hh_api_get_vacancies():
    """Тест получения вакансий через HeadHunterAPI с использованием unittest.mock."""
    mock_response = {
        "items": [
            {
                "name": "Python Developer",
                "alternate_url": "https://example.com",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "employer": {"name": "CompanyX"},
                "snippet": {"requirement": "Python, Django", "responsibility": "Backend development"}
            }
        ]
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_response)
        hh = HeadHunterAPI()
        vacancies = hh.get_vacancies("Python Developer", area=1, per_page=1)

        assert len(vacancies) == 1
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].name == "Python Developer"
        assert vacancies[0].salary_from == 100000
        assert vacancies[0].salary_to == 150000
        assert vacancies[0].currency == "RUR"
        assert vacancies[0].employer == "CompanyX"
        assert vacancies[0].requirement == "Python, Django"
        assert vacancies[0].responsibility == "Backend development"


def test_hh_api_no_results():
    """Тест обработки ситуации, когда API возвращает пустой список вакансий."""
    mock_response = {"items": []}

    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_response)
        hh = HeadHunterAPI()
        vacancies = hh.get_vacancies("Non-existent Job", area=1, per_page=1)

        assert vacancies == []


def test_hh_api_invalid_response():
    """Тест обработки ошибки при невалидном ответе API с использованием unittest.mock."""
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=500)
        hh = HeadHunterAPI()
        vacancies = hh.get_vacancies("Python Developer", area=1, per_page=1)

        assert vacancies == []
