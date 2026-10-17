import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Atmos | Weather Intelligence",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "search_history.json"

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# ---------------------------------------------------------
# PROFESSIONAL STYLING
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu, footer, header, [data-testid="stSidebar"] {
        visibility: hidden;
        display: none;
    }

    .stApp {
        background:
            radial-gradient(circle at 5% 0%, #e9f0ff 0%, transparent 32%),
            linear-gradient(135deg, #f7f9fd 0%, #f1f5fb 100%);
        color: #17233d;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        color: #17233d !important;
        letter-spacing: -0.5px;
    }

    .brand {
        font-family: 'Manrope', sans-serif;
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: 2px;
        color: #253b70;
    }

    .eyebrow {
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #657594;
        font-size: 0.72rem;
        font-weight: 700;
    }

    .muted {
        color: #75829a;
        font-size: 0.91rem;
    }

    .weather-hero {
        background: linear-gradient(120deg, #172c57 0%, #314f89 58%, #637fbd 100%);
        color: white;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 16px 38px rgba(35, 59, 108, 0.16);
        min-height: 260px;
    }

    .weather-hero h2, .weather-hero h3,
    .weather-hero p, .weather-hero div {
        color: white !important;
    }

    .hero-temp {
        font-family: 'Manrope', sans-serif;
        font-size: clamp(3.8rem, 7vw, 5.5rem);
        line-height: 1.1;
        font-weight: 800;
        letter-spacing: -4px;
        margin: 10px 0;
    }

    .hero-icon {
        font-size: 4rem;
        text-align: right;
    }

    .panel {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #e7ecf5;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 7px 22px rgba(36, 54, 92, 0.045);
        min-height: 112px;
    }

    .panel-label {
        color: #75829a;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .panel-value {
        font-family: 'Manrope', sans-serif;
        font-size: 1.65rem;
        font-weight: 800;
        color: #1c2b49;
    }

    .panel-sub {
        color: #8490a5;
        font-size: 0.78rem;
        margin-top: 4px;
    }

    .section-title {
        font-family: 'Manrope', sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: #1d2b48;
        margin-top: 1.1rem;
        margin-bottom: 0.15rem;
    }

    .forecast-card {
        background: white;
        border: 1px solid #e5eaf3;
        border-radius: 17px;
        padding: 16px 10px;
        text-align: center;
        min-height: 150px;
        box-shadow: 0 6px 18px rgba(36, 54, 92, 0.04);
    }

    .forecast-day {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64728c;
    }

    .forecast-icon {
        font-size: 1.8rem;
        margin: 10px 0;
    }

    .forecast-temps {
        font-weight: 800;
        color: #233354;
        font-size: 0.95rem;
    }

    .forecast-rain {
        font-size: 0.73rem;
        color: #6384bd;
        margin-top: 7px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e6ebf4;
        border-radius: 17px;
        padding: 18px;
        box-shadow: 0 5px 16px rgba(36, 54, 92, 0.035);
    }

    div[data-testid="stMetricLabel"] {
        color: #6f7d96;
    }

    .stButton > button {
        border-radius: 11px;
        min-height: 42px;
        font-weight: 700;
        border: 1px solid #dce4f2;
    }

    .stButton > button[kind="primary"] {
        background: #263e70;
        border: 1px solid #263e70;
        color: white;
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 11px;
    }

    .footer {
        color: #8490a5;
        font-size: 0.78rem;
        text-align: center;
        padding-top: 24px;
    }

    hr {
        border-color: #e5eaf3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# WEATHER CODE HELPERS
# ---------------------------------------------------------
WEATHER_CODES = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    56: ("Freezing drizzle", "🌧️"),
    57: ("Heavy freezing drizzle", "🌧️"),
    61: ("Light rain", "🌦️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    66: ("Freezing rain", "🌧️"),
    67: ("Heavy freezing rain", "🌧️"),
    71: ("Light snow", "🌨️"),
    73: ("Moderate snow", "❄️"),
    75: ("Heavy snow", "❄️"),
    77: ("Snow grains", "❄️"),
    80: ("Rain showers", "🌦️"),
    81: ("Moderate showers", "🌧️"),
    82: ("Heavy showers", "⛈️"),
    85: ("Snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with hail", "⛈️"),
    99: ("Severe thunderstorm", "⛈️"),
}


def weather_info(code):
    return WEATHER_CODES.get(int(code or 0), ("Weather conditions", "🌡️"))


# ---------------------------------------------------------
# SEARCH HISTORY
# ---------------------------------------------------------
def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2, ensure_ascii=False)
    except OSError:
        st.warning("Search history could not be saved on this device.")


def location_label(place):
    parts = [
        place.get("name"),
        place.get("admin1"),
        place.get("country"),
    ]

    unique_parts = []
    for part in parts:
        if part and part not in unique_parts:
            unique_parts.append(part)

    return ", ".join(unique_parts)


def add_to_history(place):
    history = load_history()
    label = location_label(place)

    entry = {
        "name": place.get("name", ""),
        "admin1": place.get("admin1", ""),
        "country": place.get("country", ""),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "timezone": place.get("timezone", "auto"),
        "label": label,
        "searched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    # Move repeated locations to the top instead of duplicating them.
    history = [
        item for item in history
        if item.get("label") != label
    ]

    history.insert(0, entry)
    history = history[:20]
    save_history(history)
    return history


# ---------------------------------------------------------
# API FUNCTIONS
# ---------------------------------------------------------
@st.cache_data(ttl=900, show_spinner=False)
def search_places(city_name):
    response = requests.get(
        GEOCODING_URL,
        params={
            "name": city_name,
            "count": 10,
            "language": "en",
            "format": "json",
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json().get("results", [])


@st.cache_data(ttl=300, show_spinner=False)
def get_weather(latitude, longitude, timezone):
    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone or "auto",
            "forecast_days": 7,
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,is_day,precipitation,"
                "weather_code,wind_speed_10m,wind_direction_10m,"
                "surface_pressure"
            ),
            "hourly": (
                "temperature_2m,precipitation_probability,"
                "relative_humidity_2m,wind_speed_10m,weather_code"
            ),
            "daily": (
                "weather_code,temperature_2m_max,temperature_2m_min,"
                "precipitation_probability_max,sunrise,sunset,"
                "uv_index_max"
            ),
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "selected_place" not in st.session_state:
    st.session_state.selected_place = None

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "search_counter" not in st.session_state:
    st.session_state.search_counter = 0

if "last_updated" not in st.session_state:
    st.session_state.last_updated = None

# ---------------------------------------------------------
# TOP HEADER
# ---------------------------------------------------------
header_left, header_right = st.columns([3, 1])

with header_left:
    st.markdown(
        '<div class="brand">◈ ATMOS <span style="color:#8c9ab3;'
        'font-weight:500;letter-spacing:1px;">WEATHER INTELLIGENCE</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 style='margin-bottom:0;'>Weather, clearly.</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="muted">Real-time conditions and forecasts for the places that matter.</div>',
        unsafe_allow_html=True,
    )

with header_right:
    st.write("")
    if st.button("↻ Refresh weather", use_container_width=True):
        get_weather.clear()
        st.rerun()

st.write("")

# ---------------------------------------------------------
# SEARCH BAR
# ---------------------------------------------------------
with st.container(border=True):
    st.markdown("**Explore a location**")
    search_col, search_button_col = st.columns([5, 1])

    with search_col:
        city_query = st.text_input(
            "City, state, or country",
            placeholder="e.g. Mysuru, Karnataka or London",
            label_visibility="collapsed",
            key="city_query",
        )

    with search_button_col:
        search_clicked = st.button(
            "Search location",
            type="primary",
            use_container_width=True,
        )

    if search_clicked:
        if not city_query.strip():
            st.warning("Enter a city, state, or location to search.")
        else:
            try:
                with st.spinner("Finding locations..."):
                    results = search_places(city_query.strip())

                st.session_state.search_results = results
                st.session_state.search_counter += 1

                if results:
                    st.success(
                        f"Found {len(results)} matching location(s). "
                        "Choose the correct city and state below."
                    )
                else:
                    st.warning("No matching location found. Try another spelling.")

            except requests.RequestException:
                st.error("Unable to search locations. Check your internet connection.")

    if st.session_state.search_results:
        labels = [location_label(place) for place in st.session_state.search_results]

        chosen_label = st.selectbox(
            "Select the full location",
            labels,
            key=f"location_choice_{st.session_state.search_counter}",
        )

        selected_index = labels.index(chosen_label)
        selected_result = st.session_state.search_results[selected_index]

        if st.button("View this location", type="primary"):
            st.session_state.selected_place = selected_result
            add_to_history(selected_result)
            st.session_state.last_updated = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
            st.rerun()

# ---------------------------------------------------------
# SEARCH HISTORY
# ---------------------------------------------------------
history = load_history()

with st.expander(f"Recent searches  ·  {len(history)} saved locations", expanded=False):
    if not history:
        st.caption("Your searched locations will appear here.")
    else:
        history_labels = [item.get("label", "Unknown location") for item in history]

        history_col, history_button_col = st.columns([5, 1])

        with history_col:
            selected_history_label = st.selectbox(
                "Choose a recent location",
                history_labels,
                label_visibility="collapsed",
                key="history_choice",
            )

        with history_button_col:
            if st.button("Open", use_container_width=True):
                selected_history = next(
                    item for item in history
                    if item.get("label") == selected_history_label
                )
                st.session_state.selected_place = selected_history
                st.session_state.last_updated = datetime.now().strftime(
                    "%d %b %Y, %I:%M:%S %p"
                )
                st.rerun()

st.write("")

# ---------------------------------------------------------
# CURRENT WEATHER
# ---------------------------------------------------------
place = st.session_state.selected_place

if place:
    full_location = location_label(place)

    try:
        with st.spinner(f"Loading weather for {full_location}..."):
            weather = get_weather(
                place["latitude"],
                place["longitude"],
                place.get("timezone", "auto"),
            )

        current = weather["current"]
        daily = weather["daily"]
        hourly = weather["hourly"]

        description, icon = weather_info(current.get("weather_code"))

        st.markdown(
            f"""
            <div class="eyebrow">CURRENT CONDITIONS</div>
            <div style="font-size:1.55rem;font-weight:800;margin-top:4px;">
                {full_location}
            </div>
            <div class="muted">
                Local time: {current.get("time", "").replace("T", " ")}
                &nbsp; · &nbsp; Time zone: {weather.get("timezone_abbreviation", weather.get("timezone", "Local"))}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        hero_left, hero_right = st.columns([1.5, 1])

        with hero_left:
            st.markdown(
                f"""
                <div class="weather-hero">
                    <div style="font-size:0.82rem;letter-spacing:1.5px;
                                text-transform:uppercase;opacity:0.8;">
                        {description}
                    </div>
                    <div class="hero-temp">{current.get("temperature_2m", "--")}°</div>
                    <div style="font-size:1rem;opacity:0.92;">
                        Feels like {current.get("apparent_temperature", "--")}°C
                    </div>
                    <div style="font-size:0.85rem;margin-top:24px;opacity:0.82;">
                        Updated from live weather data
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with hero_right:
            st.markdown(
                f"""
                <div class="panel" style="height:100%;">
                    <div style="font-size:3.6rem;text-align:center;margin-top:8px;">{icon}</div>
                    <div style="text-align:center;font-size:1.15rem;font-weight:800;
                                color:#253554;margin-top:8px;">{description}</div>
                    <div style="text-align:center;color:#8190a9;font-size:0.85rem;
                                margin-top:8px;">{full_location}</div>
                    <hr>
                    <div style="display:flex;justify-content:space-between;padding:7px 0;">
                        <span style="color:#75829a;">Daylight</span>
                        <b style="color:#263653;">{"Daytime" if current.get("is_day") else "Nighttime"}</b>
                    </div>
                    <div style="display:flex;justify-content:space-between;padding:7px 0;">
                        <span style="color:#75829a;">Wind direction</span>
                        <b style="color:#263653;">{current.get("wind_direction_10m", "--")}°</b>
                    </div>
                    <div style="display:flex;justify-content:space-between;padding:7px 0;">
                        <span style="color:#75829a;">Coordinates</span>
                        <b style="color:#263653;">{place["latitude"]:.2f}, {place["longitude"]:.2f}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('<div class="section-title">Weather at a glance</div>', unsafe_allow_html=True)
        st.write("")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Humidity", f'{current.get("relative_humidity_2m", "--")}%')
        m2.metric("Wind speed", f'{current.get("wind_speed_10m", "--")} km/h')
        m3.metric("Precipitation", f'{current.get("precipitation", "--")} mm')
        m4.metric("Surface pressure", f'{current.get("surface_pressure", "--")} hPa')

        # Today's sunlight and forecast
        st.markdown('<div class="section-title">Today’s outlook</div>', unsafe_allow_html=True)
        st.write("")

        today_cols = st.columns(4)

        today_cols[0].metric(
            "High",
            f'{daily["temperature_2m_max"][0]:.1f}°C',
        )
        today_cols[1].metric(
            "Low",
            f'{daily["temperature_2m_min"][0]:.1f}°C',
        )
        today_cols[2].metric(
            "Rain probability",
            f'{daily["precipitation_probability_max"][0] or 0}%',
        )
        today_cols[3].metric(
            "Maximum UV index",
            f'{daily["uv_index_max"][0]:.1f}',
        )

        sunrise = daily["sunrise"][0].split("T")[-1]
        sunset = daily["sunset"][0].split("T")[-1]

        sun1, sun2 = st.columns(2)
        with sun1:
            st.markdown(
                f'<div class="panel"><div class="panel-label">SUNRISE</div>'
                f'<div class="panel-value"> {sunrise}</div></div>',
                unsafe_allow_html=True,
            )
        with sun2:
            st.markdown(
                f'<div class="panel"><div class="panel-label">SUNSET</div>'
                f'<div class="panel-value"> {sunset}</div></div>',
                unsafe_allow_html=True,
            )

        # 7-day forecast cards
        st.markdown('<div class="section-title">7-day forecast</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="muted">A quick look at the week ahead.</div>',
            unsafe_allow_html=True,
        )
        st.write("")

        forecast_columns = st.columns(7)

        for i, col in enumerate(forecast_columns):
            day = pd.to_datetime(daily["time"][i])
            day_label = "Today" if i == 0 else day.strftime("%a")
            day_description, day_icon = weather_info(daily["weather_code"][i])
            rain_chance = daily["precipitation_probability_max"][i] or 0

            with col:
                st.markdown(
                    f"""
                    <div class="forecast-card">
                        <div class="forecast-day">{day_label}</div>
                        <div class="forecast-icon">{day_icon}</div>
                        <div class="forecast-temps">
                            {daily["temperature_2m_max"][i]:.0f}°
                            <span style="color:#9ba6b9;font-weight:500;">
                            {daily["temperature_2m_min"][i]:.0f}°
                            </span>
                        </div>
                        <div class="forecast-rain">☂ {rain_chance}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                with st.popover("Details", use_container_width=True):
                    st.write(f"**{day_description}**")
                    st.write(f"High: {daily['temperature_2m_max'][i]:.1f}°C")
                    st.write(f"Low: {daily['temperature_2m_min'][i]:.1f}°C")
                    st.write(f"Rain chance: {rain_chance}%")
                    st.write(f"UV index: {daily['uv_index_max'][i]}")

        # Hourly forecast chart
        st.markdown('<div class="section-title">Hourly forecast</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="muted">Temperature and precipitation probability over the next 24 hours.</div>',
            unsafe_allow_html=True,
        )
        st.write("")

        hourly_df = pd.DataFrame({
            "Time": pd.to_datetime(hourly["time"]),
            "Temperature (°C)": hourly["temperature_2m"],
            "Rain probability (%)": hourly["precipitation_probability"],
            "Humidity (%)": hourly["relative_humidity_2m"],
            "Wind (km/h)": hourly["wind_speed_10m"],
        })

        hourly_df = hourly_df[
            hourly_df["Time"] >= pd.Timestamp(current["time"])
        ].head(24)

        chart_tab, table_tab = st.tabs(["Temperature chart", "Hourly details"])

        with chart_tab:
            chart_data = hourly_df.set_index("Time")[["Temperature (°C)"]]
            st.line_chart(chart_data, height=300)

            st.caption("Temperatures are shown in degrees Celsius.")

        with table_tab:
            display_df = hourly_df.copy()
            display_df["Time"] = display_df["Time"].dt.strftime("%a, %I %p")
            display_df = display_df.rename(columns={"Time": "Local time"})
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

        st.write("")
        with st.expander("Location and data details"):
            st.write(f"**Location:** {full_location}")
            st.write(f"**Latitude:** {place['latitude']}")
            st.write(f"**Longitude:** {place['longitude']}")
            st.write(f"**Time zone:** {weather.get('timezone', 'Local')}")
            st.write(f"**Data provider:** Open-Meteo")
            st.write(f"**Last refreshed in this session:** {datetime.now().strftime('%d %b %Y, %I:%M:%S %p')}")

    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as exc:
        st.error(
            "Weather data could not be loaded. Please refresh or select another location."
        )
        with st.expander("Technical details"):
            st.code(str(exc))

else:
    # Welcome state before a location is selected
    st.markdown(
        """
        <div class="weather-hero">
            <div style="font-size:0.8rem;letter-spacing:2px;opacity:0.8;">
                YOUR WEATHER, IN ONE PLACE
            </div>
            <div style="font-family:Manrope,sans-serif;font-size:2.4rem;
                        font-weight:800;margin-top:14px;max-width:680px;">
                A clearer view of the day ahead.
            </div>
            <div style="font-size:1rem;opacity:0.9;max-width:620px;
                        margin-top:14px;line-height:1.8;">
                Search for a city to explore live weather conditions, hourly
                temperatures, rain chances, and a seven-day forecast.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown('<div class="section-title">What you can explore</div>', unsafe_allow_html=True)
    st.write("")

    feature_cols = st.columns(4)
    features = [
        ("Live conditions", "Temperature, feels-like, humidity, and wind."),
        ("Hourly outlook", "Track changing temperatures through the day."),
        ("7-day forecast", "Compare daily highs, lows, rain chance, and UV."),
        ("Saved locations", "Reopen recent searches with their state and country."),
    ]

    for col, (title, description) in zip(feature_cols, features):
        with col:
            st.markdown(
                f"""
                <div class="panel">
                    <div style="font-weight:800;color:#243452;margin-top:12px;">
                        {title}
                    </div>
                    <div class="muted" style="margin-top:7px;">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown(
    """
    <div class="footer">
        ATMOS Weather Intelligence · Weather data provided by Open-Meteo
        · Built with Python and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.selected_place:
    st_autorefresh(
        interval=5 * 60 * 1000,
        key="weather_auto_refresh",
    )