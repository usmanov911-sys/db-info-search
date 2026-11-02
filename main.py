"""Точка входа в приложение db-info-search.

Демонстрирует работу всех методов класса DBManager.
"""

from services.data_loader import DataLoader
from database.db_manager import DBManager


def main():
    """Главная функция запуска проекта."""
    print("=" * 60)
    print("🛫 ПРОЕКТ: ПОИСК ИНФОРМАЦИИ О САМОЛЕТАХ")
    print("=" * 60)

    # 1. Загружаем данные из API в БД
    print("\n📡 Загрузка данных из OpenSky API...")
    loader = DataLoader()
    loader.load_data()

    # 2. Создаем экземпляр DBManager для демонстрации методов
    db = DBManager()

    # Метод 1: Список стран и количество самолетов
    print("\n" + "=" * 60)
    print("📊 МЕТОД 1: get_countries_and_aeroplanes_count()")
    print("=" * 60)
    countries_count = db.get_countries_and_aeroplanes_count()
    for country_name, count in countries_count:
        print(f"  {country_name}: {count} самолетов")

    # Метод 2: Список всех воздушных судов (покажем первые 10)
    print("\n" + "=" * 60)
    print("✈️  МЕТОД 2: get_all_aeroplanes()")
    print("=" * 60)
    all_planes = db.get_all_aeroplanes()
    print(f"  Всего самолетов в БД: {len(all_planes)}")
    print("  Первые 10 самолетов:")
    for plane in all_planes[:10]:
        print(f"    - {plane['callsign'] or 'N/A'} ({plane['country'] or 'Unknown'}): "
              f"скорость {plane['velocity'] or 0} м/с")

    # Метод 3: Средняя скорость
    print("\n" + "=" * 60)
    print("📈 МЕТОД 3: get_avg_speed()")
    print("=" * 60)
    avg_speed = db.get_avg_speed()
    print(f"  Средняя скорость всех самолетов: {avg_speed} м/с")

    # Метод 4: Самолеты со скоростью выше средней
    print("\n" + "=" * 60)
    print("🚀 МЕТОД 4: get_aeroplanes_with_higher_speed()")
    print("=" * 60)
    fast_planes = db.get_aeroplanes_with_higher_speed()
    print(f"  Самолетов со скоростью выше средней ({avg_speed} м/с): {len(fast_planes)}")
    print("  Топ-5 самых быстрых:")
    for plane in fast_planes[:5]:
        print(f"    - {plane['callsign'] or 'N/A'}: {plane['velocity']} м/с")

    # Метод 5: Поиск по ключевому слову
    print("\n" + "=" * 60)
    print("🔍 МЕТОД 5: get_aeroplanes_with_keyword()")
    print("=" * 60)
    keyword = "ACA"  # Air Canada
    keyword_planes = db.get_aeroplanes_with_keyword(keyword)
    print(f"  Найдено самолетов с позывным, содержащим '{keyword}': {len(keyword_planes)}")
    print("  Первые 10 результатов:")
    for plane in keyword_planes[:10]:
        print(f"    - {plane['callsign']} ({plane['origin_country']}): "
              f"{plane['velocity'] or 0} м/с")

    print("\n" + "=" * 60)
    print("✅ ВСЕ МЕТОДЫ DBMANAGER УСПЕШНО ПРОДЕМОНСТРИРОВАНЫ")
    print("=" * 60)


if __name__ == "__main__":
    main()