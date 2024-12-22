import asyncio
import streamlit as st
from weather_agent import weather_agent, Deps
from httpx import AsyncClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Weather code lookup
code_lookup = {
    1000: 'Clear, Sunny',
    1100: 'Mostly Clear',
    1101: 'Partly Cloudy',
    1102: 'Mostly Cloudy',
    1001: 'Cloudy',
    2000: 'Fog',
    2100: 'Light Fog',
    4000: 'Drizzle',
    4001: 'Rain',
    4200: 'Light Rain',
    4201: 'Heavy Rain',
    5000: 'Snow',
    5001: 'Flurries',
    5100: 'Light Snow',
    5101: 'Heavy Snow',
    6000: 'Freezing Drizzle',
    6001: 'Freezing Rain',
    6200: 'Light Freezing Rain',
    6201: 'Heavy Freezing Rain',
    7000: 'Ice Pellets',
    7101: 'Heavy Ice Pellets',
    7102: 'Light Ice Pellets',
    8000: 'Thunderstorm',
}

# Weather icons for dynamic UI
weather_icons = {
    'Clear, Sunny': '☀️',
    'Mostly Clear': '🌤️',
    'Partly Cloudy': '⛅',
    'Mostly Cloudy': '🌥️',
    'Cloudy': '☁️',
    'Fog': '🌫️',
    'Light Fog': '🌁',
    'Drizzle': '🌦️',
    'Rain': '🌧️',
    'Light Rain': '🌦️',
    'Heavy Rain': '🌧️',
    'Snow': '❄️',
    'Flurries': '🌨️',
    'Light Snow': '🌨️',
    'Heavy Snow': '❄️',
    'Freezing Drizzle': '🌬️',
    'Freezing Rain': '🌬️',
    'Light Freezing Rain': '🌬️',
    'Heavy Freezing Rain': '🌬️',
    'Ice Pellets': '🧊',
    'Heavy Ice Pellets': '🧊',
    'Light Ice Pellets': '🧊',
    'Thunderstorm': '⛈️',
}

# Background colors for weather descriptions
background_colors = {
    'Clear, Sunny': '#FFFAE6',
    'Mostly Clear': '#FFF5CC',
    'Partly Cloudy': '#D3D3D3',
    'Mostly Cloudy': '#C0C0C0',
    'Cloudy': '#A9A9A9',
    'Fog': '#E0E0E0',
    'Light Fog': '#F5F5F5',
    'Drizzle': '#ADD8E6',
    'Rain': '#87CEEB',
    'Light Rain': '#B0E0E6',
    'Heavy Rain': '#4682B4',
    'Snow': '#E0FFFF',
    'Flurries': '#AFEEEE',
    'Light Snow': '#F0FFFF',
    'Heavy Snow': '#B0E0E6',
    'Freezing Drizzle': '#DDEEFF',
    'Freezing Rain': '#DDEEFF',
    'Light Freezing Rain': '#DDEEFF',
    'Heavy Freezing Rain': '#A9CCE3',
    'Ice Pellets': '#B0C4DE',
    'Heavy Ice Pellets': '#B0C4DE',
    'Light Ice Pellets': '#B0C4DE',
    'Thunderstorm': '#778899',
}

async def fetch_weather(locations: list[str]) -> dict:
    """Fetch weather information using the weather_agent."""
    async with AsyncClient() as client:
        weather_api_key = os.getenv("WEATHER_API_KEY")
        geo_api_key = os.getenv("GEO_API_KEY")
        deps = Deps(
            client=client,
            weather_api_key=weather_api_key,
            geo_api_key=geo_api_key,
        )
        query = f"What is the weather like in {', '.join(locations)}?"
        result = await weather_agent.run(query, deps=deps)
        return result

def parse_weather_response(response):
    """Parse weather data from the structured response."""
    all_messages = response._all_messages
    weather_results = []

    # Extract relevant tool return parts
    for message in all_messages:
        if message.kind == "request":
            for part in message.parts:
                if part.part_kind == "tool-return" and part.tool_name == "get_weather":
                    weather_results.append(part.content)
    return weather_results

def set_dynamic_background(description):
    """Set background color dynamically based on weather description."""
    color = background_colors.get(description, '#FFFFFF')
    st.markdown(
        f"""
        <style>
        .reportview-container {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    """Streamlit UI for the weather agent."""
    st.title("Dynamic Weather Agent 🌤️")
    #st.markdown("### Get weather updates with a dynamic UI!")

    # Input for multiple locations
    locations = st.text_area(
        "Enter a location"
    )

    # Fetch and display weather information
    if st.button("Get Weather"):
        if locations.strip():
            location_list = [loc.strip() for loc in locations.split(",")]
            with st.spinner("Fetching weather..."):
                try:
                    # Run the weather fetching coroutine
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(fetch_weather(location_list))

                    # Parse and display weather data
                    weather_data = parse_weather_response(response)

                    st.markdown("### Weather Information:")
                    for loc, weather in zip(location_list, weather_data):
                        description = weather['description']
                        st.write(f"**Location:** {loc}")
                        st.write(f"**Temperature:** {weather['temperature']}")
                        st.write(f"**Description:** {description}")

                        # Add emoji for weather description
                        st.write(weather_icons.get(description, "🌍"))

                        # Set dynamic background for each location
                        set_dynamic_background(description)

                        st.markdown("---")
                except Exception as e:
                    st.error(f"Error fetching weather: {e}")
        else:
            st.warning("Please enter at least one location!")

if __name__ == "__main__":
    main()
