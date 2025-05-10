import streamlit as st
import pandas as pd
import os

# Page 1: Project & Data Summary
def show():
    # Page header
    st.title("🌫️ Beijing Air Quality Analysis")
    st.markdown(
        """
        Welcome to the **Beijing Air Quality Dashboard**—an end-to-end exploration
        and forecasting platform for hourly AQI (Air Quality Index).
        This project brings together pollutant measurements, meteorological data,
        and machine-learning models to help understand and predict pollution levels.
        """,
        unsafe_allow_html=True
    )

    # Objectives
    st.header("🎯 Project Objectives")
    st.markdown(
        """
        1. **Forecast** hourly AQI using historical pollutant and weather data.
        2. **Compare** pollution patterns across urban, suburban, and rural sites.
        3. **Evaluate** multiple regression models to identify the most accurate predictors.
        """
    )

    # Stations & Rationale
    st.subheader("📍 Monitoring Stations & Rationale")
    st.markdown(
        """
        Selected **five** key stations in Beijing to capture a wide variety of environments:
        - **Gucheng** (Urban-industrial hotspot)
        - **Dongsi** (Central urban area)
        - **Guanyuan** (Residential – suburban)
        - **Shunyi** (Outskirts – semi-rural)
        - **Huairou** (Rural/suburban transition)

        **Why these stations?**
        • **Geographical diversity** ensures representation of traffic, industry, and background levels.
        • **Data quality**—each site has consistently low missing rates, ideal for reliable modeling.
        """
    )
    st.subheader("🗃️ Raw Dataset Preview")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'merged_data.csv')
    df_raw = pd.read_csv(csv_path)
    col1, col2, col3 = st.columns(3)
    col1.metric("📅 Timeframe Start", df_raw['YEAR'].min())
    col2.metric("📅 Timeframe End",   df_raw['YEAR'].max())
    col3.metric("📝 Total Records",   f"{len(df_raw):,}")

    st.dataframe(df_raw.head(15), height=300)

    # Variables list
    st.markdown(
        """
        **Data Variables**
        - **Pollutants**: PM2.5, PM10, SO₂, NO₂, CO, O₃
        - **Meteorological**: Temperature (TEMP), Pressure (PRES), Dew Point (DEWP), Rainfall (RAIN), Wind Speed (WSPM), Wind Direction (wd)
        - **Contextual**: Station name, DateTime
        """
    )

    # Final descriptive note
    st.markdown(
        """
        ---
        This **interactive dashboard** will guide you through our complete workflow—from raw data ingestion
        and cleaning, through feature engineering and exploratory analysis, to advanced modeling and live AQI prediction.
        Use the sidebar to navigate between summary, processing steps, visual analytics, and predictive modeling pages.
        """
    )
