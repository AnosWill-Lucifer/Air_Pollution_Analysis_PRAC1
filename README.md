````
Beijing Air Quality Forecasting Dashboard
=========================================

Hey there! 👋  
Welcome to my Air Quality Index (AQI) forecasting project for Beijing. I’ve pulled together data from five monitoring stations—urban, suburban, rural, and an industrial hotspot—to build an end-to-end Streamlit dashboard. Here’s the lowdown:

What’s Inside
-------------
1. **Raw data**  
   - Five CSVs (`PRSA_Data_*.csv`) covering March 2013 – Feb 2017  
   - Each contains hourly readings: PM₂.₅, PM₁₀, SO₂, NO₂, CO, O₃ + basic weather (TEMP, PRES, DEWP, RAIN, WSPM, wind dir)

2. **Cleaning & Preprocessing**  
   - Merged all station files into `merged_data.csv`  
   - Imputed missing values via forward linear interpolation  
   - Dropped any leftover gaps and duplicates (<1% of rows) → `merged_data_final.csv`  
   - Engineered AQI & category, vehicular vs industrial pollution, seasonal codes  
   - Winsorized outliers (1st/99th percentiles) and removed extremes → `merged_data_no_outliers.csv`  

3. **Exploratory Data Analysis**  
   - Detailed descriptive stats + skew/kurtosis  
   - Time-series summaries (yearly, monthly, weekly, daily, seasonal)  
   - Rich visualizations: line plots, radar charts, heatmaps, pairplots, jointplots, boxplots  
   - Correlation matrices for pollutants, AQI, grouped emissions  

4. **Modeling & Prediction**  
   - Train/test split, StandardScaler + SelectKBest (top 10 features)  
   - Six regression algorithms (Ridge, Decision Tree, Random Forest, GBM, SVR, KNN) tuned via GridSearchCV  
   - Performance saved in `model_performance_tuned.csv`  
   - Predictions saved in `model_predictions_tuned.csv`  
   - Live prediction form with user inputs and AQI category lookup  

5. **Streamlit App**  
   - **1️⃣ Project & Data Summary** – goals, stations, raw preview  
   - **2️⃣ Theory & Processing** – detailed pipeline steps  
   - **3️⃣ Visualization** – interactive & prebuilt charts + explanations  
   - **4️⃣ Modeling & Prediction** – performance tables, scatter/error plots, live AQI forecast  
   - **5️⃣ Summary & Insights** – key takeaways, final learnings  

Getting Started
---------------
1. **Clone** this repo  
2. **Install** dependencies (e.g. in a virtualenv):
   ```bash
   pip install -r requirements.txt
````

*(Streamlit, pandas, scikit-learn, seaborn, missingno, joblib, etc.)*
3\. **Copy** all CSVs & pickle files into the project root (or adjust paths in `app.py`).
4\. **Run** the app:

```bash
streamlit run app.py
```

5. **Explore!** Use the sidebar to switch between pages and dive in.

## Why I Did It

* To practice a full data-science workflow: raw data → cleaning → EDA → modeling → deployment.
* To compare urban vs rural pollution patterns in a mega-city context.
* To learn how to stitch together multiple Python tools into a user-friendly dashboard.

## What’s Next?

* Bring in traffic counts or satellite AOD data for richer forecasting
* Experiment with deep-learning time-series models (LSTM, Transformer)

📬 Got feedback or questions? Shoot me an email at *[st20307179@outlook.cardiffmet.ac.uk](mailto:st20307179@outlook.cardiffmet.ac.uk)* — I’d love to hear from you!

— \Abdullah Ajmal, MSc Robotics & AI (Cardiff Met, 2025)

```
```