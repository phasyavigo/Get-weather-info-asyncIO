import streamlit as st
import pandas as pd

# Konfigurasi Halaman Website
st.set_page_config(page_title="Dashboard Cuaca Jawa Tengah", layout="wide")

# Judul
st.title("🌤️ Dashboard Monitoring Cuaca Jawa Tengah")
st.markdown("Data diambil menggunakan **AsyncIO** dari WeatherAPI")

# Load Data Excel Hasil Output Script Asyncio Kamu
FILE_EXCEL = "kecamatan_jawa_tengah_REKAP_asyncio.xlsx"

try:
    df = pd.read_excel(FILE_EXCEL)
    
    # --- METRIK RINGKASAN (KOTAK INFO DI ATAS) ---
    col1, col2, col3, col4 = st.columns(4)
    
    avg_temp = df["Temperature (°C)"].mean()
    max_temp = df["Temperature (°C)"].max()
    hottest_city = df.loc[df["Temperature (°C)"].idxmax(), "Kecamatan"]
    avg_humid = df["Humidity (%)"].mean()
    
    col1.metric("Rata-rata Suhu", f"{avg_temp:.1f} °C")
    col2.metric("Suhu Tertinggi", f"{max_temp} °C", f"di {hottest_city}")
    col3.metric("Rata-rata Kelembapan", f"{avg_humid:.1f} %")
    col4.metric("Total Kecamatan", len(df))

    st.divider()

    # --- TABEL DATA INTERAKTIF ---
    st.subheader("📋 Tabel Detail Data Cuaca")
    
    # Fitur canggih Streamlit: Column Config
    # Ini bikin tabelnya punya visual bar dan highlight warna
    st.dataframe(
        df,
        column_config={
            "Temperature (°C)": st.column_config.NumberColumn(
                "Suhu (°C)",
                format="%.1f °C",
            ),
            "Humidity (%)": st.column_config.ProgressColumn(
                "Kelembapan",
                format="%d%%",
                min_value=0,
                max_value=100,
            ),
            "UV Index": st.column_config.NumberColumn(
                "Indeks UV",
                help="Indeks Sinar Ultraviolet",
            ),
             "Wind Speed (km/h)": st.column_config.NumberColumn(
                "Kecepatan Angin",
                format="%.1f km/h",  # Menambahkan satuan km/h di belakang angka
            )
        },
        use_container_width=True,
        hide_index=True,
        height=600 # Tinggi tabel
    )

except FileNotFoundError:
    st.error(f"File '{FILE_EXCEL}' belum ditemukan. Jalankan script asyncio dulu ya!")