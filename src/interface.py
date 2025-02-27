from src.api import HeadHunterAPI
from src.storage import JSONStorage


def main():
    storage = JSONStorage()
    hh = HeadHunterAPI()

    while True:
        print("\nМеню:")
        print("1. Найти вакансии")
        print("2. Показать сохранённые вакансии")
        print("3. Фильтровать вакансии по зарплате")
        print("4. Отсортировать вакансии по зарплате")
        print("5. Удалить вакансию")
        print("6. Очистить хранилище вакансий")
        print("7. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            keyword = input("Введите название вакансии: ")
            area = int(input("Введите ID региона (1 — Москва, 2 — Санкт-Петербург и т. д.): "))
            vacancies = hh.get_vacancies(keyword, area=area, per_page=5)
            storage.save_vacancies(vacancies)
            print("Вакансии сохранены!")

        elif choice == "2":
            loaded_vacancies = storage.load_vacancies()
            print("Загруженные вакансии:")
            for v in loaded_vacancies:
                print(v)

        elif choice == "3":
            min_salary = int(input("Введите минимальную зарплату: "))
            filtered_vacancies = storage.filter_vacancies_by_salary(min_salary)
            print("Фильтрованные вакансии:")
            for v in filtered_vacancies:
                print(v)

        elif choice == "4":
            sorted_vacancies = storage.sort_vacancies_by_salary()
            print("Отсортированные вакансии:")
            for v in sorted_vacancies:
                print(v)

        elif choice == "5":
            vacancy_name = input("Введите название вакансии для удаления: ")
            storage.delete_vacancy(vacancy_name)
            print("Вакансия удалена!")

        elif choice == "6":
            storage.clear_storage()
            print("Хранилище вакансий очищено!")

        elif choice == "7":
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Попробуйте снова.")
