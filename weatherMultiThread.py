# ANGGOTA KELOMPOK
# Phasya Vigo Khalil Nugroho    - 235150300111004
# Muhammad Rafie Habibi Fauzi   - 235150307111011
# Daffa Fawwaz Garibaldi        - 235150301111009

import threading
import time
from queue import Queue
import requests
from requests.adapters import HTTPAdapter, Retry
import pandas as pd
import re

# ================== KONFIG ==================
API_KEY = "98f93bb4ed854681ad9170804251909"
INPUT_XLSX = "kecamatan_jawa_tengah_clean_full.xlsx"
SHEET_NAME = 0                
KOLom_NAMA = "Kecamatan"      
MAX_CONCURRENT = 20           
TIMEOUT = 10                  
OUTPUT_XLSX = "kecamatan_jawa_tengah_REKAP_threading.xlsx"
# ============================================

# --- Session HTTP dengan retry ringan ---
session = requests.Session()
retries = Retry(
    total=3, backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

sem = threading.BoundedSemaphore(MAX_CONCURRENT)
results_q = Queue()
print_lock = threading.Lock()

def bersihkan_nama(n):
    s = str(n).strip()
    s = s.split(";")[0].strip()
    s = re.sub(r"\s+", " ", s)
    return s

def get_weather_json(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    try:
        response = session.get(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        with print_lock:
            print(f"[ERR] {city}: {e}")
        return None

    if response.status_code != 200:
        with print_lock:
            print(f"[HTTP {response.status_code}] {city}")
        return None

    data = response.json()
    if "current" not in data or "location" not in data:
        with print_lock:
            print(f"[NO DATA] {city}")
        return None

    # pastikan region = Central Java
    if data["location"].get("region") != "Central Java":
        with print_lock:
            print(f"[SKIP] {city} bukan di Central Java (region: {data['location'].get('region')})")
        return None

    return data

def extract_record(city, data):
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

def worker(city):
    with sem:
        data = get_weather_json(city)
        if data:
            results_q.put(extract_record(city, data))

def main():
    start = time.time()


    df = pd.read_excel(INPUT_XLSX, sheet_name=SHEET_NAME)
    if KOLom_NAMA not in df.columns:
        raise ValueError(f"Kolom '{KOLom_NAMA}' tidak ditemukan di file {INPUT_XLSX}.")

    cities = [bersihkan_nama(x) for x in df[KOLom_NAMA].dropna().tolist()]
    seen = set()
    cities = [c for c in cities if not (c in seen or seen.add(c))]

    threads = []
    for city in cities:
        t = threading.Thread(target=worker, args=(city,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    results = []
    while not results_q.empty():
        results.append(results_q.get())

    
    cols = [
        "Kecamatan", "Last Update", "Temperature (°C)", "Humidity (%)",
        "Condition", "Wind Speed (km/h)", "Wind Direction", "UV Index"
    ]
    out = pd.DataFrame(results)
    if not out.empty:
        out = out[cols]
        out = out.sort_values("Kecamatan").reset_index(drop=True)

    out.to_excel(OUTPUT_XLSX, index=False)
    dur = time.time() - start
    print(f"Selesai. {len(out)} baris ditulis ke {OUTPUT_XLSX}. Waktu: {dur:.2f} dtk")

if __name__ == "__main__":
    main()
