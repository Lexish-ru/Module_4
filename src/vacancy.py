from typing import Any, Dict


class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = (
        "_name",
        "_url",
        "_salary_from",
        "_salary_to",
        "_currency",
        "_employer",
        "_requirement",
        "_responsibility",
    )

    def __init__(
        self,
        name: str,
        url: str,
        salary_from: int,
        salary_to: int,
        currency: str,
        employer: str,
        requirement: str,
        responsibility: str,
    ):
        self._name = name
        self._url = url
        self._salary_from = salary_from or 0
        self._salary_to = salary_to or 0
        self._currency = currency or "Не указано"
        self._employer = employer
        self._requirement = requirement
        self._responsibility = responsibility

    def __str__(self) -> str:
        salary_info = (
            f"{self._salary_from} - {self._salary_to} {self._currency}"
            if self._salary_from or self._salary_to
            else "Зарплата не указана"
        )
        return (
            f"Вакансия: {self._name}\n"
            f"Компания: {self._employer}\n"
            f"Зарплата: {salary_info}\n"
            f"Требования: {self._requirement}\n"
            f"Обязанности: {self._responsibility}\n"
            f"Ссылка: {self._url}\n"
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def salary_from(self) -> int:
        return self._salary_from

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект вакансии в словарь для JSON."""
        return {
            "name": self._name,
            "url": self._url,
            "salary_from": self._salary_from,
            "salary_to": self._salary_to,
            "currency": self._currency,
            "employer": self._employer,
            "requirement": self._requirement,
            "responsibility": self._responsibility,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        """Создает объект вакансии из словаря JSON."""
        return cls(
            name=data["name"],
            url=data["url"],
            salary_from=data.get("salary_from", 0),
            salary_to=data.get("salary_to", 0),
            currency=data.get("currency", "Не указано"),
            employer=data["employer"],
            requirement=data["requirement"],
            responsibility=data["responsibility"],
        )

    def __lt__(self, other: "Vacancy") -> bool:
        return self._salary_from < other._salary_from

    def __gt__(self, other: "Vacancy") -> bool:
        return self._salary_from > other._salary_from
