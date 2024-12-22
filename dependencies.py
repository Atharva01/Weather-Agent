import os
from dotenv import load_dotenv
from httpx import AsyncClient
from typing import Any

from weather_agent import weather_agent, Deps

load_dotenv()

async def fetch_weather(location: str) -> dict[str, Any]:
    async with AsyncClient() as client:
        weather_api_key = os.getenv("WEATHER_API_KEY")
        geo_api_key = os.getenv("GEO_API_KEY")
        deps = Deps(client=client, weather_api_key=weather_api_key, geo_api_key=geo_api_key)
        result = await weather_agent.run(f"What is the weather like in {location}?", deps=deps)
        return result.data
