import os
import sys
import unittest

from src.main import Category, Product

# Добавляем путь к src в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


class TestProduct(unittest.TestCase):
    def test_product_initialization(self):
        """Проверка корректности инициализации объекта Product."""
        product = Product("Test Product", "Description", 100.0, 10)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Description")
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.quantity, 10)


class TestCategory(unittest.TestCase):
    def setUp(self):
        """Сбрасываем счётчики перед каждым тестом и создаём тестовые данные."""
        Category.category_count = 0
        Category.product_count = 0

        self.product1 = Product("Product1", "Description1", 100.0, 5)
        self.product2 = Product("Product2", "Description2", 200.0, 3)

    def test_category_initialization(self):
        """Проверка инициализации категории с продуктами."""
        category = Category("TestCategory", "Category Description", [self.product1, self.product2])
        self.assertEqual(category.name, "TestCategory")
        self.assertEqual(category.description, "Category Description")
        self.assertEqual(len(category.products), 2)
        self.assertIn(self.product1, category.products)
        self.assertIn(self.product2, category.products)

    def test_category_and_product_counts(self):
        """Проверка подсчёта категорий и продуктов."""
        Category("Category1", "Description1", [self.product1])
        Category("Category2", "Description2", [self.product2])
        self.assertEqual(Category.category_count, 2)
        self.assertEqual(Category.product_count, 2)

    def test_multiple_categories_with_same_products(self):
        """Проверка, что один и тот же продукт учитывается в разных категориях."""
        Category("Category1", "Description1", [self.product1, self.product2])
        Category("Category2", "Description2", [self.product1])
        self.assertEqual(Category.product_count, 3)  # 2 продукта в первой категории и 1 в другой

    def test_add_new_category(self):
        """Добавление новой категории и проверка обновления счётчиков."""
        Category("Category1", "Description1", [self.product1])
        self.assertEqual(Category.category_count, 1)
        self.assertEqual(Category.product_count, 1)

        product3 = Product("Product3", "Description3", 300.0, 7)
        Category("Category2", "Description2", [product3])
        self.assertEqual(Category.category_count, 2)
        self.assertEqual(Category.product_count, 2)


if __name__ == "__main__":
    unittest.main()
