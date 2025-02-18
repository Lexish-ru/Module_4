import json
import unittest
from unittest.mock import mock_open, patch

from src.load_products import load_categories_from_json
from src.main import LawnGrass, Smartphone


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        """Создание примера данных для тестов."""
        self.sample_data = [
            {
                "name": "Смартфоны",
                "description": "Смартфоны для удобства жизни",
                "products": [
                    {
                        "name": "Samsung Galaxy S23 Ultra",
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
                    "description": "Категория телефонов",
                    "products": [
                        {
                            "name": "iPhone 15",
                            "description": "512GB, Gray",
                            "price": 210000.0,
                            "quantity": 8,
                            "efficiency": "A16",
                            "model": "Pro Max",
                            "memory": 512,
                            "color": "Space Gray",
                        }
                    ],
                },
                {
                    "name": "Газонная трава",
                    "description": "Категория трав",
                    "products": [
                        {
                            "name": "GreenField",
                            "description": "Газонная трава",
                            "price": 1500.0,
                            "quantity": 20,
                            "country": "Нидерланды",
                            "germination_period": "2 недели",
                            "color": "Зелёный",
                        }
                    ],
                },
            ]
        ),
    )
    @patch("os.path.isfile", return_value=True)
    def test_load_smartphone_and_lawngrass(self, mock_isfile, mock_open):
        """Проверка загрузки смартфона и газонной травы из JSON."""
        categories = load_categories_from_json("products.json")

        self.assertEqual(len(categories), 2)

        phone_category = categories[0]
        self.assertEqual(phone_category.name, "Смартфоны")
        self.assertIsInstance(phone_category.products[0], Smartphone)
        self.assertEqual(phone_category.products[0].name, "iPhone 15")

        grass_category = categories[1]
        self.assertEqual(grass_category.name, "Газонная трава")
        self.assertIsInstance(grass_category.products[0], LawnGrass)
        self.assertEqual(grass_category.products[0].name, "GreenField")

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
