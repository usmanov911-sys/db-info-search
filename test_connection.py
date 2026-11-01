"""Тест подключения к БД."""

from database.db_manager import DBManager


def test_connection():
    """Проверяет подключение к базе данных."""
    db = DBManager()
    db.connect()

    # Проверяем, что таблицы существуют
    db.cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = db.cursor.fetchall()
    print(f"📋 Таблицы в БД: {[t[0] for t in tables]}")

    db.close()


if __name__ == "__main__":
    test_connection()