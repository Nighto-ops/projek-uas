# 🇮🇩 Merajut Benang Merah Kesejahteraan: Dasbor Analisis Ketimpangan Indonesia 2025

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![BPS Data](https://img.shields.io/badge/Data-BPS%202025-0072B2?style=for-the-badge)](https://www.bps.go.id/)
[![STIS](https://img.shields.io/badge/Institution-Politeknik%20Statistika%20STIS-F59E0B?style=for-the-badge)](https://stis.ac.id/)

Dasbor analitis interaktif **"Merajut Benang Merah Kesejahteraan"** menyajikan potret komprehensif mengenai peta ketimpangan sosial-ekonomi dan kondisi kesejahteraan masyarakat di Indonesia berbasis data resmi **Badan Pusat Statistik (BPS) 2025**. Analisis dirancang menggunakan pendekatan *scrollytelling* visualisasi data multi-dimensi: **Multivariat** (38 Provinsi), **Geospasial** (514 Kabupaten/Kota), dan **Hierarki** (Struktur Konsumsi Rumah Tangga).

---

## 📌 Identitas Proyek

- **Mata Kuliah:** Visualisasi Data dan Informasi
- **Institusi:** Politeknik Statistika STIS
- **Penyusun:** Rahman Al Gifary (NIM: 222313328)
- **Tahun Akademik:** 2025/2026
- **Repositori GitHub:** [Nighto-ops/projek-uas](https://github.com/Nighto-ops/projek-uas)

---

## 🚀 Fitur Utama & Visualisasi Multi-Dimensi

### 1. 📊 Dimensi Multivariat (Karakteristik 38 Provinsi)
- **Reduksi Dimensi (PCA Scatter Plot):** Menyederhanakan 8 indikator utama BPS (IPM, Persentase Kemiskinan, TPT, RLS, Gini Ratio, PDRB per Kapita, Pengeluaran per Kapita, dan Angka Harapan Hidup) menjadi 2 Komponen Utama untuk memetakan kedudukan 38 provinsi.
- **Klastering K-Means:** Pengelompokan otomatis provinsi ke dalam 3 Klaster Kesejahteraan (*Kesejahteraan Tinggi*, *Kesejahteraan Menengah*, dan *Tantangan Pembangunan*).
- **Parallel Coordinates Plot:** Menguraikan profil 8 indikator secara simultan dengan interaksi *brushing* dan filter klaster terintegrasi (*Brushing & Linking*).

### 2. 🗺️ Dimensi Geospasial (Kantong Kemiskinan 514 Kab/Kota)
- **Peta Interaktif Folium Terfokus:** Peta khusus wilayah Indonesia tanpa gangguan peta dasar laut/negara lain (*clean dark slate canvas*).
- **Layer Choropleth:** Visualisasi rasio persentase penduduk miskin (%) dengan warna *colorblind-friendly* (`YlOrRd`).
- **Layer Simbol Proporsional:** Lingkaran proporsional untuk memvisualisasikan beban akumulasi jumlah penduduk miskin absolut (ribu jiwa).
- **Fitur Interaktif:** Sticky tooltip rincian wilayah, *zoom/pan*, serta *Layer Control toggle*.

### 3. 🌳 Dimensi Hierarki (Ironi Konsumsi Rumah Tangga)
- **Struktur Pengeluaran per Kapita:** Menguraikan rata-rata pengeluaran bulanan (Rp/Bulan) untuk komoditas **Makanan** dan **Bukan Makanan**.
- **Mode Visualisasi Ganda:** Pengguna dapat beralih antara tampilan **Treemap (Kotak)** dan **Sunburst Chart (Lingkaran)** secara dinamis.
- **Temuan Utama:** Mengungkap porsi pengeluaran **Rokok & Tembakau** yang sangat tinggi pada kelompok makanan, bahkan melampaui komoditas gizi esensial (daging dan telur).

### 4. 📚 Metadata, Metodologi & Fitur Unduh Data
- **Transparansi Metodologi:** Dokumentasi pembersihan data, harmonisasi kode wilayah (`kodekab`), standarisasi *StandardScaler*, algoritma clustering, serta penyederhanaan geometri spasial *Douglas-Peucker*.
- **Kamus Data & Definisi Resmi:** Penjelasan rinci satuan dan definisi operasional indikator BPS.
- **Unduh Dataset (CSV):** Tombol unduh data CSV langsung untuk setiap dimensi analisis.

---

## 🛠️ Teknologi & Dependensi

Proyek ini dibangun menggunakan *stack* statistik & visualisasi Python modern:

| Kategori | Perpustakaan / Alat | Fungsi Utama |
|---|---|---|
| **Framework UI** | `streamlit` | Kerangka aplikasi web interaktif |
| **Data Wrangling** | `pandas`, `numpy` | Pengolahan, agregasi, dan manipulasi data |
| **Geospatial Analysis** | `geopandas`, `folium`, `streamlit-folium` | Pemrosesan Shapefile (.shp) & render peta interaktif |
| **Machine Learning** | `scikit-learn` | *StandardScaler*, *PCA*, dan *KMeans Clustering* |
| **Visualisasi Data** | `plotly` | Grafik interaktif (Scatter, Parcoords, Treemap, Sunburst) |

---

## 📁 Struktur Direktori Proyek

```text
projek-uas/
├── .streamlit/
│   └── config.toml          # Konfigurasi tema dark mode Streamlit
├── data/
│   ├── Administrasi_Kabupaten.shp / .dbf / .shx / .prj  # Geometri Shapefile BPS/BIG
│   ├── Dataset_Geospasial_Kemiskinan_Final.csv           # Data Kemiskinan 514 Kab/Kota
│   ├── Dataset_Hierarki_Pengeluaran.csv                 # Data Struktur Pengeluaran Susenas
│   └── Dataset_Multivariat_Final_Complete.csv           # Indikator 38 Provinsi 2025
├── app.py                   # Berkas utama aplikasi Streamlit
├── logo.png                 # Logo instansi & favicon web
├── requirements.txt         # Daftar dependensi Python
└── README.md                # Dokumentasi proyek
```

---

## ⚡ Panduan Instalasi & Melakukan Running

### 1. Prasyarat System
Pastikan Anda telah menginstal **Python 3.9** atau versi yang lebih baru di perangkat Anda.

### 2. Kloning Repositori
```bash
git clone https://github.com/Nighto-ops/projek-uas.git
cd projek-uas
```

### 3. Buat & Aktifkan Lingkungan Virtual (Virtual Environment)
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Instal Dependensi
```bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi Streamlit
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser lokal Anda pada alamat `http://localhost:8501`.

---

## 📈 Sumber Data Resmi

1. **Badan Pusat Statistik (BPS) 2025:** Indikator Sosial Ekonomi Provinsi, Persentase & Jumlah Penduduk Miskin Kabupaten/Kota, serta Survei Sosial Ekonomi Nasional (Susenas) Pengeluaran Rumah Tangga.
2. **Badan Informasi Geospasial (BIG) / BPS:** Peta Geometri Administrasi Kabupaten/Kota Indonesia.

---

## 📄 Lisensi & Hak Cipta

Proyek ini dikembangkan untuk kepentingan akademik dan penelitian dalam mata kuliah **Visualisasi Data dan Informasi** di **Politeknik Statistika STIS**. Seluruh data yang digunakan bersumber dari publikasi resmi BPS.

© 2026 **Rahman Al Gifary** — Politeknik Statistika STIS.
