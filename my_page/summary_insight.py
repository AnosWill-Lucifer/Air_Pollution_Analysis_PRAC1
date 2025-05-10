import streamlit as st
import pandas as pd
import os
import io
import zipfile
import glob

def show():
    st.title("📝 Summary & Insights")
    st.markdown(
        """
        Welcome to the **Summary & Insights** page. Here You recap what has been done, what were the learnings,
        and the key outcomes of the Air Quality Index (AQI) forecasting project in Beijing.
        """
    )

    # --- Project Recap ---
    st.header("1️⃣ Project Recap")
    st.markdown(
        """
        **Objective:** Forecast hourly AQI using pollutant & meteorological data from five Beijing stations (Gucheng, Dongsi, Guanyuan, Shunyi, Huairou).
        **Why these stations?** They span urban, suburban, and rural areas, capturing a full spectrum of pollution dynamics.
        """
    )

    # --- Data Processing Summary ---
    st.header("2️⃣ Data Processing")
    st.markdown(
        """
        1. **Merged & cleaned** five CSVs, filtered unusable rows.
        2. **Imputed** missing values via linear interpolation, dropped remaining <1% of data.
        3. **Engineered features**: Combined daily/hourly datetime, computed AQI & AQI category, grouped vehicular vs industrial pollution.
        4. **Encoded** wind direction, station, seasons, and AQI category into numeric codes.
        5. **Winsorized** outliers at the 1st/99th percentiles to reduce the effect of extreme values.
        """
    )

    # --- EDA Key Findings ---
    st.header("3️⃣ Exploratory Data Analysis (EDA) Insights")
    st.markdown(
        """
        - **Seasonality:** Winter months saw the highest PM₂.₅, PM₁₀, and AQI levels; summer was markedly cleaner.
        - **Vehicular vs Industrial:** Traffic‐related pollutants (NO₂, CO) peaked during rush hours and weekdays, whereas O₃ showed midday summer spikes.
        - **Weather impact:** Rain events correlated with temporary dips in AQI, confirming wash‐out effects.
        - **Correlations:** PM₂.₅ and PM₁₀ were highly correlated (r≈0.9), while O₃ anti‐correlated with NO₂ (r≈–0.5), suggesting photochemical relationships.
        """
    )

    # --- Modeling & Performance ---
    st.header("4️⃣ Modeling & Performance Summary")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'model_performance_tuned.csv')
    perf = pd.read_csv(csv_path, index_col=0)
    best_model = perf['R2'].idxmax()
    best_r2    = perf['R2'].max()
    st.markdown(
        f"""
        We trained six regression models on the top-10 features (selected by **SelectKBest** after scaling):
        - **Best performer:** {best_model} (R² = {best_r2:.3f})
        - **Typical R² range:** {perf['R2'].min():.3f} – {perf['R2'].max():.3f}
        - **RMSE range:** {perf['RMSE'].min():.2f} – {perf['RMSE'].max():.2f} AQI units
        - **MAE range:**  {perf['MAE'].min():.2f} – {perf['MAE'].max():.2f} AQI units
        """
    )
    st.dataframe(perf.style.format({
        'R2':'{:.3f}', 'RMSE':'{:.2f}',
        'MAE':'{:.2f}', 'MAPE_%':'{:.2f}%'
    }), height=200)

    # --- Prediction Tool Reminder ---
    st.header("5️⃣ Live Prediction Tool")
    st.markdown(
        """
        On the **Modeling & Prediction** page you can:
        1. **Select** any of the six trained models.
        2. **Enter** real‐time pollutant & meteorology values.
        3. **Get** an immediate AQI forecast with its category and model confidence (R²).
        This enables on-the-fly air quality assessment for decision support.
        """
    )

    # --- Final Takeaways ---
    st.header("🔑 Final Takeaways")
    st.markdown(
        """
        - **Feature importance:** PM₂.₅, PM₁₀, NO₂, CO, O₃, DEWP, WSPM, and vehicle vs industrial aggregates were most predictive.
        - **Seasonal patterns** dominate AQI fluctuations—any operational forecasting should incorporate weather forecasts.
        - **Model readiness:** Our best model achieves R²≈0.85, making it suitable for near‐real-time AQI alerts in Beijing.
        - **Next steps:** Incorporate traffic volume data, satellite aerosol optical depth, or deploy online learning for continuously improving forecasts.
        """
    )

    st.markdown("---")
    st.markdown(
        "✅ **Thank you** for exploring the Air Quality Forecasting project!  \n"
        "📬 Feedback and questions welcome at _st20307179@outlook.cardiffmet.ac.uk_."
    )

 # --- Download all project files as a ZIP ---
    st.markdown("---")
    st.header("📥 Download Project Files")
    st.markdown("Click below to download all CSV & PKL files used in this project as a single ZIP.")

    # construct list of files
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_dir  = os.path.join(BASE_DIR, "..", "Data_set")
    model_dir = os.path.join(BASE_DIR, "..", "Models")

    files_to_zip = glob.glob(os.path.join(data_dir, "*.csv")) + \
                   glob.glob(os.path.join(model_dir, "*.pkl"))

    # create in-memory ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for filepath in files_to_zip:
            arcname = os.path.basename(filepath)
            zf.write(filepath, arcname=arcname)
    zip_buffer.seek(0)

    st.download_button(
        label="📦 Download All Files",
        data=zip_buffer,
        file_name="Beijing_AQI_Project_Files.zip",
        mime="application/zip"
    )