import json
import os
import sys
import unittest
from unittest.mock import mock_open, patch

from src.load_products import load_categories_from_json
from src.main import Category

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        """Создание примера данных для тестов."""
        self.sample_data = [
            {
                "name": "Смартфоны",
                "description": "Смартфоны для удобства жизни",
                "products": [
                    {
                        "name": "Samsung Galaxy C23 Ultra",
                        "description": "256GB, Серый цвет, 200MP камера",
                        "price": 180000.0,
                        "quantity": 5,
                    },
                    {"name": "iPhone 15", "description": "512GB, Gray space", "price": 210000.0, "quantity": 8},
                ],
            }
        ]

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [
                {
                    "name": "Смартфоны",
                    "description": "Смартфоны для удобства жизни",
                    "products": [
                        {
                            "name": "Samsung Galaxy C23 Ultra",
                            "description": "256GB, Серый цвет, 200MP камера",
                            "price": 180000.0,
                            "quantity": 5,
                        },
                        {"name": "iPhone 15", "description": "512GB, Gray space", "price": 210000.0, "quantity": 8},
                    ],
                }
            ]
        ),
    )
    @patch("os.path.isfile", return_value=True)
    def test_load_categories_successfully(self, mock_isfile, mock_open):
        """Проверка успешной загрузки категорий из JSON."""
        categories = load_categories_from_json("products.json")
        self.assertEqual(len(categories), 1)
        category = categories[0]
        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, "Смартфоны")
        self.assertEqual(len(category.products), 2)

        product1 = category.products[0]
        product2 = category.products[1]

        self.assertEqual(product1.name, "Samsung Galaxy C23 Ultra")
        self.assertEqual(product2.name, "iPhone 15")

    @patch("os.path.isfile", return_value=False)
    def test_file_not_found(self, mock_isfile):
        """Проверка обработки ошибки при отсутствии файла."""
        with patch("builtins.input", return_value="nonexistent.json"):
            categories = load_categories_from_json("nonexistent.json", max_attempts=2)
            self.assertEqual(categories, [])

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    @patch("os.path.isfile", return_value=True)
    def test_invalid_json_format(self, mock_isfile, mock_open):
        """Проверка обработки ошибки при некорректном формате JSON."""
        categories = load_categories_from_json("products.json")
        self.assertEqual(categories, [])


if __name__ == "__main__":
    unittest.main()
