from typing import List

from src.load_products import load_categories_from_json


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Базовый класс для всех продуктов.
        """
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_info: dict):
        """
        Создание нового продукта из словаря.
        """
        if "efficiency" in product_info:
            return Smartphone(**product_info)
        elif "country" in product_info:
            return LawnGrass(**product_info)
        return cls(**product_info)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Цена должна быть больше нуля")
        self.__price = value


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return (
            f"{self.name} ({self.model}), {self.memory}GB, {self.color}, "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return (
            f"{self.name}, {self.country}, {self.color}, "
            f"срок прорастания: {self.germination_period}, "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.products = products
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его подклассов")
        self.products.append(product)
        Category.product_count += 1

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        return iter(self.products)

    def formatted_products(self):
        """
        Геттер для получения списка продуктов в формате строки.
        """
        return "\n".join(str(product) for product in self.products)


def main():
    """
    Главная функция программы. Загружает категории и товары из JSON-файла и выводит их на экран.
    """
    categories = load_categories_from_json("data/products.json")  # Просто загружаем категории

    for category in categories:
        print(f"Категория: {category.name}, Описание: {category.description}")
        print(category.formatted_products())  # Выводим товары


if __name__ == "__main__":
    main()
