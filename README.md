# 🌦️ Weather Info - Asynchronous Processing

Aplikasi untuk mengambil data cuaca kecamatan di Jawa Tengah menggunakan asynchronous processing dengan Python dan menampilkannya melalui dashboard Streamlit.

## 📋 Deskripsi

Project ini menggunakan asyncio dan aiohttp untuk melakukan fetching data cuaca secara asynchronous dari WeatherAPI untuk seluruh kecamatan di Jawa Tengah. Hasilnya disimpan dalam file Excel dan dapat divisualisasikan melalui dashboard Streamlit yang interaktif.

## 🚀 Fitur

- ⚡ **Asynchronous Processing**: Mengambil data cuaca untuk ratusan kecamatan secara paralel
- 📊 **Export ke Excel**: Hasil disimpan dalam format Excel yang mudah dianalisis
- 📱 **Dashboard Interaktif**: Visualisasi data menggunakan Streamlit
- 🎯 **Concurrent Control**: Kontrol jumlah request bersamaan untuk menghindari rate limiting
- 🔄 **Data Cleaning**: Pembersihan otomatis nama kecamatan dan validasi data

## 📁 Struktur Project

```
.
├── data/                          # Folder untuk file Excel
│   ├── kecamatan_jawa_tengah_clean_full.xlsx
│   └── kecamatan_jawa_tengah_REKAP_asyncio.xlsx
├── src/                           # Source code Python
│   ├── cobawebskrep.py           # Script untuk web scraping (opsional)
│   ├── weatherAsychronusProcessing.py  # Main script untuk fetch cuaca
│   └── dashboard.py              # Streamlit dashboard
├── .gitignore
├── requirements.txt
├── secrets.json                  # API Key (tidak di-commit)
└── README.md
```

## 🛠️ Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd "Get weather info with Asynchronus Processing"
```

### 2. Buat Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup API Key

Buat file `secrets.json` di root folder dengan format:

```json
{
  "API_KEY": "YOUR_WEATHERAPI_KEY_HERE"
}
```

> 💡 **Dapatkan API Key gratis** di [WeatherAPI.com](https://www.weatherapi.com/)

## 🎯 Cara Penggunaan

### Step 1: Persiapan Data (Opsional)

Jika belum ada file Excel kecamatan:

```bash
python src/cobawebskrep.py
```

Output: `data/kecamatan_jawa_tengah_clean_full.xlsx`

### Step 2: Fetch Data Cuaca

Jalankan script utama untuk mengambil data cuaca:

```bash
python src/weatherAsychronusProcessing.py
```

**Konfigurasi yang dapat disesuaikan** (di dalam script):
- `MAX_CONCURRENT`: Jumlah request bersamaan (default: 18)
- `TIMEOUT`: Timeout per request dalam detik (default: 10)
- `INPUT_XLSX`: Path ke file Excel input
- `OUTPUT_XLSX`: Path untuk file Excel output

Output: `data/kecamatan_jawa_tengah_REKAP_asyncio.xlsx`

### Step 3: Jalankan Dashboard

```bash
streamlit run src/dashboard.py
```

Dashboard akan terbuka otomatis di browser (biasanya `http://localhost:8501`)

## 📊 Data Output

File Excel hasil akan berisi kolom:
- **Kecamatan**: Nama kecamatan
- **Last Update**: Waktu update terakhir
- **Temperature (°C)**: Suhu dalam Celsius
- **Humidity (%)**: Kelembaban udara
- **Condition**: Kondisi cuaca (Sunny, Cloudy, Rain, dll)
- **Wind Speed (km/h)**: Kecepatan angin
- **Wind Direction**: Arah angin
- **UV Index**: Indeks UV

## ⚙️ Dependencies

- **aiohttp**: HTTP client asynchronous
- **pandas**: Manipulasi dan analisis data
- **requests**: HTTP requests
- **beautifulsoup4**: Web scraping
- **openpyxl**: Baca/tulis Excel
- **streamlit**: Dashboard interaktif
- **lxml**: Parser XML/HTML

## 🔧 Troubleshooting

### Error: File tidak ditemukan

Pastikan file Excel input ada di folder `data/`:
```bash
ls data/
```

### Error: API Key invalid

Periksa file `secrets.json` dan pastikan API key valid

### Error: ModuleNotFoundError

Install ulang dependencies:
```bash
pip install -r requirements.txt
```

### Terlalu banyak timeout

Kurangi `MAX_CONCURRENT` di script:
```python
MAX_CONCURRENT = 10  # Kurangi dari 18 menjadi 10
```

## 📝 Catatan

- ⚠️ **Rate Limiting**: Free tier WeatherAPI memiliki limit request. Atur `MAX_CONCURRENT` sesuai kebutuhan
- 🔒 **Jangan commit** file `secrets.json` ke repository (sudah ada di `.gitignore`)
- 📹 **File video** (`.mp4`) tidak di-commit ke repository
- ⏱️ **Waktu eksekusi**: Tergantung jumlah kecamatan dan kecepatan internet (biasanya 1-3 menit untuk ~500 kecamatan)

## 📄 License

Project ini dibuat untuk keperluan pembelajaran dan riset.

## 👨‍💻 Author

Dibuat sebagai bagian dari Kerja Praktik (KP) - Semester 5

---

⭐ Jika project ini membantu, jangan lupa kasih star!
