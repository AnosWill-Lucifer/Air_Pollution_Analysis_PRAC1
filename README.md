# 🌆 Beijing Air Quality Forecasting Dashboard

[![Streamlit](https://img.shields.io/badge/Streamlit-%23FF4B4B.svg?logo=streamlit\&logoColor=white)](https://streamlit.io) [![Python](https://img.shields.io/badge/Python-%233776AB.svg?logo=python\&logoColor=white)](https://python.org)

Welcome to the Beijing Air Quality Index (AQI) Forecasting Dashboard! Dive into a full data-science pipeline—from raw sensor readings to interactive predictions—built with Streamlit. 😊

---

## 📋 Table of Contents

1. [🚀 Project Overview](#-project-overview)
2. [📂 Data Collection](#-data-collection)
3. [🧹 Cleaning & Preprocessing](#-cleaning--preprocessing)
4. [🔍 Exploratory Data Analysis](#-exploratory-data-analysis)
5. [🤖 Modeling & Prediction](#-modeling--prediction)
6. [🖥️ Streamlit App](#-streamlit-app)
7. [🔮 What's Next](#-whats-next)
8. [📬 Contact](#-contact)

---

## 🚀 Project Overview

This dashboard captures hourly air-quality metrics from five distinct monitoring stations around Beijing—urban, suburban, rural, and an industrial hotspot—spanning **March 2013 to February 2017**. You'll explore how pollutants vary over time and get a live AQI forecast powered by tuned ML models. citeturn0file0

**Why build this?**

* Practice an end-to-end data-science workflow: ingestion → cleaning → EDA → modeling → deployment
* Compare urban vs. rural pollution dynamics in a major metropolis
* Create a user-friendly interface for stakeholders and researchers

---

## 📂 Data Collection

| Station Type       | File Pattern               | Records         |
| ------------------ | -------------------------- | --------------- |
| Urban              | `PRSA_Data_URBAN.csv`      | Hourly, 2013–17 |
| Suburban           | `PRSA_Data_SUBUR.csv`      | Hourly, 2013–17 |
| Rural              | `PRSA_Data_RURAL.csv`      | Hourly, 2013–17 |
| Industrial Hotspot | `PRSA_Data_INDUSTRIAL.csv` | Hourly, 2013–17 |

Each CSV includes:

* **Pollutants:** PM₂.₅, PM₁₀, SO₂, NO₂, CO, O₃
* **Weather:** Temperature, Pressure, Dew Point, Rain, Wind Speed & Direction

---

## 🧹 Cleaning & Preprocessing

1. **Merge & Interpolate**: Combined all station files → `merged_data.csv`. Imputed missing hours via forward/backward linear interpolation.
2. **Cleanup**: Dropped duplicates & remaining nulls (<1% of rows) → `merged_data_final.csv`.
3. **Feature Engineering**:

   * Calculated **AQI** per pollutant & overall category
   * Labeled **vehicular vs. industrial** contributions
   * Encoded **season** and **time-based** features
4. **Outlier Treatment**: Winsorized at 1st/99th percentiles & removed extreme tails → `merged_data_no_outliers.csv`

---

## 🔍 Exploratory Data Analysis

* **Descriptive Stats:** Mean, median, skewness, kurtosis
* **Temporal Trends:** Yearly, monthly, weekly, daily & seasonal breakdowns
* **Visual Insights:**

  * Line plots & heatmaps of pollutant levels
  * Radar charts contrasting station profiles
  * Pairplots & jointplots for relationships
  * Boxplots to spot outliers & distributions
* **Correlation Matrix:** Pollutants vs. AQI & emission sources

---

## 🤖 Modeling & Prediction

* **Preprocessing:** Train/test split → StandardScaler + `SelectKBest` (top 10 features)
* **Algorithms Tested:** Ridge, Decision Tree, Random Forest, Gradient Boosting, SVR, KNN
* **Hyperparameter Tuning:** `GridSearchCV` for optimal settings
* **Results:** Stored in `model_performance_tuned.csv`; predictions in `model_predictions_tuned.csv`

| Model             | MAE   | MSE   | RMSE  | R²    |
| ----------------- | ----- | ----- | ----- | ----- |
| Random Forest     | **X** | **X** | **X** | **X** |
| Gradient Boosting | X     | X     | X     | X     |
| ...               |       |       |       |       |

*View the full performance table in the app.*

---

## 🖥️ Streamlit App

Use the sidebar to explore each section:

1. **Project & Data Summary** – Goals, station map, raw-data preview
2. **Theory & Pipeline** – Step-by-step processing details
3. **Visualizations** – Interactive charts with explanations
4. **Modeling & Prediction** – Performance metrics, error plots, live AQI forecast form
5. **Summary & Insights** – Key takeaways and recommendations

**Run locally:**

```bash
git clone <repo-url>
pip install -r requirements.txt
python -m streamlit run app.py
```

---

## 🔮 What's Next

* Integrate **traffic volume** & **satellite AOD** for enhanced modeling
* Experiment with **deep-learning** time-series architectures (LSTM / Transformer)
* Deploy on **Heroku** or **AWS** for wider access

---

## 📬 Contact

**Abdullah Ajmal** (MSc Robotics & AI, Cardiff Met 2025)
✉️ [st20307179@outlook.cardiffmet.ac.uk](mailto:st20307179@outlook.cardiffmet.ac.uk)

*Feel free to open issues or pull requests!*
