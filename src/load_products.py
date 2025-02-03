import json
import os


def load_categories_from_json(file_name: str = "products.json", max_attempts: int = None):
    """
    Загружает данные из JSON-файла и создает объекты Category и Product.
    :param file_name: Имя JSON-файла.
    :param max_attempts: Максимальное количество попыток найти файл (для тестов).
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(project_root, "data", file_name)
    attempts = 0

    while not os.path.isfile(file_path):
        print(f"Ошибка: файл '{file_path}' не найден.")
        if max_attempts is not None and attempts >= max_attempts:
            return []  # Выход после максимального количества попыток
        file_name = input("Введите имя JSON-файла (по умолчанию 'products.json'): ") or "products.json"
        file_path = os.path.join(project_root, "data", file_name)
        attempts += 1

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        from src.main import Category, Product

        return [
            Category(cat["name"], cat["description"], [Product(**prod) for prod in cat["products"]]) for cat in data
        ]

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки JSON: {e}")
        return []
