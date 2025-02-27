from src.vacancy import Vacancy


def test_vacancy_creation() -> None:
    vacancy = Vacancy(
        "Python Developer",
        "https://example.com",
        100000,
        150000,
        "RUR",
        "CompanyX",
        "Python, Django",
        "Backend development",
    )
    assert vacancy._name == "Python Developer"
    assert vacancy._url == "https://example.com"
    assert vacancy._salary_from == 100000
    assert vacancy._salary_to == 150000
    assert vacancy._currency == "RUR"
    assert vacancy._employer == "CompanyX"
    assert vacancy._requirement == "Python, Django"
    assert vacancy._responsibility == "Backend development"


def test_vacancy_salary_none() -> None:
    vacancy = Vacancy(
        "QA Engineer", "https://example.com", None, None, None, "CompanyY", "Testing, Selenium", "Automation testing"
    )
    assert vacancy._salary_from == 0
    assert vacancy._salary_to == 0
    assert vacancy._currency == "Не указано"


def test_vacancy_comparison() -> None:
    v1 = Vacancy("Dev1", "https://example.com", 90000, 120000, "RUR", "CompanyA", "Python", "Backend")
    v2 = Vacancy("Dev2", "https://example.com", 110000, 130000, "RUR", "CompanyB", "Django", "Backend")
    assert v1 < v2
    assert v2 > v1
