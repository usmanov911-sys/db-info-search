"""Модуль для загрузки данных из API в БД."""

from services.api_client import APIClient
from database.db_manager import DBManager


class DataLoader:
    """Загрузчик данных: получает данные из API и сохраняет их в БД."""

    def __init__(self):
        """Инициализация клиентов API и БД."""
        self.api_client = APIClient()
        self.db_manager = DBManager()

    def load_data(self):
        """Полный цикл: получение данных и сохранение в БД."""
        print("📡 Этап 1: Получаем данные из OpenSky API...")
        data = self.api_client.fetch_all_data()

        print("\n💾 Этап 2: Сохраняем данные в PostgreSQL...")
        self.db_manager.save_data(data)

        print("🎉 Загрузка данных завершена успешно!")