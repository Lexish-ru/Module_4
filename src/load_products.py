import json
import os


def load_categories_from_json(file_name: str = "products.json"):
    """
    Загружает данные из JSON-файла и создает объекты Category и Product.
    """
    # Получаем путь к корню проекта, поднимаясь только на один уровень вверх
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Один уровень вверх
    file_path = os.path.join(project_root, 'data', file_name)  # Путь к файлу в папке data

    # Проверка на существование директории и файла
    while not os.path.isfile(file_path):
        print(f"Ошибка: файл '{file_path}' не найден.")
        file_name = input("Введите имя JSON-файла (по умолчанию 'products.json'): ") or "products.json"
        file_path = os.path.join(project_root, 'data', file_name)  # Обновляем путь

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Здесь импорты классов внутри try, чтобы избежать циклического импорта
        from main import Product, Category

        categories = []
        for category_data in data:
            products = [
                Product(p["name"], p["description"], p["price"], p["quantity"])
                for p in category_data["products"]
            ]
            category = Category(category_data["name"], category_data["description"], products)
            categories.append(category)

        return categories

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки JSON: {e}")
        return []
