import streamlit as st
import pandas as pd
import numpy as np
import re
import os
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# ==========================================
# 1. KONFIGURASI HALAMAN & STYLING CUSTOM
# ==========================================
st.set_page_config(
    page_title="Dasbor Ketimpangan & Kesejahteraan Indonesia 2025",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan Premium Dark Analytics / Intelligence Command Center
st.markdown("""
    <style>
    /* Global Typography & Font Family */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #E2E8F0;
    }
    
    /* Background Container Deep Slate */
    .stApp {
        background-color: #0F172A;
    }
    
    /* Metric Cards Premium Dark Mode */
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 18px 22px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        margin-bottom: 16px;
        transition: all 0.2s ease-in-out;
    }
    
    .metric-card:hover {
        border-left-color: #0EA5E9;
        border-color: #475569;
        box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.3);
    }
    
    /* Metric Card Typography */
    .metric-card h4 {
        margin: 0 0 6px 0;
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card h2 {
        margin: 0;
        color: #F8FAFC;
        font-size: 1.85rem;
        font-weight: 700;
        line-height: 1.2;
    }
    
    /* Header Kop Styling */
    .institution-badge {
        color: #F59E0B;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 0;
    }
    
    .main-header-title {
        color: #F8FAFC;
        font-size: 1.8rem;
        font-weight: 800;
        line-height: 1.25;
        margin: 4px 0 8px 0;
    }
    
    .author-meta-text {
        color: #94A3B8;
        font-size: 0.85rem;
        margin: 0 0 12px 0;
    }
    
    /* Topic Cards */
    .topic-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-top: 4px solid #0EA5E9;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        height: 100%;
    }
    
    .topic-card-title {
        color: #F8FAFC;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 12px;
        border-bottom: 1px solid #334155;
        padding-bottom: 8px;
    }

    .topic-card-item {
        font-size: 0.85rem;
        color: #CBD5E1;
        margin-bottom: 8px;
        line-height: 1.45;
    }
    
    .topic-card-item strong {
        color: #38BDF8;
    }

    /* Info Panels */
    .info-panel {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 20px;
        height: 100%;
    }
    
    .info-panel-header {
        color: #F59E0B;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 14px;
    }

    /* Dark Mode Source Captions */
    .source-caption {
        font-size: 0.8rem;
        color: #64748B;
        font-style: italic;
        margin-top: 8px;
        margin-bottom: 12px;
        display: block;
    }
    
    /* Dark Mode Divider Line */
    hr {
        margin: 2rem 0;
        border: 0;
        border-top: 1px solid #334155;
    }
    
    /* Custom Streamlit Primary Button Styling */
    div.stButton > button[kind="primary"] {
        background-color: #F59E0B !important;
        color: #0F172A !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #D97706 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4) !important;
    }
    
    /* Custom Table Dark Mode Styling */
    .stTable table {
        background-color: #1E293B !important;
        color: #E2E8F0 !important;
        border-collapse: collapse !important;
        border: 1px solid #334155 !important;
    }
    .stTable th {
        background-color: #0F172A !important;
        color: #F59E0B !important;
        border: 1px solid #334155 !important;
    }
    .stTable td {
        border: 1px solid #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HEADER RESMI & TEKS PENGANTAR
# ==========================================
col_logo, col_title = st.columns([1, 4])

with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.image("logo.png")

with col_title:
    st.markdown("""
        <div>
            <p class="institution-badge">   POLITEKNIK STATISTIKA STIS</p>
            <h1 class="main-header-title">Merajut Benang Merah Kesejahteraan: Analisis Ketimpangan di Indonesia 2025</h1>
            <p class="author-meta-text">
                <strong>Disusun oleh:</strong> Rahman Al Gifary &nbsp;|&nbsp; 
                <strong>NIM:</strong> 222313328 &nbsp;|&nbsp; 
                <em>Mata Kuliah Visualisasi Data dan Informasi — Politeknik Statistika STIS</em>
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="background-color: #1E293B; border-left: 4px solid #0EA5E9; border-radius: 6px; padding: 16px 20px; margin: 10px 0 24px 0;">
    <p style="margin: 0; color: #E2E8F0; font-size: 0.95rem; line-height: 1.6;">
        <strong>Selamat Datang di Dasbor Ketimpangan & Kesejahteraan Indonesia 2025!</strong><br>
        Dasbor interaktif ini menyajikan potret komprehensif mengenai kondisi kesejahteraan dan peta ketimpangan sosial-ekonomi di Indonesia berdasarkan data resmi <strong>Badan Pusat Statistik (BPS)</strong>. Analisis dirancang menggunakan pendekatan <em>scrollytelling</em> melalui tiga dimensi visualisasi data yang saling melengkapi: <strong>Multivariat</strong> (karakteristik sosial-ekonomi provinsi), <strong>Geospasial</strong> (sebaran kantong kemiskinan kabupaten/kota), dan <strong>Hierarki</strong> (struktur pola pengeluaran konsumsi rumah tangga).
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. KARTU RINGKASAN TIGA TOPIK (NAVIGASI KONTEKS)
# ==========================================
col_t1, col_t2, col_t3 = st.columns(3)

with col_t1:
    st.markdown("""
        <div class="topic-card" style="border-top-color: #0072B2;">
            <div class="topic-card-title">1. Dimensi Multivariat</div>
            <div class="topic-card-item"><strong>Pertanyaan:</strong> Bagaimana pengelompokan karakteristik sosial-ekonomi 38 provinsi di Indonesia?</div>
            <div class="topic-card-item"><strong>Teknik:</strong> Reduksi Dimensi (PCA Scatter Plot) & Profiling Indikator (Parallel Coordinates).</div>
            <div class="topic-card-item"><strong>Data:</strong> 8 Indikator Utama BPS 2025 (IPM, Kemiskinan, TPT, RLS, Gini, PDRB, Pengeluaran, AHH).</div>
            <div class="topic-card-item"><strong>Interaksi:</strong> Multiselect filter klaster sinkron, tooltip rincian nilai, dan pengurutan sumbu.</div>
        </div>
    """, unsafe_allow_html=True)

with col_t2:
    st.markdown("""
        <div class="topic-card" style="border-top-color: #E69F00;">
            <div class="topic-card-title">2. Dimensi Geospasial</div>
            <div class="topic-card-item"><strong>Pertanyaan:</strong> Di mana lokasi kantong kemiskinan & bagaimana disparitas spasial di 514 Kab/Kota?</div>
            <div class="topic-card-item"><strong>Teknik:</strong> Interactive Folium Map (Choropleth Layer & Proportional Symbols).</div>
            <div class="topic-card-item"><strong>Data:</strong> Persentase Penduduk Miskin (%) & Jumlah Penduduk Miskin (Ribu Jiwa) BPS 2025 + Shapefile.</div>
            <div class="topic-card-item"><strong>Interaksi:</strong> Toggle Layer Control, Zoom, Pan, dan Sticky Hover Tooltip Wilayah.</div>
        </div>
    """, unsafe_allow_html=True)

with col_t3:
    st.markdown("""
        <div class="topic-card" style="border-top-color: #785EF0;">
            <div class="topic-card-title">3. Dimensi Hierarki</div>
            <div class="topic-card-item"><strong>Pertanyaan:</strong> Bagaimana struktur prioritas pengeluaran konsumsi bulanan masyarakat Indonesia?</div>
            <div class="topic-card-item"><strong>Teknik:</strong> Visualisasi Hierarki (Interactive Treemap & Sunburst Chart).</div>
            <div class="topic-card-item"><strong>Data:</strong> Rata-rata Pengeluaran per Kapita (Rp/Bulan) Kelompok Makanan & Bukan Makanan.</div>
            <div class="topic-card-item"><strong>Interaksi:</strong> Radio Button Switcher (Treemap vs Sunburst) & Drilldown Hover Tooltip.</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. PANEL SEKILAS TEMUAN & CARA MENGGUNAKAN
# ==========================================
col_f1, col_f2 = st.columns(2)

with col_f1:
    st.markdown("""
        <div class="info-panel">
            <div class="info-panel-header">Sekilas Temuan Utama (Key Insights)</div>
            <ul style="color: #CBD5E1; font-size: 0.875rem; padding-left: 1.2rem; margin: 0; line-height: 1.6;">
                <li style="margin-bottom: 8px;">
                    <strong>Ketimpangan Wilayah:</strong> DKI Jakarta dan DI Yogyakarta mendominasi Klaster Kesejahteraan Tinggi (IPM > 80), sedangkan provinsi wilayah timur menghadapi tantangan pembangunan yang signifikan.
                </li>
                <li style="margin-bottom: 8px;">
                    <strong>Kantong Kemiskinan:</strong> Kabupaten/Kota di wilayah timur Indonesia mencatat persentase kemiskinan tertinggi, tetapi akumulasi jumlah penduduk miskin terbesar berada di pulau Jawa.
                </li>
                <li>
                    <strong>Struktur Pengeluaran:</strong> Pengeluaran untuk komoditas <strong>Rokok & Tembakau</strong> menempati porsi sangat dominan pada kelompok Makanan, bahkan melampaui pengeluaran protein telur dan daging.
                </li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col_f2:
    st.markdown("""
        <div class="info-panel">
            <div class="info-panel-header">Cara Menggunakan Dasbor</div>
            <ol style="color: #CBD5E1; font-size: 0.875rem; padding-left: 1.2rem; margin: 0; line-height: 1.6;">
                <li style="margin-bottom: 8px;">
                    <strong>Tinjau Indikator Utama:</strong> Pelajari ringkasan statistik nasional pada kartu KPI metric di bawah ini untuk mendapatkan gambaran awal.
                </li>
                <li style="margin-bottom: 8px;">
                    <strong>Gunakan Filter Interaktif:</strong> Saring data provinsi berdasarkan klaster pada grafik Multivariat, atau pilih mode tampilan Treemap/Sunburst pada bagian Hierarki.
                </li>
                <li>
                    <strong>Eksplorasi Peta & Unduh Data:</strong> Aktifkan layer peta geospasial melalui menu di pojok kanan atas peta, lalu unduh dataset resmi CSV pada tombol di setiap akhir topik.
                </li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 5. LOAD & CACHE DATASET & HELPER FUNCTIONS
# ==========================================
@st.cache_data
def load_datasets():
    # Dataset Multivariat Provinsi
    df_multi = pd.read_csv("data/Dataset_Multivariat_Final_Complete.csv")
    df_multi = df_multi.drop_duplicates(subset=['Provinsi']).reset_index(drop=True)
    
    # Dataset Geospasial Kabupaten/Kota
    df_geo = pd.read_csv("data/Dataset_Geospasial_Kemiskinan_Final.csv")
    df_geo['kodekab'] = df_geo['kodekab'].astype(str).str.zfill(4)
    
    # 1. Hapus baris agregat tingkat provinsi 'D I YOGYAKARTA' agar Kota Yogyakarta (3471) tidak terhapus saat deduplikasi
    df_geo = df_geo[~df_geo['Kabupaten_Kota'].str.upper().isin(['D I YOGYAKARTA', 'DIYOGYAKARTA', 'PROVINSI DI YOGYAKARTA'])].reset_index(drop=True)
    
    # 2. Tambahkan baris Kabupaten Gorontalo (7502) jika belum ada agar genap 514 Kabupaten/Kota se-Indonesia
    if '7502' not in df_geo['kodekab'].values:
        row_gorontalo = pd.DataFrame([{
            'kodekab': '7502',
            'Kabupaten_Kota': 'Kabupaten Gorontalo',
            'Persentase_Penduduk_Miskin': 17.16,
            'Jumlah_Penduduk_Miskin_Ribu': 70.83
        }])
        df_geo = pd.concat([df_geo, row_gorontalo], ignore_index=True)
    
    # Load Shapefile Administrasi Kabupaten
    gdf = gpd.read_file("data/Administrasi_Kabupaten.shp")
    gdf['kodekab'] = gdf['kodekab'].astype(str).str.zfill(4)
    
    # ---------------------------------------------------------
    # ROUTINE VALIDASI & MATCHING KODEKAB BERDASARKAN NAMA WILAYAH
    # ---------------------------------------------------------
    def clean_region_name(text):
        if not isinstance(text, str):
            return ""
        s = text.upper()
        s = re.sub(r'^(KABUPATEN|KAB\.|KAB|KOTA)\s+', '', s)
        s = re.sub(r'[^A-Z0-9]', '', s)
        return s

    gdf['clean_name'] = gdf['nmkab'].apply(clean_region_name)
    gdf['is_kota_code'] = gdf['kodekab'].apply(lambda c: c[2] >= '7' if len(c) == 4 else False)

    df_geo['clean_name'] = df_geo['Kabupaten_Kota'].apply(clean_region_name)
    df_geo['is_kota_text'] = df_geo['Kabupaten_Kota'].str.upper().str.contains('KOTA')

    # Pemetaan Referensi dari Shapefile: (clean_name, is_kota) -> kodekab resmi
    shape_map = {}
    for _, row in gdf.iterrows():
        shape_map[(row['clean_name'], row['is_kota_code'])] = row['kodekab']

    # Patching Kodekab pada df_geo berdasarkan pencocokan nama & tipe wilayah
    patched_codes = []
    for idx, row in df_geo.iterrows():
        name = row['clean_name']
        is_k = row['is_kota_text']
        orig_code = row['kodekab']
        
        if (name, is_k) in shape_map:
            true_code = shape_map[(name, is_k)]
        elif (name, not is_k) in shape_map:
            true_code = shape_map[(name, not is_k)]
        else:
            true_code = orig_code
        patched_codes.append(true_code)

    df_geo['kodekab'] = patched_codes

    # Hapus duplikasi kodekab jika ada baris agregat non-kabupaten
    df_geo = df_geo.drop_duplicates(subset=['kodekab'], keep='first').reset_index(drop=True)
    gdf = gdf.drop(columns=['clean_name', 'is_kota_code'])
    df_geo = df_geo.drop(columns=['clean_name', 'is_kota_text'])
    
    # Penyederhanaan geometri & Konversi CRS ke EPSG:4326 untuk Folium
    gdf['geometry'] = gdf['geometry'].simplify(tolerance=0.005, preserve_topology=True)
    gdf = gdf.to_crs(epsg=4326)
    
    # Merge Shapefile dengan Data Kemiskinan yang telah divalidasi
    merged_gdf = gdf.merge(df_geo, on='kodekab', how='inner')
    
    # Dataset Hierarki Pengeluaran (Gunakan fillna(0) agar Plotly dapat menghitung ukuran parent node)
    df_hierarchy = pd.read_csv("data/Dataset_Hierarki_Pengeluaran.csv")
    df_hierarchy['value_clean'] = pd.to_numeric(df_hierarchy['value'], errors='coerce').fillna(0)
    
    return df_multi, df_geo, merged_gdf, df_hierarchy

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

df_multi, df_geo, merged_gdf, df_hierarchy = load_datasets()

# Ringkasan Eksekutif (KPI Metrics)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown("""
        <div class="metric-card">
            <h4>Cakupan Wilayah</h4>
            <h2>38 Provinsi</h2>
        </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown(f"""
        <div class="metric-card">
            <h4>Kabupaten / Kota</h4>
            <h2>{len(df_geo)} Wilayah</h2>
        </div>
    """, unsafe_allow_html=True)
with col_m3:
    avg_ipm = df_multi['Indeks Pembangunan Manusia'].mean()
    st.markdown(f"""
        <div class="metric-card">
            <h4>Rata-rata IPM</h4>
            <h2>{avg_ipm:.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
with col_m4:
    avg_poverty = df_geo['Persentase_Penduduk_Miskin'].mean()
    st.markdown(f"""
        <div class="metric-card">
            <h4>Rata-rata Kemiskinan</h4>
            <h2>{avg_poverty:.2f}%</h2>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================
# BAGIAN 1: MULTIVARIAT (Karakteristik Provinsi)
# ==========================================
st.header("1. Wajah Ketimpangan Antar Provinsi (Multivariat)")
st.markdown("""
Analisis multivariat ini mereduksi 8 indikator sosial-ekonomi (IPM, Persentase Kemiskinan, TPT, Rata-rata Lama Sekolah, Gini Ratio, PDRB per Kapita, Pengeluaran per Kapita, dan Angka Harapan Hidup) menjadi 2 Komponen Utama (PCA). 
Provinsi-provinsi diidentifikasi ke dalam **3 Klaster Kesejahteraan** menggunakan algoritma *K-Means* untuk mewujudkan **Brushing & Linking** antar tampilan visual.
""")

# Skalasi & Analisis PCA
features = [
    'Indeks Pembangunan Manusia', 'Persentase_Miskin', 'TPT',
    'Rata_Rata_Lama_Sekolah', 'Gini_Ratio', 'PDRB_per_Kapita',
    'Pengeluaran_per_Kapita', 'Angka_Harapan_Hidup'
]

X = df_multi[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)
pcs = pca.fit_transform(X_scaled)
df_multi['PC1'] = pcs[:, 0]
df_multi['PC2'] = pcs[:, 1]

var_pc1 = pca.explained_variance_ratio_[0] * 100
var_pc2 = pca.explained_variance_ratio_[1] * 100

# Clustering KMeans
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_multi['Cluster_ID'] = kmeans.fit_predict(X_scaled)

cluster_names = {
    0: 'Klaster 1: Kesejahteraan Tinggi',
    1: 'Klaster 2: Kesejahteraan Menengah',
    2: 'Klaster 3: Tantangan Pembangunan'
}
df_multi['Klaster'] = df_multi['Cluster_ID'].map(cluster_names)

color_discrete_map = {
    'Klaster 1: Kesejahteraan Tinggi': '#0072B2',     # Biru (Colorblind-Safe)
    'Klaster 2: Kesejahteraan Menengah': '#E69F00',   # Oranye (Colorblind-Safe)
    'Klaster 3: Tantangan Pembangunan': '#785EF0'     # Ungu (Colorblind-Safe)
}

# Filter Klaster Interaktif (Multiselect)
all_klasters = list(cluster_names.values())
selected_klasters = st.multiselect(
    "Filter Klaster Provinsi (Berlaku Sinkron untuk Scatter Plot & Parallel Coordinates):",
    options=all_klasters,
    default=all_klasters,
    help="Pilih satu atau beberapa klaster untuk memfilter tampilan grafik di bawah ini."
)

df_multi_filtered = df_multi[df_multi['Klaster'].isin(selected_klasters)]

if df_multi_filtered.empty:
    st.warning("Harap pilih minimal satu klaster pada filter di atas untuk menampilkan grafik.")
else:
    # PCA Scatter Plot (Lebar Penuh)
    st.subheader("A. Pengelompokan Provinsi (PCA Scatter Plot)")
    
    fig_pca = px.scatter(
        df_multi_filtered,
        x='PC1',
        y='PC2',
        color='Klaster',
        hover_name='Provinsi',
        hover_data=features,
        color_discrete_map=color_discrete_map,
        labels={
            'PC1': f'Komponen Utama 1 (PC1: {var_pc1:.1f}% Variansi)',
            'PC2': f'Komponen Utama 2 (PC2: {var_pc2:.1f}% Variansi)'
        },
        height=480
    )
    
    fig_pca.update_traces(
        mode='markers',
        marker=dict(size=12, opacity=0.85, line=dict(width=1, color='DarkSlateGrey'))
    )
    
    fig_pca.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    
    st.plotly_chart(fig_pca, use_container_width=True)

    st.markdown("---")

    # Parallel Coordinates (Lebar Penuh)
    st.subheader("B. Profil 8 Indikator (Parallel Coordinates)")
    
    ordered_features = [
        'PDRB_per_Kapita',
        'Pengeluaran_per_Kapita',
        'Persentase_Miskin',
        'Indeks Pembangunan Manusia',
        'Rata_Rata_Lama_Sekolah',
        'Angka_Harapan_Hidup',
        'TPT',
        'Gini_Ratio'
    ]
    
    feature_short_names = {
        'Indeks Pembangunan Manusia': 'IPM',
        'Persentase_Miskin': 'Kemiskinan (%)',
        'TPT': 'TPT (%)',
        'Rata_Rata_Lama_Sekolah': 'RLS (Thn)',
        'Gini_Ratio': 'Gini Ratio',
        'PDRB_per_Kapita': 'PDRB/Kap',
        'Pengeluaran_per_Kapita': 'Pengeluaran/Kap',
        'Angka_Harapan_Hidup': 'AHH (Thn)'
    }
    
    dimensions = []
    for col in ordered_features:
        dimensions.append(
            dict(
                range=[df_multi[col].min(), df_multi[col].max()],
                label=feature_short_names.get(col, col),
                values=df_multi_filtered[col]
            )
        )
    
    fig_parcoords = go.Figure(data=go.Parcoords(
        line=dict(
            color=df_multi_filtered['Cluster_ID'],
            colorscale=[
                [0.0, 'rgba(0, 114, 178, 0.45)'],    # Biru (Klaster 1)
                [0.5, 'rgba(230, 159, 0, 0.45)'],    # Oranye (Klaster 2)
                [1.0, 'rgba(120, 94, 240, 0.45)']    # Ungu (Klaster 3)
            ],
            showscale=False
        ),
        dimensions=dimensions
    ))
    
    fig_parcoords.update_layout(
        height=500,
        margin=dict(l=60, r=60, t=50, b=30)
    )
    
    st.plotly_chart(fig_parcoords, use_container_width=True)

st.markdown('<p class="source-caption">Sumber: BPS (Badan Pusat Statistik) — Indikator Sosial Ekonomi Provinsi 2025</p>', unsafe_allow_html=True)

st.download_button(
    label="Unduh Data Multivariat 2025 (CSV)",
    data=convert_df_to_csv(df_multi),
    file_name="data_multivariat_2025.csv",
    mime="text/csv",
    type="primary",
    help="Klik untuk mengunduh dataset indikator multivariat 38 provinsi dalam format CSV."
)

st.divider()

# ==========================================
# BAGIAN 2: GEOSPASIAL (Sebaran Kemiskinan Kab/Kota)
# ==========================================
st.header("2. Kantong Kemiskinan di Pelosok Negeri (Geospasial)")
st.markdown("""
Peta geospasial interaktif ini menggambarkan ketimpangan kemiskinan di 514 Kabupaten/Kota se-Indonesia. 
Anda dapat mengontrol dua *layer* visualisasi melalui menu di pojok kanan atas peta:
- **Layer Choropleth (Rasio Persentase Kemiskinan):** Menampilkan tingkat kerentanan kemiskinan dengan gradasi warna yang ramah buta warna (*Colorblind-friendly YlOrRd*).
- **Layer Simbol Proporsional (Jumlah Penduduk Miskin):** Menampilkan lingkaran dengan ukuran proporsional terhadap akumulasi beban absolut penduduk miskin (ribu jiwa).
""")

# Inisialisasi Peta Folium
map_center = [-2.548926, 118.0148634]
m = folium.Map(location=map_center, zoom_start=5, tiles="OpenStreetMap")

# Layer 1: Choropleth (Persentase Penduduk Miskin)
choropleth = folium.Choropleth(
    geo_data=merged_gdf,
    name="Persentase Penduduk Miskin (%)",
    data=merged_gdf,
    columns=['kodekab', 'Persentase_Penduduk_Miskin'],
    key_on='feature.properties.kodekab',
    fill_color='YlOrRd',
    fill_opacity=0.75,
    line_opacity=0.3,
    legend_name='Persentase Penduduk Miskin (%)',
    smooth_factor=0.5
).add_to(m)

# Tooltip GeoJson Interaktif Layer Choropleth
geojson_tooltip = folium.GeoJson(
    merged_gdf,
    name="Info Wilayah (Tooltip)",
    style_function=lambda x: {'fillColor': '#ffffff00', 'color': '#00000000'},
    tooltip=folium.GeoJsonTooltip(
        fields=['Kabupaten_Kota', 'Persentase_Penduduk_Miskin', 'Jumlah_Penduduk_Miskin_Ribu'],
        aliases=['Kabupaten/Kota:', 'Persentase Miskin (%):', 'Jumlah Penduduk Miskin (Ribu):'],
        localize=True,
        sticky=True
    )
).add_to(m)

# Layer 2: Proportional Symbol (Jumlah Penduduk Miskin)
symbol_layer = folium.FeatureGroup(name="Jumlah Absolut Penduduk Miskin (Ribu Jiwa)", overlay=True, show=False)

for _, row in merged_gdf.iterrows():
    if row.geometry is not None:
        centroid = row.geometry.centroid
        radius = np.sqrt(row['Jumlah_Penduduk_Miskin_Ribu']) * 1.5
        
        folium.CircleMarker(
            location=[centroid.y, centroid.x],
            radius=max(radius, 3),
            popup=f"<b>{row['Kabupaten_Kota']}</b><br>Jumlah Miskin: {row['Jumlah_Penduduk_Miskin_Ribu']} ribu jiwa<br>Persentase: {row['Persentase_Penduduk_Miskin']}%",
            tooltip=f"{row['Kabupaten_Kota']}: {row['Jumlah_Penduduk_Miskin_Ribu']} ribu jiwa",
            color='#b30000',
            fill=True,
            fill_color='#e34a33',
            fill_opacity=0.6,
            weight=1
        ).add_to(symbol_layer)

symbol_layer.add_to(m)

# Layer Control
folium.LayerControl(collapsed=False).add_to(m)

# Tampilkan Peta di Streamlit
st_folium(m, use_container_width=True, height=580, returned_objects=[])

st.markdown('<p class="source-caption">Sumber: BPS (Badan Pusat Statistik) — Persentase & Jumlah Penduduk Miskin Kabupaten/Kota 2025</p>', unsafe_allow_html=True)

st.download_button(
    label="Unduh Data Geospasial Kemiskinan 2025 (CSV)",
    data=convert_df_to_csv(df_geo),
    file_name="data_geospasial_kemiskinan_2025.csv",
    mime="text/csv",
    type="primary",
    help="Klik untuk mengunduh dataset tingkat kemiskinan 514 Kabupaten/Kota dalam format CSV."
)

st.divider()

# ==========================================
# BAGIAN 3: DATA BERHIERARKI (Struktur Pengeluaran)
# ==========================================
st.header("3. Ironi Konsumsi: Makanan vs Bukan Makanan (Hierarki)")
st.markdown("""
Bagaimana masyarakat Indonesia mendistribusikan anggaran pengeluaran bulannya? 
Visualisasi hierarkis di bawah ini menguraikan struktur rata-rata pengeluaran per kapita (Rp/bulan) untuk kelompok kebutuhan **Makanan** dan **Bukan Makanan**.
""")

col_h1, col_h2 = st.columns([1, 3])

with col_h1:
    st.subheader("Mode Tampilan")
    chart_type = st.radio(
        "Pilih Visualisasi Hierarki:",
        ["Treemap (Kotak)", "Sunburst (Lingkaran)"],
        index=0
    )
    
    st.markdown("""
    **Temuan Penting:**
    - Pengeluaran untuk **Rokok** menempati porsi yang sangat tinggi di kelompok Makanan, bahkan melampaui komoditas esensial seperti daging, telur, dan buah-buahan.
    - Pada kelompok Bukan Makanan, **Perumahan & Fasilitas Rumah Tangga** mendominasi porsi pengeluaran utama masyarakat.
    """)

with col_h2:
    if chart_type == "Treemap (Kotak)":
        fig_hierarki = px.treemap(
            df_hierarchy,
            names='id',
            parents='parent',
            values='value_clean',
            color='value_clean',
            color_continuous_scale='Viridis',
            title="Struktur Pengeluaran per Kapita (Treemap)"
        )
    else:
        fig_hierarki = px.sunburst(
            df_hierarchy,
            names='id',
            parents='parent',
            values='value_clean',
            color='value_clean',
            color_continuous_scale='Viridis',
            title="Struktur Pengeluaran per Kapita (Sunburst)"
        )
    
    fig_hierarki.update_traces(
        hovertemplate="<b>%{label}</b><br>Rata-rata Pengeluaran: Rp %{value:,.0f} / bln<extra></extra>"
    )
    fig_hierarki.update_layout(
        height=550,
        margin=dict(t=40, l=10, r=10, b=10)
    )
    
    st.plotly_chart(fig_hierarki, use_container_width=True)

st.markdown('<p class="source-caption">Sumber: BPS (Badan Pusat Statistik) — Rata-rata Pengeluaran per Kapita Sebulan 2025</p>', unsafe_allow_html=True)

st.download_button(
    label="Unduh Data Hierarki Pengeluaran 2025 (CSV)",
    data=convert_df_to_csv(df_hierarchy),
    file_name="data_hierarki_pengeluaran_2025.csv",
    mime="text/csv",
    type="primary",
    help="Klik untuk mengunduh rincian struktur pengeluaran per kapita dalam format CSV."
)

st.divider()

# ==========================================
# 6. BAGIAN METADATA, METODOLOGI & KAMUS DATA
# ==========================================
st.header("4. Metadata, Metodologi & Kamus Data")
st.markdown("""
Halaman metadata ini menyajikan transparansi data, dokumentasi metodologi pengolahan, serta penjelasan definisi operasional indikator yang digunakan dalam dasbor ini.
""")

# A. Tabel Sumber Data Resmi
st.subheader("Tabel Sumber Data Resmi")

data_sources = [
    {
        "No": 1,
        "Nama Dataset": "Indikator Multivariat Sosio-Ekonomi",
        "Instansi Pembuat": "Badan Pusat Statistik (BPS)",
        "Tahun Rilis": "2025",
        "Cakupan Wilayah": "38 Provinsi",
        "Format": "CSV"
    },
    {
        "No": 2,
        "Nama Dataset": "Persentase & Jumlah Penduduk Miskin",
        "Instansi Pembuat": "Badan Pusat Statistik (BPS)",
        "Tahun Rilis": "2025",
        "Cakupan Wilayah": "514 Kabupaten/Kota",
        "Format": "CSV"
    },
    {
        "No": 3,
        "Nama Dataset": "Peta Geometri Administrasi Kabupaten/Kota",
        "Instansi Pembuat": "Badan Informasi Geospasial (BIG) / BPS",
        "Tahun Rilis": "2025",
        "Cakupan Wilayah": "Batas Spasial Indonesia",
        "Format": "Shapefile (SHP)"
    },
    {
        "No": 4,
        "Nama Dataset": "Struktur Pengeluaran per Kapita Sebulan",
        "Instansi Pembuat": "Badan Pusat Statistik (BPS - Susenas)",
        "Tahun Rilis": "2025",
        "Cakupan Wilayah": "Kelompok Makanan & Bukan Makanan",
        "Format": "CSV"
    }
]

df_sources = pd.DataFrame(data_sources)
st.table(df_sources)

# B. Catatan Metodologi & Keterbatasan
with st.expander("Catatan Metodologi & Keterbatasan Data", expanded=False):
    st.markdown("""
    #### 1. Validasi & Pembersihan Data (*Data Cleaning*)
    - **Harmonisasi Kode Wilayah:** Dilakukan normalisasi kode kabupaten/kota (`kodekab`) 4 digit string dengan pengisi nol (*zero padding*). 
    - **Pencocokan Nama & Geometri:** Menerapkan fungsi pembersihan nama wilayah (*text stripping*) untuk mengatasi perbedaan penulisan entitas antara dataset BPS dan batas administrasi Shapefile.
    
    #### 2. Analisis Komponen Utama (*Principal Component Analysis / PCA*)
    - **Standarisasi Fitur:** Sebelum ekstraksi komponen, 8 indikator terstandarisasi menggunakan *StandardScaler* ($\\mu=0, \\sigma=1$) untuk menghilangkan bias variansi antar skala variabel.
    - **Reduksi Dimensi:** 2 Komponen Utama (PC1 & PC2) diekstrak untuk merangkum mayoritas ragam data spasial-ekonomi provinsi Indonesia.
    
    #### 3. Pengelompokan Klaster (*K-Means Clustering*)
    - **Algoritma:** Algoritma *K-Means* ($K=3, \\text{random\\_state}=42$) membagi 38 provinsi ke dalam 3 kelompok kesejahteraan: *Kesejahteraan Tinggi*, *Kesejahteraan Menengah*, dan *Tantangan Pembangunan*.
    
    #### 4. Penyederhanaan Geometri Spasial
    - **Optimasi Performa Peta:** Geometri Shapefile disederhanakan dengan *Douglas-Peucker simplification algorithm* (tolerance = 0.005) serta ditransformasi ke koordinat WGS84 (EPSG:4326) untuk meningkatkan kecepatan rendering peta interaktif Folium.
    
    #### 5. Peran Kecerdasan Buatan (*AI Assistance*)
    - Pengolahan data, perancangan struktur visualisasi interaktif, pembentukan tema *Dark Analytics*, serta pengkodean komponen UI Streamlit dalam dasbor ini dibantu oleh teknologi Kecerdasan Buatan (AI) secara terstruktur.
    """)

# C. Kamus Data & Definisi Indikator
with st.expander("Kamus Data & Definisi Indikator", expanded=False):
    st.markdown("""
    | Indikator | Satuan | Definisi Operasional Resmi |
    |---|---|---|
    | **Indeks Pembangunan Manusia (IPM)** | Skala 0–100 | Ukuran komposit pencapaian umur panjang & sehat, pengetahuan (RLS & HLS), dan standar hidup layak. |
    | **Tingkat Pengangguran Terbuka (TPT)** | Persen (%) | Persentase jumlah penganggur terhadap total angkatan kerja. |
    | **Persentase Penduduk Miskin** | Persen (%) | Persentase penduduk dengan pengeluaran per kapita sebulan di bawah Garis Kemiskinan. |
    | **Jumlah Penduduk Miskin** | Ribu Jiwa | Jumlah absolut penduduk yang hidup di bawah garis kemiskinan. |
    | **Gini Ratio** | Rasio 0–1 | Ukuran ketimpangan pengeluaran penduduk (0 = pemerataan sempurna, 1 = ketimpangan sempurna). |
    | **PDRB per Kapita** | Juta Rp/Thn | Nilai tambah bruto seluruh barang & jasa di suatu daerah dibagi jumlah penduduk. |
    | **Rata-rata Lama Sekolah (RLS)** | Tahun | Rata-rata lamanya tahun yang ditempuh oleh penduduk usia 25 tahun ke atas dalam pendidikan formal. |
    | **Angka Harapan Hidup (AHH)** | Tahun | Perkiraan rata-rata jumlah tahun hidup yang akan dijalani oleh seseorang sejak lahir. |
    | **Pengeluaran per Kapita** | Rp/Bulan | Biaya konsumsi makanan dan bukan makanan per anggota rumah tangga per bulan. |
    """)

# ==========================================
# 7. FOOTER HAK CIPTA
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6C757D; font-size: 0.85rem; padding-bottom: 20px;">
    <i>Aplikasi Dasbor Interaktif Komando Kesejahteraan Indonesia 2025.<br>
    Dikembangkan untuk Tugas Akhir Semester Mata Kuliah Visualisasi Data dan Informasi.<br>
    Politeknik Statistika STIS — 2026.</i>
</div>
""", unsafe_allow_html=True)