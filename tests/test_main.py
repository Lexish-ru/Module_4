import os
import sys
import unittest

from src.main import Category, Product

# Добавляем путь к src в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


class TestProduct(unittest.TestCase):
    def test_product_initialization(self):
        """Проверка корректности инициализации объекта Product."""
        product = Product("Безделушка", "Описание", 100.0, 10)
        self.assertEqual(product.name, "Безделушка")
        self.assertEqual(product.description, "Описание")
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.quantity, 10)

    def test_price_private_attribute(self):
        """Проверка, что price является приватным атрибутом."""
        product = Product("Безделушка", "Описание", 100.0, 10)
        with self.assertRaises(AttributeError):
            _ = product.__price

    def test_price_getter_setter(self):
        """Проверка работы геттера и сеттера для цены."""
        product = Product("Безделушка", "Описание", 100.0, 10)
        product.price = 200.0
        self.assertEqual(product.price, 200.0)

        product.price = -50.0  # Некорректное значение
        self.assertEqual(product.price, 200.0)  # Цена не должна измениться


class TestCategory(unittest.TestCase):
    def setUp(self):
        """Сбрасываем счётчики перед каждым тестом и создаём тестовые данные."""
        Category.category_count = 0
        Category.product_count = 0

        self.product1 = Product("Безделушка1", "Описание1", 100.0, 5)
        self.product2 = Product("Безделушка2", "Описание2", 200.0, 3)

    def test_category_initialization(self):
        """Проверка инициализации категории с продуктами."""
        category = Category("Категория", "Описание категории", [self.product1, self.product2])
        self.assertEqual(category.name, "Категория")
        self.assertEqual(category.description, "Описание категории")
        self.assertIn("Безделушка1, 100.0 руб. Остаток: 5 шт.", category.formatted_products())
        self.assertIn("Безделушка2, 200.0 руб. Остаток: 3 шт.", category.formatted_products())

    def test_products_private_attribute(self):
        """Проверка, что products является приватным атрибутом."""
        category = Category("Категория", "Описание категории", [self.product1])
        with self.assertRaises(AttributeError):
            _ = category.__products

    def test_add_product(self):
        """Проверка добавления нового продукта в категорию."""
        category = Category("Категория", "Описание категории", [self.product1])
        category.add_product(self.product2)
        self.assertIn("Безделушка2, 200.0 руб. Остаток: 3 шт.", category.formatted_products())
        self.assertEqual(Category.product_count, 2)

    def test_category_and_product_counts(self):
        """Проверка подсчёта категорий и продуктов."""
        Category("Категория1", "Описание1", [self.product1])
        Category("Категория2", "Описание2", [self.product2])
        self.assertEqual(Category.category_count, 2)
        self.assertEqual(Category.product_count, 2)

    def test_multiple_categories_with_same_products(self):
        """Проверка, что один и тот же продукт учитывается в разных категориях."""
        Category("Категория1", "Описание1", [self.product1, self.product2])
        Category("Категория2", "Описание2", [self.product1])
        self.assertEqual(Category.product_count, 3)  # 2 продукта в первой категории и 1 в другой

    def test_add_new_category(self):
        """Добавление новой категории и проверка обновления счётчиков."""
        Category("Категория1", "Описание1", [self.product1])
        self.assertEqual(Category.category_count, 1)
        self.assertEqual(Category.product_count, 1)

        product3 = Product("Product3", "Описание3", 300.0, 7)
        Category("Категория2", "Описание2", [product3])
        self.assertEqual(Category.category_count, 2)
        self.assertEqual(Category.product_count, 2)


if __name__ == "__main__":
    unittest.main()
