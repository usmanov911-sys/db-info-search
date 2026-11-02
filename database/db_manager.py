"""Модуль для работы с базой данных PostgreSQL."""

import psycopg2
from config import DB_CONFIG


class DBManager:
    """Менеджер для подключения и работы с БД PostgreSQL."""

    def __init__(self):
        """Инициализация менеджера БД."""
        self.connection = None
        self.cursor = None

    def connect(self):
        """Устанавливает соединение с базой данных."""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print(f"❌ Ошибка подключения к БД: {e}")
            raise

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def save_data(self, countries_data: dict):
        """Сохраняет данные о странах и самолетах в БД.

        Args:
            countries_data: Словарь {country_name: {"coords": {...}, "airplanes": [...]}}.
        """
        self.connect()
        try:
            for country_name, data in countries_data.items():
                coords = data["coords"]

                # 1. Сохраняем или пропускаем страну (ON CONFLICT DO NOTHING)
                self.cursor.execute(
                    """INSERT INTO countries (name, min_lat, max_lat, min_lon, max_lon)
                       VALUES (%s, %s, %s, %s, %s)
                       ON CONFLICT (name) DO NOTHING
                       RETURNING id""",
                    (country_name, coords["min_lat"], coords["max_lat"],
                     coords["min_lon"], coords["max_lon"])
                )
                row = self.cursor.fetchone()
                country_id = row[0] if row else self._get_country_id(country_name)

                # 2. Сохраняем или обновляем самолеты
                for plane in data["airplanes"]:
                    self.cursor.execute(
                        """INSERT INTO airplanes 
                           (icao24, callsign, origin_country, longitude, latitude, 
                            velocity, country_id, last_contact)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                           ON CONFLICT (icao24, country_id) DO UPDATE SET
                           callsign = EXCLUDED.callsign,
                           longitude = EXCLUDED.longitude,
                           latitude = EXCLUDED.latitude,
                           velocity = EXCLUDED.velocity,
                           last_contact = EXCLUDED.last_contact""",
                        (plane["icao24"], plane["callsign"], plane["origin_country"],
                         plane["longitude"], plane["latitude"], plane["velocity"],
                         country_id, plane["last_contact"])
                    )
            self.connection.commit()
            print("✅ Данные успешно сохранены в БД")
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Ошибка сохранения данных: {e}")
            raise
        finally:
            self.close()

    def _get_country_id(self, name: str) -> int:
        """Вспомогательный метод: возвращает ID страны по названию."""
        self.cursor.execute("SELECT id FROM countries WHERE name = %s", (name,))
        return self.cursor.fetchone()[0]

    def get_countries_and_aeroplanes_count(self) -> list:
        """Получает список стран и количество самолетов в их воздушном пространстве.

        Returns:
            Список кортежей (country_name, airplane_count).
        """
        self.connect()
        try:
            self.cursor.execute(
                """SELECT c.name, COUNT(a.id)
                   FROM countries c
                   LEFT JOIN airplanes a ON c.id = a.country_id
                   GROUP BY c.name
                   ORDER BY COUNT(a.id) DESC"""
            )
            return self.cursor.fetchall()
        finally:
            self.close()

    def get_all_aeroplanes(self) -> list:
        """Получает список всех воздушных судов.

        Returns:
            Список словарей с данными о самолетах.
        """
        self.connect()
        try:
            self.cursor.execute(
                """SELECT a.icao24, a.callsign, a.origin_country, 
                          a.longitude, a.latitude, a.velocity, c.name AS country
                   FROM airplanes a
                   LEFT JOIN countries c ON a.country_id = c.id"""
            )
            columns = ["icao24", "callsign", "origin_country",
                       "longitude", "latitude", "velocity", "country"]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        finally:
            self.close()

    def get_avg_speed(self) -> float:
        """Получает среднюю скорость по всем самолетам.

        Returns:
            Среднее значение скорости (float).
        """
        self.connect()
        try:
            self.cursor.execute(
                "SELECT AVG(velocity) FROM airplanes WHERE velocity IS NOT NULL"
            )
            result = self.cursor.fetchone()[0]
            return round(result, 2) if result else 0.0
        finally:
            self.close()

    def get_aeroplanes_with_higher_speed(self) -> list:
        """Получает список самолетов со скоростью выше средней.

        Returns:
            Список словарей с данными о самолетах.
        """
        self.connect()
        try:
            self.cursor.execute(
                """SELECT a.icao24, a.callsign, a.velocity
                   FROM airplanes a
                   WHERE a.velocity > (
                       SELECT AVG(velocity) FROM airplanes 
                       WHERE velocity IS NOT NULL
                   )
                   ORDER BY a.velocity DESC"""
            )
            columns = ["icao24", "callsign", "velocity"]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        finally:
            self.close()

    def get_aeroplanes_with_keyword(self, keyword: str) -> list:
        """Получает список самолетов, в позывном которых содержится keyword.

        Args:
            keyword: Искомая подстрока (например, 'ACA' для Air Canada).

        Returns:
            Список словарей с данными о самолетах.
        """
        self.connect()
        try:
            self.cursor.execute(
                """SELECT a.icao24, a.callsign, a.origin_country, a.velocity
                   FROM airplanes a
                   WHERE a.callsign ILIKE %s
                   ORDER BY a.callsign""",
                (f"%{keyword}%",)
            )
            columns = ["icao24", "callsign", "origin_country", "velocity"]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        finally:
            self.close()