import os
from pathlib import Path
from src.storage import JSONStorage
from src.vacancy import Vacancy


def test_storage_operations(tmp_path: Path) -> None:
    """Тест сохранения, загрузки, фильтрации и удаления вакансий, включая граничные случаи."""
    test_file = tmp_path / "test_vacancies.json"
    storage = JSONStorage(filename=str(test_file))

    vacancies = [
        Vacancy(
            "Python Developer",
            "https://example.com",
            100000,
            150000,
            "RUR",
            "CompanyX",
            "Python, Django",
            "Backend development",
        ),
        Vacancy("Junior Developer", "https://example.com", 50000, 70000, "RUR", "CompanyY", "Flask", "Backend"),
        Vacancy("Intern Developer", "https://example.com", None, None, None, "CompanyZ", "Basics", "Learning"),
    ]

    # Тест сохранения
    storage.save_vacancies(vacancies)
    assert os.path.exists(test_file)

    # Тест загрузки
    loaded_vacancies = storage.load_vacancies()
    assert len(loaded_vacancies) == 3
    assert loaded_vacancies[0].name == "Python Developer"

    # Тест фильтрации
    filtered_vacancies = storage.filter_vacancies_by_salary(80000)
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0].name == "Python Developer"

    # Тест удаления
    storage.delete_vacancy("Python Developer")
    remaining_vacancies = storage.load_vacancies()
    assert len(remaining_vacancies) == 2
    assert remaining_vacancies[0].name == "Junior Developer"

    # Тест очистки хранилища
    storage.clear_storage()
    cleared_vacancies = storage.load_vacancies()
    assert cleared_vacancies == []

    # Граничные случаи
    # Сохранение пустого списка
    storage.save_vacancies([])
    assert storage.load_vacancies() == []

    # Фильтрация по зарплате, когда у вакансии нет зарплаты
    storage.save_vacancies(
        [Vacancy("Intern", "https://example.com", None, None, None, "CompanyZ", "Basics", "Learning")]
    )
    assert storage.filter_vacancies_by_salary(0) == []

    # Удаление несуществующей вакансии
    storage.delete_vacancy("Non-existent Job")  # Должно работать без ошибок
