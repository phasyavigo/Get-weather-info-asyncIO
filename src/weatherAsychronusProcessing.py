import asyncio
import aiohttp
import pandas as pd
import time
import re
import json

# ================== KONFIGURASI ==================
# Pastikan file excel input berada di folder yang sama dengan script ini
with open('secrets.json') as f:
    API_KEY = json.load(f)["API_KEY"]
    f.close()
INPUT_XLSX = "kecamatan_jawa_tengah_clean_full.xlsx"
SHEET_NAME = 0                
KOLOM_NAMA = "Kecamatan"      
MAX_CONCURRENT = 18           
TIMEOUT = 10                  
OUTPUT_XLSX = "kecamatan_jawa_tengah_REKAP_asyncio.xlsx"
# ================================================

def bersihkan_nama(n):
    """Membersihkan nama kecamatan dari karakter aneh/spasi berlebih."""
    s = str(n).strip()
    s = s.split(";")[0].strip()
    s = re.sub(r"\s+", " ", s)
    return s

async def fetch_weather(session, city):
    """Fungsi asynchronous untuk mengambil data dari API."""
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    
    try:
        async with session.get(url, timeout=TIMEOUT) as response:
            if response.status != 200:
                print(f"[HTTP {response.status}] Gagal mengambil data untuk: {city}")
                return None
            
            data = await response.json()
            
            # Validasi data
            if "current" not in data or "location" not in data or data["location"]["country"] != "Indonesia":
                return None

            if data["location"]["region"] != "Central Java":
                # print(f"[WARNING] {city} bukan di Jawa Tengah.")
                return None

            c = data["current"]
            return {
                "Kecamatan": city,
                "Last Update": c.get("last_updated"),
                "Temperature (°C)": c.get("temp_c"),
                "Humidity (%)": c.get("humidity"),
                "Condition": c.get("condition", {}).get("text"),
                "Wind Speed (km/h)": c.get("wind_kph"),
                "Wind Direction": c.get("wind_dir"),
                "UV Index": c.get("uv"),
            }

    except Exception as e:
        print(f"[ERROR] {city}: {str(e)}")
        return None

async def worker(sem, session, city):
    """Worker yang dibatasi oleh Semaphore untuk mengontrol concurrency."""
    async with sem:
        return await fetch_weather(session, city)

async def main():
    start_time = time.time()
    print("Membaca file Excel...")
    
    # 1. Baca Excel
    try:
        df = pd.read_excel(INPUT_XLSX, sheet_name=SHEET_NAME)
    except FileNotFoundError:
        print(f"File {INPUT_XLSX} tidak ditemukan!")
        return

    if KOLOM_NAMA not in df.columns:
        raise ValueError(f"Kolom '{KOLOM_NAMA}' tidak ditemukan di file Excel.")

    # 2. Bersihkan daftar kota/kecamatan
    cities_raw = df[KOLOM_NAMA].dropna().tolist()
    cities = []
    seen = set()
    # Hapus duplikat dan bersihkan nama
    for c in cities_raw:
        clean_c = bersihkan_nama(c)
        if clean_c not in seen:
            seen.add(clean_c)
            cities.append(clean_c)

    print(f"Memulai proses pengambilan data untuk {len(cities)} kecamatan...")
    print(f"Menggunakan Asyncio dengan Max Concurrent: {MAX_CONCURRENT}")

    # 3. Setup Asyncio Loop
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async with aiohttp.ClientSession() as session:
        tasks = [worker(sem, session, city) for city in cities]
        results = await asyncio.gather(*tasks)

    # 4. Filter hasil yang None (gagal request)
    valid_results = [r for r in results if r is not None]

    # 5. Simpan ke Excel
    if valid_results:
        df_hasil = pd.DataFrame(valid_results)
        
        cols_order = [
            "Kecamatan", "Last Update", "Temperature (°C)", "Humidity (%)",
            "Condition", "Wind Speed (km/h)", "Wind Direction", "UV Index"
        ]
        # Pastikan kolom ada
        df_final = df_hasil[cols_order]
        
        df_final.to_excel(OUTPUT_XLSX, index=False)
        print(f"\nSukses! Data berhasil disimpan ke: {OUTPUT_XLSX}")
        print(f"Total Data Berhasil: {len(valid_results)}/{len(cities)}")
    else:
        print("\nTidak ada data yang berhasil diambil.")

    duration = time.time() - start_time
    print(f"Waktu Eksekusi: {duration:.2f} detik")

if __name__ == "__main__":
    # Menjalankan event loop
    asyncio.run(main())