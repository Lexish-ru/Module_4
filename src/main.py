from abc import ABC, abstractmethod
from typing import List

from src.load_products import load_categories_from_json


class BaseProduct(ABC):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        pass

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Цена должна быть больше нуля")
        self.__price = value


class ProductLoggerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"Создан объект: {self.__class__.__name__} с параметрами {self.__dict__}")


class Product(ProductLoggerMixin, BaseProduct):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен.")
        super().__init__(name, description, price, quantity)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_info: dict):
        if "efficiency" in product_info:
            return Smartphone(**product_info)
        elif "country" in product_info:
            return LawnGrass(**product_info)
        return cls(**product_info)


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


class AbstractEntity(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self):
        pass


class Category(AbstractEntity):
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        super().__init__(name, description)
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
        return "\\n".join(str(product) for product in self.products)


class Order(AbstractEntity):
    def __init__(self, product: Product, quantity: int):
        super().__init__(product.name, f"Заказ на {quantity} шт.")
        if quantity < 0:
            raise ValueError("Количество товаров в заказе не может быть отрицательным.")
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    def __str__(self):
        return f"Заказ: {self.product.name}, Количество: {self.quantity}, Итоговая стоимость: {self.total_price} руб."


def main():
    categories = load_categories_from_json("data/products.json")
    for category in categories:
        print(f"Категория: {category.name}, Описание: {category.description}")
        print(category.formatted_products())


if __name__ == "__main__":
    main()
