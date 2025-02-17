import io
import os
import sys
import unittest

import pytest

from src.main import BaseProduct, Category, LawnGrass, Order, Product, Smartphone, OrderException

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

        with self.assertRaises(ValueError):  # Ожидаем ошибку при установке отрицательной цены
            product.price = -50.0

        with self.assertRaises(ValueError):  # Ожидаем ошибку при установке нулевой цены
            product.price = 0.0

    def test_extreme_price_values(self):
        """Проверка крайних значений для цены."""
        product = Product("Безделушка", "Описание", 1.0, 10)

        # Проверка очень большого значения цены
        extreme_price = 1e10
        product.price = extreme_price
        self.assertEqual(product.price, extreme_price)

        # Проверка очень маленького положительного значения цены
        small_positive_price = 1e-10
        product.price = small_positive_price
        self.assertEqual(product.price, small_positive_price)

        # Проверка граничного значения (очень близкого к нулю, но не равного)
        borderline_price = 1e-15
        product.price = borderline_price
        self.assertEqual(product.price, borderline_price)

    def test_product_str(self):
        """Проверка строкового представления продукта."""
        product = Product("Тестовый товар", "Описание", 100.0, 10)
        self.assertEqual(str(product), "Тестовый товар, 100.0 руб. Остаток: 10 шт.")

    def test_product_addition(self):
        """Проверка магического метода сложения продуктов."""
        product1 = Product("Товар 1", "Описание", 100.0, 2)
        product2 = Product("Товар 2", "Описание", 200.0, 3)
        self.assertEqual(product1 + product2, (100.0 * 2 + 200.0 * 3))

    def test_product_logger_mixin(self):
        """Проверяем, что при создании объекта выводится информация в консоль."""
        captured_output = io.StringIO()  # Перехватываем вывод в консоль
        sys.stdout = captured_output

        phone = Smartphone("iPhone 15", "512GB", 210000.0, 8, "A16", "Pro", 512, "Gray")
        _ = phone
        sys.stdout = sys.__stdout__  # Восстанавливаем стандартный вывод
        assert "Создан объект: Smartphone" in captured_output.getvalue()
        assert "'name': 'iPhone 15'" in captured_output.getvalue()

    def test_product_quantity_zero(self):
        """Проверка, что при создании товара с нулевым количеством выбрасывается ValueError"""
        with self.assertRaises(ValueError, msg="Товар с нулевым количеством не может быть добавлен."):
            Product("Бракованный товар", "Неверное количество", 1000.0, 0)

    def test_product_negative_quantity(self):
        """Проверка, что при создании товара с отрицательным количеством выбрасывается ValueError"""
        with self.assertRaises(ValueError, msg="Товар с нулевым количеством не может быть добавлен."):
            Product("Бракованный товар", "Неверное количество", 1000.0, -5)


class TestBaseProduct(unittest.TestCase):
    """Тесты для абстрактного класса BaseProduct."""

    def test_base_product_is_abstract(self):
        """Проверяем, что нельзя создать экземпляр BaseProduct."""
        with pytest.raises(TypeError):
            BaseProduct("Тест", "Описание", 100.0, 10)

    def test_product_inherits_base_product(self):
        """Проверяем, что Product наследуется от BaseProduct."""
        phone = Smartphone("iPhone 15", "512GB", 210000.0, 8, "A16", "Pro", 512, "Gray")
        assert isinstance(phone, BaseProduct)


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

    def test_add_invalid_product(self):
        category = Category("Электроника", "Тестовая категория", [])
        with pytest.raises(TypeError, match="Можно добавлять только объекты Product или его подклассов"):
            category.add_product("Некорректный объект")

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

        product3 = Product("Продукт3", "Описание3", 300.0, 7)
        Category("Категория2", "Описание2", [product3])
        self.assertEqual(Category.category_count, 2)
        self.assertEqual(Category.product_count, 2)

    def test_add_duplicate_product(self):
        """Проверка добавления одного и того же продукта несколько раз."""
        category = Category("Категория", "Описание категории", [self.product1])
        category.add_product(self.product1)  # Добавляем тот же продукт снова
        self.assertEqual(len(category.products), 2)  # Ожидаем два одинаковых продукта в списке
        self.assertEqual(Category.product_count, 2)

    def test_category_str(self):
        """Проверка строкового представления категории."""
        products = [Product("Товар 1", "Описание", 100.0, 2), Product("Товар 2", "Описание", 200.0, 3)]
        category = Category("Категория", "Описание", products)
        self.assertEqual(str(category), "Категория, количество продуктов: 5 шт.")

    def test_category_iteration(self):
        """Проверка работы итератора в категории."""
        products = [Product("Товар 1", "Описание", 100.0, 2), Product("Товар 2", "Описание", 200.0, 3)]
        category = Category("Категория", "Описание", products)
        iterated_products = [product for product in category]
        self.assertEqual(iterated_products, products)

    def test_category_iterator_exhaustion(self):
        """Проверка, что итератор категории можно исчерпать."""
        products = [Product("Товар 1", "Описание", 100.0, 2), Product("Товар 2", "Описание", 200.0, 3)]
        category = Category("Категория", "Описание", products)
        iterator = iter(category)
        self.assertEqual(next(iterator), products[0])
        self.assertEqual(next(iterator), products[1])
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_category_iterable(self):
        """Проверка возможности перебора товаров через итератор."""

        products = [
            Product("Товар A", "Описание", 500.0, 1),
            Product("Товар B", "Описание", 300.0, 2),
            Product("Товар C", "Описание", 150.0, 5),
        ]
        category = Category("Тестовая категория", "Описание", products)
        for i, product in enumerate(category):
            self.assertEqual(product, products[i])

    def test_category_middle_price(self):
        """Проверка расчёта средней цены товаров в категории"""
        product1 = Product("Товар 1", "Описание", 100, 2)  # 100 * 2
        product2 = Product("Товар 2", "Описание", 200, 3)  # 200 * 3
        category = Category("Тестовая категория", "Описание", [product1, product2])

        expected_price = round((100 * 2 + 200 * 3) / (2 + 3), 2)  # (200 + 600) / 5 = 160.0
        self.assertEqual(category.middle_price(), expected_price)

    def test_category_middle_price_empty(self):
        """Проверка, что для пустой категории средняя цена равна 0"""
        category = Category("Пустая категория", "Описание", [])
        self.assertEqual(category.middle_price(), 0)


