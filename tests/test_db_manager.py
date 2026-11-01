"""Тесты для модуля database.db_manager."""

import pytest
from database.db_manager import DBManager


@pytest.fixture(scope="module")
def db():
    """Фикстура: создает подключение к БД перед тестами и закрывает после."""
    manager = DBManager()
    yield manager
    manager.close()


def test_get_countries_and_aeroplanes_count(db):
    """Тест метода 1: проверяем, что возвращается список кортежей."""
    result = db.get_countries_and_aeroplanes_count()
    assert isinstance(result, list), "Результат должен быть списком"
    assert len(result) > 0, "Список стран не должен быть пустым"
    assert isinstance(result[0], tuple), "Элементы списка должны быть кортежами"
    assert len(result[0]) == 2, "Кортеж должен содержать 2 элемента (страна, количество)"


def test_get_all_aeroplanes(db):
    """Тест метода 2: проверяем, что возвращается список словарей."""
    result = db.get_all_aeroplanes()
    assert isinstance(result, list), "Результат должен быть списком"
    assert len(result) > 0, "Список самолетов не должен быть пустым"
    assert isinstance(result[0], dict), "Элементы списка должны быть словарями"
    assert "callsign" in result[0], "Словарь должен содержать ключ 'callsign'"
    assert "velocity" in result[0], "Словарь должен содержать ключ 'velocity'"


def test_get_avg_speed(db):
    """Тест метода 3: проверяем, что средняя скорость - это число."""
    result = db.get_avg_speed()
    assert isinstance(result, float), "Средняя скорость должна быть числом с плавающей точкой"
    assert result > 0, "Средняя скорость должна быть больше нуля"


def test_get_aeroplanes_with_higher_speed(db):
    """Тест метода 4: проверяем, что все самолеты быстрее средней."""
    avg_speed = db.get_avg_speed()
    fast_planes = db.get_aeroplanes_with_higher_speed()

    assert isinstance(fast_planes, list), "Результат должен быть списком"
    for plane in fast_planes:
        assert plane["velocity"] > avg_speed, f"Скорость {plane['velocity']} не выше средней {avg_speed}"


def test_get_aeroplanes_with_keyword(db):
    """Тест метода 5: проверяем поиск по ключевому слову."""
    keyword = "ACA"
    result = db.get_aeroplanes_with_keyword(keyword)

    assert isinstance(result, list), "Результат должен быть списком"
    for plane in result:
        assert keyword in plane["callsign"].upper(), f"Ключевое слово {keyword} не найдено в {plane['callsign']}"