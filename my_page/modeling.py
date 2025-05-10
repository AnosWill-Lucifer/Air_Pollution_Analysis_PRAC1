import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

def show():
    st.title("🤖 Modeling & Prediction")
    st.markdown(
        """
        **Modeling & Prediction**: Six regression models trained on the top-10 features
        selected by SelectKBest, with scaling by StandardScaler.
        """,
        unsafe_allow_html=True
    )

    # 1) Performance table
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'model_performance_tuned.csv')
    perf = pd.read_csv(csv_path, index_col=0)
    st.subheader("📊 Model Performance")
    st.dataframe(
        perf.style.format({'R2':'{:.3f}','RMSE':'{:.2f}','MAE':'{:.2f}','MAPE_%':'{:.2f}%'}),
        height=250
    )

    # 2) Actual vs Predicted AQI
    st.subheader("🔍 Actual vs Predicted AQI")
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'model_predictions_tuned.csv')
    preds  = pd.read_csv(csv_path)
    actual = preds['Actual']
    st.markdown(
        """
        Scatter plots compare each model’s predictions (y-axis) to the true AQI values (x-axis).
        Red dashed line = perfect prediction.
        """
    )
    for model_name in perf.index:
        pred = preds[f"{model_name}_Pred"]
        fig, ax = plt.subplots(figsize=(4,4))
        sns.scatterplot(x=actual, y=pred, alpha=0.5, ax=ax)
        ax.plot([actual.min(), actual.max()],
                [actual.min(), actual.max()], 'r--')
        ax.set_xlabel("Actual AQI")
        ax.set_ylabel("Predicted AQI")
        ax.set_title(model_name)
        st.pyplot(fig, use_container_width=True)
        st.markdown(
            f"• **{model_name}** → R² {perf.at[model_name,'R2']:.3f}, "
            f"RMSE {perf.at[model_name,'RMSE']:.2f}, MAE {perf.at[model_name,'MAE']:.2f}, "
            f"MAPE {perf.at[model_name,'MAPE_%']:.2f}%"
        )
        st.write("---")

    # 3) Error comparison
    st.subheader("📈 Error Comparison")
    fig2, ax2 = plt.subplots(figsize=(8,4))
    perf[['RMSE','MAE','MAPE_%']].plot.bar(ax=ax2)
    ax2.set_xlabel("Model")
    ax2.set_ylabel("Error")
    st.pyplot(fig2, use_container_width=True)

    # 4) Live AQI Prediction
    st.subheader("🚀 Live AQI Prediction")
    st.markdown("Select a model, then enter values for the 9 pollutant & meteorology features.")

    # Load cleaned data & artifacts
    csv_path = os.path.join(BASE_DIR, '..', 'Data_set', 'merged_data_eda.csv')
    df_eda   = pd.read_csv(csv_path, parse_dates=['DATETIME'], index_col='DATETIME')
    pkl_path = os.path.join(BASE_DIR, '..', 'Models', 'scaler.pkl')
    scaler   = joblib.load(pkl_path)
    pkl_path = os.path.join(BASE_DIR, '..', 'Models', 'selector.pkl')
    selector = joblib.load(pkl_path)

    # --- Ensure all code columns exist exactly as during training ---
    # Encode wind direction
    df_eda['WD_code']      = df_eda['WD'].astype('category').cat.codes
    # Encode station
    df_eda['STATION_code'] = df_eda['STATION'].astype('category').cat.codes
    # Encode seasons
    df_eda['SEASONS_code'] = df_eda['SEASONS'].astype('category').cat.codes
    # Encode AQI category
    df_eda['AQI_Category_code'] = df_eda['AQI_Category'].astype('category').cat.codes

    # Grab the exact list of features seen by the scaler
    full_cols = list(scaler.feature_names_in_)

    # Fixed input features (drop 'AQI_Category_code')
    input_feats = [
        'PM2.5','PM10','SO2','NO2','CO',
        'O3','DEWP','WSPM','Vehicular_Pollution'
    ]

    # 4-A) Model selection
    model_choice = st.selectbox("Model", perf.index.tolist())
    model = joblib.load(os.path.join(BASE_DIR, '..', 'Models',f"{model_choice}_best.pkl"))

    st.markdown(f"**Enter values for:** {', '.join(input_feats)}")

    # 4-B) Build the input form
    with st.form("predict_form"):
        user_vals = {}
        for feat in input_feats:
            mn, mx, md = df_eda[feat].min(), df_eda[feat].max(), df_eda[feat].median()
            user_vals[feat] = st.number_input(
                label=feat.replace('_',' ').title(),
                min_value=float(mn),
                max_value=float(mx),
                value=float(md)
            )
        submitted = st.form_submit_button("Predict")

       # 4-D) On submit, assemble & predict
    if submitted:
        # 1) Build a one-row DataFrame matching scaler.feature_names_in_
        template = pd.DataFrame(
            {c: [df_eda[c].median()] for c in full_cols},
            columns=full_cols
        )

        # 2) Overwrite pollutant entries with user input
        for k, v in user_vals.items():
            template[k] = v

        # 3) Scale → select → predict
        Xs   = scaler.transform(template)
        Xsel = selector.transform(Xs)
        ypred = model.predict(Xsel)[0]
        r2    = perf.at[model_choice, 'R2']

        # 4) Map predicted AQI to its category
        category_bins   = [0, 50, 100, 150, 200, 300, 500]
        category_labels = [
            'Good',
            'Moderate',
            'Unhealthy for Sensitive Groups',
            'Unhealthy',
            'Very Unhealthy',
            'Hazardous'
        ]
        aqi_cat = pd.cut(
            [ypred],
            bins=category_bins,
            labels=category_labels,
            right=True,
            include_lowest=True
        )[0]

        # 5) Display both AQI and category
        st.success(
            f"🌟 Predicted AQI: {ypred:.1f}  |  Model R² = {r2:.3f}\n\n"
            f"🔖 Category: **{aqi_cat}**"
        )