class TestProductMethods(unittest.TestCase):
    def test_smartphone_str(self):
        """Проверка строкового представления смартфона."""
        phone = Smartphone("iPhone 15", "512GB", 200000, 5, "A16", "Pro", 512, "Gray")
        expected_str = "iPhone 15 (Pro), 512GB, Gray, 200000 руб. Остаток: 5 шт."
        self.assertEqual(str(phone), expected_str)

    def test_lawngrass_str(self):
        """Проверка строкового представления газонной травы."""
        grass = LawnGrass("GreenField", "Газонная трава", 1500.0, 20, "Нидерланды", "2 недели", "Зелёный")
        expected_str = "GreenField, Нидерланды, Зелёный, срок прорастания: 2 недели, 1500.0 руб. Остаток: 20 шт."
        self.assertEqual(str(grass), expected_str)

    def test_product_addition_same_type(self):
        """Проверка сложения товаров одного типа."""
        phone1 = Smartphone("iPhone 15", "512GB", 200000, 5, "A16", "Pro", 512, "Gray")
        phone2 = Smartphone("iPhone 15", "512GB", 200000, 3, "A16", "Pro", 512, "Gray")
        self.assertEqual(phone1 + phone2, (200000 * 5 + 200000 * 3))

    def test_product_addition_different_types(self):
        """Проверка ошибки при сложении товаров разных типов."""
        phone = Smartphone("iPhone 15", "512GB", 200000, 5, "A16", "Pro", 512, "Gray")
        grass = LawnGrass("GreenField", "Газонная трава", 1500.0, 20, "Нидерланды", "2 недели", "Зелёный")
        with self.assertRaises(TypeError):
            _ = phone + grass


class TestOrder(unittest.TestCase):
    def test_order_creation(self):
        """Проверка создания заказа и расчета итоговой стоимости."""
        phone = Smartphone("iPhone 15", "512GB", 210000.0, 8, "A16", "Pro", 512, "Gray")
        order = Order(phone, 2)
        self.assertEqual(order.product, phone)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total_price, 420000.0)
        self.assertEqual(str(order), "Заказ: iPhone 15, Количество: 2, Итоговая стоимость: 420000.0 руб.")

    def test_order_with_zero_quantity(self):
        """Проверка, что при заказе с нулевым количеством выбрасывается исключение."""
        phone = Smartphone("iPhone 15", "512GB", 210000.0, 8, "A16", "Pro", 512, "Gray")

        with self.assertRaises(OrderException):  # Ожидаем OrderException
            Order(phone, 0)

    def test_order_with_negative_quantity(self):
        """Проверка ошибки при создании заказа с отрицательным количеством."""
        phone = Smartphone("iPhone 15", "512GB", 210000.0, 8, "A16", "Pro", 512, "Gray")
        with self.assertRaises(OrderException):  # Исправляем тест, ожидаем OrderException
            Order(phone, -1)


if __name__ == "__main__":
    unittest.main()
