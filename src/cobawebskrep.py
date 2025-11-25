import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- KONFIGURASI ---
url = 'https://id.wikipedia.org/wiki/Daftar_kecamatan_dan_kelurahan_di_Jawa_Tengah'
output_filename = 'kecamatan_jawa_tengah_clean_full.xlsx'
headers_request = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Kolom yang diminta untuk file Excel
columns_excel = [
    'Kecamatan', 
    'Last Update (time)', 
    'Suhu Celsius', 
    'Kelembapan', 
    'Kondisi cuaca', 
    'Kecepatan angin', 
    'Arah Angin', 
    'Sinar UV'
]

def main():
    print("1. Mengambil data dari Wikipedia...")
    try:
        response = requests.get(url, headers=headers_request)
        response.raise_for_status() # Cek jika ada error koneksi
    except Exception as e:
        print(f"Gagal mengambil halaman: {e}")
        return

    print("2. Memproses HTML...")
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})

    if not tables:
        print("Tabel tidak ditemukan.")
        return

    # List untuk menampung semua nama kecamatan yang sudah bersih
    all_kecamatan_clean = []

    print(f"   Ditemukan {len(tables)} tabel. Sedang mengekstrak data...")
    
    for table in tables:
        rows = table.find_all('tr')[1:]  # Skip header
        for row in rows:
            cols = row.find_all('td')
            
            # Logika pengambilan kolom sesuai script awalmu:
            # Asumsi: Kolom indeks ke-1 adalah yang berisi nama Kecamatan
            if len(cols) > 1:
                kecamatan_raw_text = cols[1].get_text(separator='\n') # Ambil text, ubah <br> menjadi newline
                
                # Proses cleaning dan splitting (seperti logika script ke-2 kamu)
                # Memisahkan jika ada banyak kecamatan dalam satu sel (dipisah newline)
                parts = [k.strip() for k in kecamatan_raw_text.split('\n') if k.strip()]
                
                # Masukkan ke list utama
                all_kecamatan_clean.extend(parts)

    # Jika tidak ada data
    if not all_kecamatan_clean:
        print("Data kecamatan kosong atau gagal diekstrak.")
        return

    print(f"3. Membuat DataFrame ({len(all_kecamatan_clean)} data kecamatan ditemukan)...")
    
    # Membuat DataFrame menggunakan Pandas
    df = pd.DataFrame(all_kecamatan_clean, columns=['Kecamatan'])

    # Menambahkan kolom-kolom kosong lainnya
    for col in columns_excel:
        if col != 'Kecamatan':
            df[col] = '' # Mengisi dengan string kosong

    # Mengurutkan kolom sesuai urutan yang diminta
    df = df[columns_excel]

    print(f"4. Menyimpan ke file Excel: {output_filename}...")
    try:
        # Export ke Excel tanpa index (nomor baris)
        df.to_excel(output_filename, index=False, engine='openpyxl')
        print("\nSUKSES! File berhasil dibuat.")
    except Exception as e:
        print(f"\nGagal menyimpan file Excel: {e}")

if __name__ == '__main__':
    main()