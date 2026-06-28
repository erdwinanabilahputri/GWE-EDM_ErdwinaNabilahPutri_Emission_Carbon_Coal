import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Carbon Emission Forecasting",
    page_icon="🌍",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    return pd.read_csv("emissions_high_granularity.csv")

df = load_data()

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("model.pkl")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/427/427735.png",
    width=90
)

st.sidebar.title("Carbon Emission")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Dashboard",
        "🔮 Prediction",
        "📈 Model Performance",
        "ℹ About"
    ]
)

# ==========================================
# HOME
# ==========================================

if menu=="🏠 Home":

    st.title("🌍 Carbon Emission Forecasting System")

    st.markdown("""
Sistem ini dibangun untuk memprediksi **Total Carbon Emission (MtCO₂e)**
menggunakan algoritma **Random Forest Regression**.

Dataset berasal dari Carbon Majors Dataset.
    """)

    c1,c2,c3,c4=st.columns(4)

    c1.metric(
        "Jumlah Data",
        len(df)
    )

    c2.metric(
        "Periode",
        f"{df['year'].min()} - {df['year'].max()}"
    )

    c3.metric(
        "Commodity",
        df["commodity"].nunique()
    )

    c4.metric(
        "Company",
        df["reporting_entity"].nunique()
    )

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

# ==========================================
# DASHBOARD
# ==========================================

