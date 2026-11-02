"""Модуль для работы с внешними API (OpenSky)."""

import time
import requests
from config import COUNTRIES_DATA, OPENSKY_URL


class APIClient:
    """Клиент для получения данных о самолетах из OpenSky API."""

    def __init__(self):
        """Инициализация HTTP-сессии."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "SkyproCourseworkDBSearch/1.0",
            "Accept": "application/json"
        })

    def get_airplanes_in_bounds(
        self, min_lat: float, max_lat: float,
        min_lon: float, max_lon: float
    ) -> list:
        """Получает список самолетов в заданной области через OpenSky API."""
        params = {
            "lamin": min_lat,
            "lamax": max_lat,
            "lomin": min_lon,
            "lomax": max_lon
        }
        response = self.session.get(OPENSKY_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if not data or not data.get("states"):
            return []

        airplanes = []
        for state in data["states"]:
            airplanes.append({
                "icao24": state[0],
                "callsign": state[1].strip() if state[1] else None,
                "origin_country": state[2],
                "longitude": state[5],
                "latitude": state[6],
                "velocity": state[9],
                "last_contact": state[4]
            })
        return airplanes

    def fetch_all_data(self) -> dict:
        """Собирает данные по всем странам из COUNTRIES_DATA."""
        result = {}
        print(f"📡 Начинаем опрос OpenSky API для {len(COUNTRIES_DATA)} стран...")

        for country_name, coords in COUNTRIES_DATA.items():
            try:
                # Небольшая задержка, чтобы не перегружать OpenSky API
                time.sleep(0.5)

                airplanes = self.get_airplanes_in_bounds(
                    coords["min_lat"], coords["max_lat"],
                    coords["min_lon"], coords["max_lon"]
                )

                result[country_name] = {
                    "coords": coords,
                    "airplanes": airplanes
                }
                print(f"✅ {country_name}: найдено {len(airplanes)} самолетов")

            except Exception as e:
                print(f"❌ Ошибка при обработке {country_name}: {e}")
                continue

        return result