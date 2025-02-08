from src.load_products import load_categories_from_json


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Класс Product представляет товар с его характеристиками.
        """
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_info: dict):
        """
        Класс-метод для создания нового продукта из словаря.
        """
        return cls(**product_info)

    @property
    def price(self):
        """
        Геттер для получения цены товара.
        """
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """
        Сеттер для установки новой цены товара с проверкой валидности.
        """
        if new_price > 0:
            self.__price = new_price
        else:
            raise ValueError("Цена должна быть больше нуля.")


class Category:
    # Атрибуты класса
    category_count = 0  # Общее количество категорий
    product_count = 0  # Общее количество товаров во всех категориях

    def __init__(self, name: str, description: str, products: list):
        """
        Класс Category представляет категорию товаров.
        """
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут списка товаров

        # Автоматическое обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity}"

    def __iter__(self):
        """
        Итератор для перебора продуктов в категории.
        """
        return iter(self.__products)


    def add_product(self, product):
        """
        Метод для добавления продукта в категорию с проверкой типа.
        """
        if not isinstance(product, Product):
            print("Ошибка: добавляемый объект должен быть экземпляром класса Product или его наследником.")
            return
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """
        Геттер для получения списка продуктов в виде объектов
        :return:
        """
        return self.__products

    def formatted_products(self):
        """
        Геттер для получения списка продуктов в формате строки.
        """
        return "".join(
            [f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n" for product in self.__products]
        )


def main():
    """
    Главная функция программы. Загружает категории и товары из JSON-файла и выводит их на экран.
    """
    categories = load_categories_from_json("products.json")

    # Вывод информации о категориях и продуктах
    for category in categories:
        print(f"Категория: {category.name}, Описание: {category.description}")
        print(category.formatted_products())  # Используем геттер для вывода товаров


if __name__ == "__main__":
    main()
