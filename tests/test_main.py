import unittest
from src.main import Product, Category


class TestProduct(unittest.TestCase):
    def test_product_initialization(self):
        """Проверка корректности инициализации объекта класса Product."""
        product = Product("Test Product", "Description", 100.0, 10)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Description")
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.quantity, 10)


class TestCategory(unittest.TestCase):
    def setUp(self):
        """Сбрасываем глобальные счётчики и создаем продукты и категории для тестирования."""
        Category.category_count = 0
        Category.product_count = 0

        self.product1 = Product("Product1", "Description1", 100.0, 5)
        self.product2 = Product("Product2", "Description2", 200.0, 3)

        self.category1 = Category("TestCategory1", "Description1", [self.product1, self.product2])  # +2 продукта
        self.category2 = Category("TestCategory2", "Description2", [self.product1])  # +1 продукт

    def test_category_initialization(self):
        """Проверка корректности инициализации объекта класса Category."""
        self.assertEqual(self.category1.name, "TestCategory1")
        self.assertEqual(self.category1.description, "Description1")
        self.assertEqual(len(self.category1.products), 2)
        self.assertIn(self.product1, self.category1.products)
        self.assertIn(self.product2, self.category1.products)

    def test_product_count(self):
        """Проверка подсчета общего количества продуктов (количество объектов, а не quantity)."""
        self.assertEqual(Category.product_count, 3)  # 2 продукта в category1 + 1 продукт в category2

    def test_category_count(self):
        """Проверка подсчета количества категорий."""
        self.assertEqual(Category.category_count, 2)  # Создано 2 категории

    def test_multiple_categories(self):
        """Проверка добавления новых категорий и обновления счетчиков."""
        self.assertEqual(Category.product_count, 3)  # Проверяем, что сейчас 3 объекта Product

        product3 = Product("Product3", "Description3", 300.0, 7)
        category3 = Category("TestCategory3", "Description3", [product3])

        self.assertEqual(Category.category_count, 3)  # Теперь 3 категории
        self.assertEqual(Category.product_count, 4)  # Было 3 объекта Product, добавился 1 -> стало 4


if __name__ == '__main__':
    unittest.main()
