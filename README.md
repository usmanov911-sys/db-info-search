# db-info-search

Курсовая работа: Поиск информации о самолетах с подключением к БД PostgreSQL.

## 📖 Описание
Проект получает данные о самолетах в воздушном пространстве выбранных стран через OpenSky API и сохраняет их в PostgreSQL. Реализован класс `DBManager` для анализа данных.

## ⚙️ Установка и запуск
1. Клонирование репозитория

```bash
git clone https://github.com/usmanov911-sys/db-info-search.git
cd db-info-search
````
2. Установка зависимостей

Проект использует Poetry для управления зависимостями:
```bash
poetry install
````
3. Настройка базы данных PostgreSQL

Создайте базу данных и примените схему:
```bash
12
createdb -U postgres db_info_searchpsql -U postgres -d db_info_search -f database/schema.sql
````
4. Настройка конфигурации

Откройте файл config.py и укажите параметры подключения к вашей БД:
```python
1234567
DB_CONFIG = {    "dbname": "db_info_search",    "user": "postgres",    "password": "ваш_пароль",   # ← замените на свой пароль    "host": "localhost",    "port": "5432"}
```
5. Запуск проекта

```bash
1
poetry run python main.py
````
6. Запуск тестов

```bash
1
poetry run pytest tests/ -v
````
## 🗂 Структура проекта 
```
db-info-search/
├── .gitignore                 # Исключённые файлы (venv, кэш, конфиг с паролями)
├── pyproject.toml             # Зависимости проекта (Poetry)
├── README.md                  # Документация проекта
├── config.py                  # Конфигурация (параметры БД, список стран, URL API)
├── main.py                    # Точка входа в приложение
├── database/
│   ├── __init__.py
│   ├── schema.sql             # SQL-скрипт создания таблиц
│   └── db_manager.py          # Класс DBManager с методами работы с БД
├── services/
│   ├── __init__.py
│   ├── api_client.py          # Клиент для работы с OpenSky API
│   └── data_loader.py         # Модуль загрузки данных из API в БД
└── tests/
    ├── __init__.py
    └── test_db_manager.py     # Тесты для методов DBManager (pytest)
```
## 🧩 Методы класса DBManager

Класс DBManager реализует следующие методы согласно заданию:
```
№     Метод                                  Описание

1     get_countries_and_aeroplanes_count()   Возвращает список стран и количество самолётов в их воздушном пространстве (использует JOIN)

2     get_all_aeroplanes()                   Возвращает список всех воздушных судов с полной информацией

3     get_avg_speed()                        Вычисляет среднюю скорость всех самолётов (использует AVG)

4     get_aeroplanes_with_higher_speed()     Возвращает список самолётов со скоростью выше средней (подзапрос)

5     get_aeroplanes_with_keyword(keyword)   Поиск самолётов по ключевому слову в позывном (например, 'ACA' — Air Canada)
```
## 🛠 Технологии

Python 3.14 — язык программирования
PostgreSQL 18 — реляционная база данных
psycopg2-binary — адаптер PostgreSQL для Python
requests — HTTP-клиент для работы с API
pytest — фреймворк для тестирования
Poetry — менеджер зависимостей
## 🌐 Используемые API

OpenSky Network — https://opensky-network.org/api/states/all
Документация: https://openskynetwork.github.io/opensky-api/rest.html
Nominatim (OpenStreetMap) — https://nominatim.openstreetmap.org/search
Документация: https://nominatim.org/release-docs/latest/api/Overview/

## 👨‍💻 Автор

Arthur Usmanov
Курсовая работа по модулю «Введение в DDL и проектирование БД»