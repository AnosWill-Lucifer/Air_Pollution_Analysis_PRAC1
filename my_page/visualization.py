import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page 3: Data Visualization
def show():
    st.title("📊 Interactive Data Visualization")
    st.markdown(
        """
        Explore how air quality and pollution metrics evolve over time and relate to each other.
        Use the controls below to select your feature and time resolution, then scroll down for
        a suite of prebuilt summary charts and detailed explanations.
        """
    )

    # Load summaries
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'yearly_summary.csv')
    yearly   = pd.read_csv(csv_path,parse_dates=['DATETIME'], index_col='DATETIME')
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'monthly_summary.csv')
    monthly  = pd.read_csv(csv_path,parse_dates=['DATETIME'], index_col='DATETIME')
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'weekly_summary.csv')
    weekly   = pd.read_csv(csv_path,parse_dates=['DATETIME'], index_col='DATETIME')
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'daily_summary.csv')
    daily    = pd.read_csv(csv_path,parse_dates=['DATETIME'], index_col='DATETIME')
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'seasonal_summary.csv')
    seasonal = pd.read_csv(csv_path,index_col='SEASONS')

    # Convert PeriodIndex to Timestamp for consistency
    for df in (yearly, monthly, weekly, daily):
        if hasattr(df.index, "to_timestamp"):
            df.index = df.index.to_timestamp()

    # --- Custom Plot controls ---
    st.subheader("🔍 Custom Plot")
    feats = [
        'AQI','PM2.5','PM10','SO2','NO2','CO','O3',
        'Vehicular_Pollution','Industrial_Pollution'
    ]
    period_map = {
        'Yearly': yearly,
        'Monthly': monthly,
        'Weekly': weekly,
        'Daily': daily,
        'Seasonal': seasonal
    }
    feat   = st.selectbox("Select Feature:", feats)
    period = st.selectbox("Select Time Resolution:", list(period_map.keys()))

    df_scope = period_map[period]
    fig, ax = plt.subplots(figsize=(10,4))
    if period == 'Seasonal':
        df_scope[feat].plot.bar(ax=ax, color='teal')
        summary = (
            f"📈 The seasonal bar chart shows the average **{feat}** for each season, "
            "highlighting when pollution peaks (e.g., winter heating vs. summer smog)."
        )
    else:
        df_scope[feat].plot.line(ax=ax, color='navy', linewidth=2)
        summary = (
            f"📈 The {period.lower()} line chart for **{feat}** reveals trends and fluctuations "
            "over time—useful for spotting long-term shifts or anomalies."
        )
    ax.set_xlabel(period)
    ax.set_ylabel(feat)
    st.pyplot(fig, use_container_width=True)
    st.markdown(summary)

    # --- Prebuilt summary charts ---
    st.markdown("---")
    st.markdown("### 📈 Air Quality Index (AQI) Overview")

    # 1) Average AQI per Year
    st.subheader("Average AQI per Year")
    # Ensure datetime index is Timestamp
    df_yearly = yearly.copy()
    df_yearly.index = pd.to_datetime(df_yearly.index)
    # Create Year string column for categorical axis
    plot_df = (
        df_yearly
        .assign(YearStr=df_yearly.index.year.astype(str))
        .reset_index(drop=True)[['YearStr', 'AQI']]
    )
    fig, ax = plt.subplots(figsize=(6,4))
    sns.pointplot(data=plot_df, x='YearStr', y='AQI', color='crimson', ax=ax)
    ax.set_xlabel("Year")
    st.pyplot(fig, use_container_width=True)
    st.markdown(
        "👉 This point plot shows how the annual average AQI has changed, indicating "
        "whether overall air quality is improving or deteriorating year by year."
    )

    # 2) Average Monthly AQI per Year
    st.subheader("Average Monthly AQI per Year")
    df_monthly = monthly.reset_index()
    df_monthly['Year'] = df_monthly['DATETIME'].dt.year
    fig, ax = plt.subplots(figsize=(10,4))
    sns.lineplot(
        data=df_monthly,
        x='DATETIME', y='AQI',
        hue='Year',
        palette='tab10',
        ax=ax
    )
    ax.legend(title='Year', bbox_to_anchor=(1.05,1))
    st.pyplot(fig, use_container_width=True)
    st.markdown(
        "👉 Overlaying each year's monthly AQI trend reveals seasonal cycles and year-to-year shifts."
    )

    # 3) Average AQI per Station per Year
    st.subheader("Average AQI per Station per Year")
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'merged_data_eda.csv')
    df_eda = pd.read_csv(csv_path,parse_dates=['DATETIME'],index_col='DATETIME')
    df_sta = df_eda.reset_index()
    df_sta['Year'] = df_sta['DATETIME'].dt.year
    fig, ax = plt.subplots(figsize=(10,4))
    sns.lineplot(
        data=df_sta,
        x='Year', y='AQI', hue='STATION',
        palette='tab20', ax=ax
    )
    ax.legend(title='Station', bbox_to_anchor=(1.05,1))
    st.pyplot(fig, use_container_width=True)
    st.markdown(
        "👉 Comparing stations side-by-side highlights which areas consistently face worse pollution."
    )

    # --- Vehicle vs Industrial Emissions ---
    st.markdown("---")
    st.markdown("### 🚗 Vehicle & 🏭 Industrial Emissions Impact")

    st.subheader("Yearly Average Pollution Trend")
    fig, ax = plt.subplots(figsize=(10,4))
    sns.lineplot(
        data=yearly[['Vehicular_Pollution','Industrial_Pollution']],
        ax=ax
    )
    ax.set_ylabel("Pollution Level")
    ax.legend(title='Type')
    st.pyplot(fig, use_container_width=True)
    st.markdown(
        "👉 This chart shows how traffic-related and industrial emissions have trended over years, indicating which source dominates."
    )

    st.subheader("Seasonal Pollution Pattern")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(
        x=seasonal.index,
        y='Vehicular_Pollution',
        data=seasonal,
        color='orange',
        label='Vehicular'
    )
    sns.barplot(
        x=seasonal.index,
        y='Industrial_Pollution',
        data=seasonal,
        color='purple',
        alpha=0.6,
        label='Industrial'
    )
    ax.legend()
    st.pyplot(fig, use_container_width=True)
    st.markdown(
        "👉 Side-by-side seasonal bars compare how vehicle and industrial emissions vary across Winter/Spring/Summer/Autumn."
    )

    # --- Impact of Rain & Weather ---
    st.markdown("---")
    st.markdown("### ☔ Impact of Rain & Weather")
    st.subheader("Rainfall vs AQI")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.scatterplot(x='RAIN', y='AQI', data=df_eda, ax=ax, color='blue', alpha=0.5)
    st.pyplot(fig, use_container_width=True)
    st.markdown(
        "👉 Scatter plot reveals whether increased rainfall tends to coincide with lower AQI (cleaner air)."
    )

    st.subheader("Seasonal Temperature & Dew Point")
    fig, axes = plt.subplots(1,2, figsize=(12,4))
    sns.boxplot(x='SEASONS', y='TEMP', data=df_eda, ax=axes[0], palette='cool')
    axes[0].set_title("Temperature by Season")
    sns.boxplot(x='SEASONS', y='DEWP', data=df_eda, ax=axes[1], palette='autumn')
    axes[1].set_title("Dew Point by Season")
    st.pyplot(fig, use_container_width=True)
    st.markdown(
        "👉 Boxplots show the distribution of temperature and dew point across seasons, helping to contextualize pollutant dispersion conditions."
    )

    # --- Correlation Heatmap ---
    st.markdown("---")
    st.subheader("🔗 Correlation Heatmap")
    num_df = df_eda.select_dtypes(include='number')
    corr = num_df.corr()
    fig2, ax2 = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
    st.pyplot(fig2, use_container_width=True)
    st.markdown(
        "📊 The heatmap highlights strong positive or negative relationships between features, guiding feature selection for modeling."
    )