elif menu == "📊 Dashboard":

    st.title("📊 Dashboard Analisis Emisi Karbon")

    st.markdown("Visualisasi eksplorasi data Carbon Emission.")

    # =============================
    # FILTER
    # =============================

    tahun = st.slider(
        "Pilih Rentang Tahun",
        int(df["year"].min()),
        int(df["year"].max()),
        (
            int(df["year"].min()),
            int(df["year"].max())
        )
    )

    df_filter = df[
        (df["year"] >= tahun[0]) &
        (df["year"] <= tahun[1])
    ]

    st.divider()

    # =============================
    # METRIC
    # =============================

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Total Emission",
        f"{df_filter['total_emissions_MtCO2e'].sum():,.0f}"
    )

    c2.metric(
        "Average Emission",
        f"{df_filter['total_emissions_MtCO2e'].mean():.2f}"
    )

    c3.metric(
        "Average Production",
        f"{df_filter['production_value'].mean():.2f}"
    )

    st.divider()

    # =============================
    # HISTOGRAM
    # =============================

    fig = px.histogram(
        df_filter,
        x="total_emissions_MtCO2e",
        nbins=40,
        title="Distribusi Total Carbon Emission"
    )

    st.plotly_chart(fig,use_container_width=True)

    # =============================
    # SCATTER
    # =============================

    fig2 = px.scatter(
        df_filter,
        x="production_value",
        y="total_emissions_MtCO2e",
        color="commodity",
        hover_data=["reporting_entity"],
        title="Production Value vs Total Emission"
    )

    st.plotly_chart(fig2,use_container_width=True)

    # =============================
    # TOP COMMODITY
    # =============================

    commodity = (
        df_filter
        .groupby("commodity")["total_emissions_MtCO2e"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        commodity,
        x="commodity",
        y="total_emissions_MtCO2e",
        title="Top 10 Commodity Penyumbang Emisi"
    )

    st.plotly_chart(fig3,use_container_width=True)

    # =============================
    # EMISSION BY YEAR
    # =============================

    yearly = (
        df_filter
        .groupby("year")["total_emissions_MtCO2e"]
        .sum()
        .reset_index()
    )

    fig4 = px.line(
        yearly,
        x="year",
        y="total_emissions_MtCO2e",
        markers=True,
        title="Tren Emisi Karbon per Tahun"
    )

    st.plotly_chart(fig4,use_container_width=True)

    # ==========================================
# PREDICTION
# ==========================================

elif menu == "🔮 Prediction":

    st.title("🔮 Carbon Emission Prediction")

    st.write(
        "Masukkan informasi perusahaan untuk memprediksi Total Carbon Emission."
    )

    st.divider()

    col1,col2 = st.columns(2)

    with col1:

        year = st.number_input(
            "Year",
            min_value=int(df["year"].min()),
            max_value=int(df["year"].max()),
            value=2022
        )

        production_value = st.number_input(
            "Production Value",
            min_value=0.0,
            value=100.0
        )

        commodity = st.selectbox(
            "Commodity",
            sorted(df["commodity"].unique())
        )

        production_unit = st.selectbox(
            "Production Unit",
            sorted(df["production_unit"].unique())
        )

    with col2:

        parent_entity = st.selectbox(
            "Parent Entity",
            sorted(df["parent_entity"].unique())
        )

        parent_type = st.selectbox(
            "Parent Type",
            sorted(df["parent_type"].unique())
        )

        reporting_entity = st.selectbox(
            "Reporting Entity",
            sorted(df["reporting_entity"].unique())
        )

    st.divider()

    if st.button("Predict Emission"):

        # ================================
        # Convert category menjadi angka
        # ================================

        pe = df[df["parent_entity"]==parent_entity].index[0]
        pt = df[df["parent_type"]==parent_type].index[0]
        re = df[df["reporting_entity"]==reporting_entity].index[0]
        co = df[df["commodity"]==commodity].index[0]
        pu = df[df["production_unit"]==production_unit].index[0]

        input_data = pd.DataFrame({

            "year":[year],
            "parent_entity":[pe],
            "parent_type":[pt],
            "reporting_entity":[re],
            "commodity":[co],
            "production_value":[production_value],
            "production_unit":[pu]

        })

        prediction = model.predict(input_data)[0]

        st.success("Prediction Success")

        st.metric(

            "Estimated Total Carbon Emission",

            f"{prediction:.2f} MtCO₂e"

        )

        prediction = model.predict(input_data)[0]

        st.success("Prediction Success ✅")

        st.metric(
            "Estimated Total Carbon Emission",
            f"{prediction:.2f} MtCO₂e"
        )

        # ==========================
        # Emission Category
        # ==========================

        if prediction < 100:

            st.success("🟢 Low Emission")

        elif prediction < 500:

            st.warning("🟡 Medium Emission")

        else:

            st.error("🔴 High Emission")
# ==========================================
# MODEL PERFORMANCE
# ==========================================

elif menu == "📈 Model Performance":

    st.title("📈 Machine Learning Performance")

    st.write("Perbandingan performa seluruh model Machine Learning yang telah diuji.")

    # ===============================
    # BEST MODEL
    # ===============================

    st.subheader("🏆 Best Model")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("MAE", "2.27")
    c2.metric("MSE", "104.40")
    c3.metric("RMSE", "10.22")
    c4.metric("R² Score", "0.998")

    st.divider()

    # ===============================
    # TABLE
    # ===============================

    performance = pd.DataFrame({

        "Model":[
            "Linear Regression",
            "Decision Tree",
            "Random Forest",
            "Random Forest (Tuned)",
            "Random Forest (Feature Engineering)"
        ],

        "MAE":[
            105.68,
            48.95,
            41.57,
            39.99,
            2.27
        ],

        "MSE":[
            107041.37,
            100912.36,
            81914.27,
            60735.51,
            104.40
        ],

        "RMSE":[
            327.17,
            317.67,
            286.21,
            246.45,
            10.22
        ],

        "R²":[
            0.172,
            0.219,
            0.366,
            0.530,
            0.998
        ]

    })

    st.subheader("📋 Performance Table")

    st.dataframe(
        performance,
        use_container_width=True
    )

    st.divider()

    # ===============================
    # BAR CHART
    # ===============================

    st.subheader("📊 R² Comparison")

    fig_bar = px.bar(

        performance,

        x="Model",

        y="R²",

        color="R²",

        text="R²",

        color_continuous_scale="Viridis"

    )

    fig_bar.update_traces(

        texttemplate="%{text:.3f}",

        textposition="outside"

    )

    fig_bar.update_layout(

        yaxis_range=[0,1.05],

        xaxis_title="Model",

        yaxis_title="R² Score"

    )

    st.plotly_chart(

        fig_bar,

        use_container_width=True,

        key="bar_chart"

    )

    st.divider()

    # ===============================
    # RADAR CHART
    # ===============================

    st.subheader("🕸️ Radar Chart")

    fig_radar = px.line_polar(

        performance,

        r="R²",

        theta="Model",

        line_close=True

    )

    fig_radar.update_traces(

        fill="toself"

    )

    st.plotly_chart(

        fig_radar,

        use_container_width=True,

        key="radar_chart"

    )

    st.divider()

    st.success("""

🏆 Best Model

Random Forest (Feature Engineering)

MAE  : 2.27

MSE  : 104.40

RMSE : 10.22

R² Score : 0.998

""")
    
# ==========================================
# ABOUT
# ==========================================

elif menu=="ℹ About":

    st.title("ℹ About Project")

    st.markdown("""

# 🌍 Carbon Emission Forecasting

Project ini bertujuan membangun model Machine Learning
untuk memprediksi **Total Carbon Emission (MtCO₂e)**
berdasarkan karakteristik produksi bahan bakar fosil.

---

## 📂 Dataset

**Carbon Majors Dataset**

- Jumlah Data : **15.797 records**
- Periode : **1854 - 2022**
- Target : **Total Emissions (MtCO₂e)**

---

## 🤖 Algoritma yang Digunakan

- Linear Regression
- Decision Tree Regression
- Random Forest Regression
- Random Forest + Hyperparameter Tuning
- Random Forest + Feature Engineering

---

## 🏆 Model Terbaik

**Random Forest Regression**
(dengan Feature Engineering)

**Performance**

- MAE : **2.27**
- MSE : **104.40**
- RMSE : **10.22**
- R² Score : **0.998**

---

## 👩‍💻 Developer

**Erdwina Nabilah Putri**


""")