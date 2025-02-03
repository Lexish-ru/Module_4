from load_products import load_categories_from_json


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Класс Product представляет товар с его характеристиками.
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    # Атрибуты класса
    category_count = 0  # Общее количество категорий
    product_count = 0  # Общее количество товаров во всех категориях

    def __init__(self, name: str, description: str, products: list):
        """
        Класс Category представляет категорию товаров.
        """
        # Атрибуты объекта
        self.name = name
        self.description = description
        self.products = products

        # Автоматическое обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)  # Учитывает только количество объектов, без их quantity


def main():
    """
    Главная функция программы. Загружает категории и товары из JSON-файла и выводит их на экран.
    """
    categories = load_categories_from_json("products.json")

    # Вывод информации о категориях и продуктах
    for category in categories:
        print(f"Категория: {category.name}, Описание: {category.description}")
        for product in category.products:
            print(f"  - {product.name}: {product.description} ({product.price} руб, {product.quantity} шт)")


if __name__ == "__main__":
    main()
