import json
import csv

# Membaca data dari file JSON
with open('kecamatan_jawa_tengah.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Menyimpan data dalam format CSV dengan pemisah titik koma
with open('kecamatan_jawa_tengah.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')  # Menetapkan delimiter menjadi titik koma
    
    # Menulis header sesuai format yang diminta
    writer.writerow(['Kecamatan', 'Last Update (time)', 'Suhu Celsius', 'Kelembapan', 'Kondisi cuaca', 'Kecepatan angin', 'Arah Angin', 'Sinar UV'])
    
    # Menyaring dan menulis data kecamatan (Kolom lainnya dibiarkan kosong)
    for kabupaten_kota, kecamatan_list in data.items():
        for kecamatan in kecamatan_list:
            # Memisahkan kecamatan jika ada lebih dari satu nama kecamatan di dalam satu sel
            kecamatan_split = [k.strip() for k in kecamatan.split('\n') if k.strip()]
            
            # Menulis setiap kecamatan ke dalam baris terpisah di CSV
            for k in kecamatan_split:
                writer.writerow([k] + [''] * 7)  # Menambahkan kolom kosong (7 kolom) setelah nama kecamatan

print("Data berhasil disimpan dalam format CSV.")
