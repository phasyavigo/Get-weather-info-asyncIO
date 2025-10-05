Project 1 - Komputasi Paralel
====Get weather info with Multi Threading====

Kelompok :
	Phasya Vigo Khalil Nugroho    - 235150300111004
	Muhammad Rafie Habibi Fauzi   - 235150307111011
	Daffa Fawwaz Garibaldi        - 235150301111009

Requirements :
 - pip install request
 - pip install pandas

-----ALUR PROGRAM weatherMultiThread.py-----
Program akan membaca file excel "kecamatan_jawa_tengah_clean_full.xlsx" untuk mendapatkan lokasi yang "berpotensi" di Jawa Tengah. Semua nama kecamatan yang ada di "kecamatan_jawa_tengah_clean_full.xlsx" akan difilter belum tentu lokasi berada di Jawa Tengah dan merupakan lokasi valid di request JSON weatherapi.com. Yang ada di "kecamatan_jawa_tengah_REKAP_threading.xlsx" merupakan data informasi cuaca kecamatan yang final.