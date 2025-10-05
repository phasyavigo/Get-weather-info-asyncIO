import requests
from bs4 import BeautifulSoup
import json

# URL halaman Wikipedia yang ingin di-scrape
url = 'https://id.wikipedia.org/wiki/Daftar_kecamatan_dan_kelurahan_di_Jawa_Tengah'

# Menambahkan header User-Agent untuk meniru browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Mengambil halaman HTML dengan header User-Agent
response = requests.get(url, headers=headers)

# Cek apakah permintaan berhasil
if response.status_code != 200:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
else:
    print("Page successfully retrieved!")

# Parsing HTML menggunakan BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Menyaring tabel yang berisi daftar kecamatan dan kelurahan
tables = soup.find_all('table', {'class': 'wikitable'})

# Cek apakah tabel ditemukan
if not tables:
    print("No tables found.")
else:
    print(f"Found {len(tables)} tables.")

# Daftar untuk menyimpan data kecamatan dan kelurahan
data = {}

# Menyaring data dari tabel
for table in tables:
    rows = table.find_all('tr')[1:]  # Melewatkan header tabel
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 1:
            # Nama kabupaten/kota
            kabupaten_kota = columns[0].text.strip()
            # Nama kecamatan
            kecamatan = columns[1].text.strip()
            
            # Jika kabupaten/kota belum ada dalam dictionary, tambahkan
            if kabupaten_kota not in data:
                data[kabupaten_kota] = []
            
            # Menambahkan kecamatan ke daftar kabupaten/kota
            data[kabupaten_kota].append(kecamatan)

# Menyimpan data dalam format JSON
with open('kecamatan_jawa_tengah.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Cetak hasil akhir
if data:
    print(f"Data berhasil disimpan dalam format JSON dengan {len(data)} kabupaten/kota.")
else:
    print("Tidak ada data yang ditemukan.")
