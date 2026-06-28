# 🌍 Prediksi Emisi Karbon Menggunakan Machine Learning

## Deskripsi Proyek

Pada proyek ini saya mengembangkan sebuah **aplikasi web berbasis Machine Learning** yang digunakan untuk memprediksi **Total Emisi Karbon (MtCO₂e)** berdasarkan data historis perusahaan produsen bahan bakar fosil. Aplikasi ini dibangun menggunakan **Streamlit** sehingga pengguna dapat melakukan prediksi secara interaktif melalui browser.

Untuk melakukan prediksi, pengguna diminta mengisi beberapa informasi, yaitu:

- Tahun (Year)
- Parent Entity
- Parent Type
- Reporting Entity
- Commodity
- Production Value
- Production Unit

Berdasarkan data tersebut, sistem akan menghasilkan **prediksi Total Emisi Karbon (MtCO₂e)** serta memberikan kategori tingkat emisi, yaitu **Low Emission**, **Medium Emission**, atau **High Emission**.

Aplikasi ini bertujuan untuk membantu memahami hubungan antara aktivitas produksi dengan emisi karbon, membandingkan performa beberapa algoritma Machine Learning, serta memberikan gambaran awal mengenai besarnya emisi karbon yang mungkin dihasilkan berdasarkan karakteristik produksi.

## Dataset

Dataset yang digunakan adalah **Carbon Majors Dataset** yang diperoleh dari **Kaggle**. Dataset ini berisi informasi mengenai produksi bahan bakar fosil, perusahaan pelapor, serta data emisi karbon dari tahun **1854 hingga 2022**.

---

## Teknologi yang Digunakan

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Joblib

---

## Model Machine Learning

Model yang digunakan dan dibandingkan pada proyek ini meliputi:

- Linear Regression
- Decision Tree Regression
- Random Forest Regression
- Random Forest (Hyperparameter Tuning)
- Random Forest (Feature Engineering)

Model terbaik yang digunakan pada aplikasi adalah **Random Forest Regression**.

---

## Fitur Aplikasi

Aplikasi menyediakan beberapa menu, yaitu:

- 🏠 Home
- 📊 Dashboard
- 🔮 Prediction
- 📈 Model Performance
- ℹ About

---

## Pemanfaatan AI

Dalam proses pengembangan proyek ini, **ChatGPT (OpenAI)** digunakan sebagai asisten untuk membantu:

- Penyusunan struktur kode Streamlit.
- Membantu proses debugging.
- Memberikan rekomendasi visualisasi data.
- Membantu penyusunan dokumentasi proyek.

Seluruh proses analisis data, pelatihan model, evaluasi model, dan pengujian dilakukan oleh pengembang.

---

## Struktur Project

```
Carbon_Emission_Project/
│── app.py
│── model.pkl
│── emissions_high_granularity.csv
│── requirements.txt
│── README.md
```

---

## Pengembang

**Erdwina Nabilah Putri**

