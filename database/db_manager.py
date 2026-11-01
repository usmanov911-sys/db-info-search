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
            print("✅ Подключение к БД установлено")
        except psycopg2.Error as e:
            print(f"❌ Ошибка подключения к БД: {e}")
            raise

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("🔌 Подключение к БД закрыто")