import streamlit as st
import pandas as pd
import os

#Page 2: Theoretical Analysis & Processing Steps
def show():
    st.title("🛠️ Data Processing & Cleaning Pipeline")
    st.markdown(
        """
        Below is a step-by-step walkthrough of how raw station data was transformed
        into a fully cleaned, feature-rich dataset ready for analysis and modeling.
        Each stage is crucial to ensure data quality, consistency, and meaningful insights.
        """,
        unsafe_allow_html=True
    )

    # Detailed steps with expandable sections
    with st.expander("1️⃣ Merge & Clean"):
        st.markdown(
            """
            **What was done:**
            - **Loaded** five separate CSV files (one per station).
            - **Concatenated** them into a single DataFrame.
            - **Dropped** rows with non-sensible timestamps or missing core identifiers.
            - **Formatted** the `datetime` column into pandas `datetime64[ns]` type for time-series operations.
            """
        )

    with st.expander("2️⃣ Missing-Value Imputation"):
        st.markdown(
            """
            **What was done:**
            - Identified gaps where sensor readings were missing.
            - Applied **linear interpolation** along the time axis to estimate these values smoothly.
            - **Dropped** any remaining rows with nulls (less than 1% of total) to maintain data integrity.
            """
        )

    with st.expander("3️⃣ Feature Engineering"):
        st.markdown(
            """
            **What was done:**
            - Calculated the **Air Quality Index (AQI)** per EPA guidelines from pollutant concentrations.
            - Assigned an **AQI_Category** (Good, Moderate, Unhealthy, etc.) for interpretability.
            - Created derived features:
              - **Vehicular_Pollution** (average of PM₂.₅, PM₁₀, NO₂, CO)
              - **Industrial_Pollution** (average of SO₂, O₃)
            - Encoded `season`, `station`, `wd` (wind direction) into categorical codes.
            """
        )

    with st.expander("4️⃣ Grouping & Summaries"):
        st.markdown(
            """
            **What was done:**
            - **Resampled** the data at multiple time scales:
              - **Yearly**, **Monthly**, **Weekly**, **Daily** averages for each feature.
              - **Hourly pattern** by grouping on hour-of-day.
              - **Seasonal** averages (Winter/Spring/Summer/Autumn).
            - Saved these summary tables (`yearly_summary.csv`, etc.) for quick lookups and visualizations.
            """
        )

    with st.expander("5️⃣ Outlier Handling"):
        st.markdown(
            """
            **What was done:**
            - Determined extreme low/high thresholds at the **1st and 99th percentiles**.
            - **Winsorized** values outside these bounds to the nearest percentile limit.
            - Removed any records still beyond these thresholds to eliminate data anomalies.
            """
        )

    # Preview of the cleaned dataset
    st.subheader("🗂️ Cleaned & Transformed Data Preview")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'merged_data_eda.csv')
    df_eda = pd.read_csv(csv_path,parse_dates=['DATETIME'],index_col='DATETIME')
    st.dataframe(df_eda.head(15), height=300)

    # Concluding note
    st.markdown(
        """
        ---
        **Next Steps:**
        With the data now fully cleaned, imputed, and enriched with engineered features,
        It is ready to be explored visually, to uncover patterns, and build predictive models.
        Navigate to the **Visualization** page to see trends and correlations,
        or jump to the **Modeling & Prediction** page to evaluate forecasting algorithms.
        """,
        unsafe_allow_html=True
    )