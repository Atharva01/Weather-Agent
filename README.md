# Dynamic Weather Agent 🌦️

An interactive and visually dynamic weather application built with **Streamlit** and powered by **Pydantic AI**. This app fetches real-time weather updates for multiple locations, provides a visually appealing dynamic UI, and displays weather-specific icons and descriptions. Whether it's sunny, rainy, snowy, or cloudy, the app adapts its interface to reflect the current weather conditions.

## Features

- 🌍 **Multi-Location Support**: Enter multiple locations and get weather updates for each.
- 🎨 **Dynamic UI**: Background color changes dynamically based on weather conditions (e.g., sunny, cloudy, rainy, snowy).
- 🌤️ **Weather-Specific Icons**: Displays icons like ☀️ for sunny, 🌧️ for rain, and ❄️ for snow.
- 📡 **Real-Time Data**: Fetches live weather and geolocation data using APIs.
- ⚡ **AI-Driven**: Powered by **Pydantic AI** for intelligent query handling.
- 🛠️ **Customizable**: Easily extendable for additional features like hourly forecasts or alerts.

## Installation

To get started with this project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Atharva01/weather-agent
   cd weather-agent
   ```
2. **Create a virtual environment**
   ```bash
   python3 -m venv weather
   cd weather
   source bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```
4. **Update the OpenAI API Keys in given .env file**

5. **Launch Streamlit app**
   ```bash
   streamlit run weather_ui.py
   ```
