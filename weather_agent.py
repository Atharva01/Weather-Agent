from __future__ import annotations as _annotations

from dataclasses import dataclass
from typing import Any

import logfire
from devtools import debug
from httpx import AsyncClient

from pydantic_ai import Agent, ModelRetry, RunContext

@dataclass
class Deps:
    client: AsyncClient
    weather_api_key: str 
    geo_api_key: str 

weather_agent = Agent(
    "openai:gpt-3.5-turbo",
    system_prompt=(
        "Be concise, reply with one sentence."
        "Use the `get_lat_lng` tool to get the latitude and longitude of the locations, "
        "then use the `get_weather` tool to get the weather."
    ),
    deps_type=Deps,
    retries=2,
)

@weather_agent.tool
async def get_lat_lng(ctx: RunContext[Deps], location_description: str) -> dict[str, float]:
    if ctx.deps.geo_api_key is None:
        return {"lat": 51.1, "lng": -0.1}

    params = {"q": location_description, "api_key": ctx.deps.geo_api_key}
    r = await ctx.deps.client.get("https://geocode.maps.co/search", params=params)
    r.raise_for_status()
    data = r.json()

    if data:
        return {"lat": data[0]["lat"], "lng": data[0]["lon"]}
    else:
        raise ModelRetry("Could not find the location")

@weather_agent.tool
async def get_weather(ctx: RunContext[Deps], lat: float, lng: float) -> dict[str, Any]:
    if ctx.deps.weather_api_key is None:
        return {"temperature": "21 °C", "description": "Sunny"}

    params = {
        "apikey": ctx.deps.weather_api_key,
        "location": f"{lat},{lng}",
        "units": "metric",
    }
    r = await ctx.deps.client.get("https://api.tomorrow.io/v4/weather/realtime", params=params)
    r.raise_for_status()
    data = r.json()

    values = data["data"]["values"]
    code_lookup = {
        1000: "Clear, Sunny",
        1100: "Mostly Clear",
        1101: "Partly Cloudy",
        1102: "Mostly Cloudy",
        1001: "Cloudy",
        2000: "Fog",
        2100: "Light Fog",
        4000: "Drizzle",
        4001: "Rain",
        4200: "Light Rain",
        4201: "Heavy Rain",
        5000: "Snow",
        5001: "Flurries",
        5100: "Light Snow",
        5101: "Heavy Snow",
        6000: "Freezing Drizzle",
        6001: "Freezing Rain",
        6200: "Light Freezing Rain",
        6201: "Heavy Freezing Rain",
        7000: "Ice Pellets",
        7101: "Heavy Ice Pellets",
        7102: "Light Ice Pellets",
        8000: "Thunderstorm",
    }
    return {
        "temperature": f'{values["temperatureApparent"]:0.0f}°C',
        "description": code_lookup.get(values["weatherCode"], "Unknown"),
    }
