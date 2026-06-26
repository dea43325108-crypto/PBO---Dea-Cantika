# PENUGASAN: Mini Project SIG - Tambah Kelas, Marker Kustom, Config File

import pandas as pd
import folium
import datetime
from abc import ABC, abstractmethod

# ============================================================
# KELAS DASAR + KELAS LAMA (dari Praktikum 3)
# ============================================================

class Lokasi(ABC):
    def __init__(self, nama, latitude, longitude):
        self.nama = str(nama) if nama else "Tanpa Nama"
        try:
            self.latitude, self.longitude = float(latitude), float(longitude)
        except (ValueError, TypeError):
            self.latitude, self.longitude = 0.0, 0.0
    def get_koordinat(self): return (self.latitude, self.longitude)
    @abstractmethod
    def get_info_popup(self) -> str: pass
    def __repr__(self): return f"{type(self).__name__}(nama='{self.nama}', lat={self.latitude:.4f}, lon={self.longitude:.4f})"
    def __str__(self): return f"{self.nama} [{type(self).__name__}]"

class TempatWisata(Lokasi):
    def __init__(self, nama, latitude, longitude, jenis, deskripsi):
        super().__init__(nama, latitude, longitude)
        self.jenis_wisata = str(jenis) if jenis else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tidak ada deskripsi."
    def get_info_popup(self):
        return f"<h4><b>{self.nama}</b></h4><i>{self.jenis_wisata}</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class Kuliner(Lokasi):
    def __init__(self, nama, latitude, longitude, menu_andalan):
        super().__init__(nama, latitude, longitude)
        self.menu_andalan = str(menu_andalan) if menu_andalan else "Tidak diketahui"
    def get_info_popup(self):
        return f"<h4><b>{self.nama}</b></h4><i>Kuliner</i><br><br>Menu Andalan: {self.menu_andalan}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class TempatIbadah(Lokasi):
    def __init__(self, nama, latitude, longitude, agama="Umum", deskripsi=""):
        super().__init__(nama, latitude, longitude)
        self.agama = str(agama) if agama else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tempat Ibadah"
    def get_info_popup(self):
        return f"<h4><b>{self.nama}</b></h4><i>Tempat Ibadah ({self.agama})</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

# ============================================================
# PENUGASAN (a): KELAS BARU
# ============================================================

class Museum(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi=""):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Museum"
    def get_info_popup(self):
        return (f"<h4><b>{self.nama}</b></h4>"
                f"<i>Museum</i><br><br>"
                f"{self.deskripsi}<br><br>"
                f"Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})")

class KantorPemerintahan(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi=""):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Kantor Pemerintahan"
    def get_info_popup(self):
        return (f"<h4><b>{self.nama}</b></h4>"
                f"<i>Kantor Pemerintahan</i><br><br>"
                f"{self.deskripsi}<br><br>"
                f"Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})")

class TamanKota(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi=""):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Taman Kota"
    def get_info_popup(self):
        return (f"<h4><b>{self.nama}</b></h4>"
                f"<i>Taman Kota</i><br><br>"
                f"{self.deskripsi}<br><br>"
                f"Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})")

# ============================================================
# FUNGSI BACA DATA & BUAT OBJEK (dimodifikasi untuk tipe baru)
# ============================================================

def baca_data_lokasi(nama_file):
    try: return pd.read_csv(nama_file)
    except FileNotFoundError: print(f"ERROR: File '{nama_file}' tidak ditemukan!"); return None
    except Exception as e: print(f"ERROR: {type(e).__name__} - {e}"); return None

def buat_objek_lokasi_dari_df(dataframe) -> list:
    """Membuat objek lokasi termasuk tipe baru (Museum, Kantor, Taman)."""
    list_objek = []
    if dataframe is None or dataframe.empty: return list_objek

    print(f"\nMembuat objek dari {len(dataframe)} baris data...")
    for index, row in dataframe.iterrows():
        nama=row.get('Nama',None); lat=row.get('Latitude',None)
        lon=row.get('Longitude',None); tipe=row.get('Tipe','Lainnya')
        deskripsi=row.get('Deskripsi','')

        if nama is None or lat is None or lon is None: continue
        objek = None
        try:
            if 'Wisata' in str(tipe) or tipe == 'Landmark':
                objek = TempatWisata(nama, lat, lon, tipe, deskripsi)
            elif tipe == 'Kuliner':
                objek = Kuliner(nama, lat, lon, deskripsi)
            elif 'Ibadah' in str(tipe):
                agama = "Islam" if "Masjid" in nama else ("Tridharma" if "Klenteng" in nama else "Umum")
                objek = TempatIbadah(nama, lat, lon, agama, deskripsi)
            elif tipe == 'Museum':
                objek = Museum(nama, lat, lon, deskripsi)
            elif tipe == 'Kantor Pemerintahan':
                objek = KantorPemerintahan(nama, lat, lon, deskripsi)
            elif tipe == 'Taman Kota':
                objek = TamanKota(nama, lat, lon, deskripsi)
            else:
                print(f" -> Tipe '{tipe}' untuk '{nama}' tidak dikenali.")

            if objek: list_objek.append(objek)
        except Exception as e:
            print(f" -> GAGAL membuat objek untuk '{nama}': {e}")

    print(f"Total {len(list_objek)} objek berhasil dibuat.")
    return list_objek

# ============================================================
# PENUGASAN (b): KUSTOMISASI MARKER BERDASARKAN TIPE
# ============================================================

def tentukan_icon(lok: Lokasi) -> folium.Icon:
    """Mengembalikan ikon dan warna marker sesuai tipe objek."""
    if isinstance(lok, TempatWisata):
        return folium.Icon(color='blue', icon='camera', prefix='fa')
    elif isinstance(lok, Kuliner):
        return folium.Icon(color='red', icon='cutlery', prefix='fa')
    elif isinstance(lok, TempatIbadah):
        return folium.Icon(color='purple', icon='star', prefix='fa')
    elif isinstance(lok, Museum):
        return folium.Icon(color='orange', icon='university', prefix='fa')
    elif isinstance(lok, KantorPemerintahan):
        return folium.Icon(color='gray', icon='building', prefix='fa')
    elif isinstance(lok, TamanKota):
        return folium.Icon(color='green', icon='leaf', prefix='fa')
    else:
        return folium.Icon(color='lightblue', icon='info-sign')

# ============================================================
# PENUGASAN (c): BACA KONFIGURASI PETA DARI FILE
# ============================================================

def baca_konfigurasi_peta(file_config: str = "config_peta.txt"):
    """Membaca lat, lon, zoom dari file teks konfigurasi."""
    lat_def, lon_def, zoom_def = -6.9929, 110.4200, 13
    try:
        with open(file_config, 'r', encoding='utf-8') as f:
            baris = [b.strip() for b in f.readlines() if b.strip()]
        lat  = float(baris[0])
        lon  = float(baris[1])
        zoom = int(baris[2])
        print(f" -> Konfigurasi dibaca: lat={lat}, lon={lon}, zoom={zoom}")
        return lat, lon, zoom
    except FileNotFoundError:
        print(f" -> File config tidak ditemukan. Pakai nilai default.")
        return lat_def, lon_def, zoom_def
    except (ValueError, IndexError) as e:
        print(f" -> Error baca config ({e}). Pakai nilai default.")
        return lat_def, lon_def, zoom_def

# ============================================================
# LOGGING
# ============================================================

def tulis_log(pesan: str, file_log: str = "proses_peta.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(file_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {pesan}\n")
    except IOError as e:
        print(f"ERROR LOG: {e}")

# ============================================================
# FUNGSI BUAT PETA (gabungan semua penugasan)
# ============================================================

def buat_peta_lokasi_folium(
    list_objek: list,
    file_output: str = "peta_penugasan.html",
    file_config: str = "config_peta.txt",
    file_log: str = "proses_peta.log"
):
    """Membuat peta dengan marker kustom, konfigurasi dari file, dan logging."""
    nama_fungsi = "buat_peta_lokasi_folium"

    if not list_objek:
        pesan = f"[{nama_fungsi}] Gagal: Tidak ada data lokasi."
        print(pesan); tulis_log(pesan, file_log)
        return

    print(f"\nMemulai pembuatan peta dari {len(list_objek)} lokasi...")
    tulis_log(f"[{nama_fungsi}] Memulai '{file_output}' ({len(list_objek)} lokasi).", file_log)

    # Penugasan (c): Baca konfigurasi dari file
    lat_tengah, lon_tengah, zoom = baca_konfigurasi_peta(file_config)

    peta = folium.Map(location=[lat_tengah, lon_tengah],
                      zoom_start=zoom, tiles="OpenStreetMap")

    jumlah_marker = 0
    lokasi_dilewati = []

    for lok in list_objek:
        koordinat = lok.get_koordinat()
        if koordinat != (0.0, 0.0):
            info_popup_html = lok.get_info_popup()   # Polimorfik
            icon = tentukan_icon(lok)                 # Penugasan (b)

            folium.Marker(
                location=koordinat,
                popup=folium.Popup(info_popup_html, max_width=300),
                tooltip=lok.nama,
                icon=icon
            ).add_to(peta)
            jumlah_marker += 1
        else:
            lokasi_dilewati.append(lok.nama)

    if lokasi_dilewati:
        pesan_lewat = f"[{nama_fungsi}] Melewati: {', '.join(lokasi_dilewati)}."
        print(f" -> {pesan_lewat}")
        tulis_log(pesan_lewat, file_log)

    try:
        peta.save(file_output)
        pesan_sukses = f"[{nama_fungsi}] '{file_output}' berhasil dibuat. Marker: {jumlah_marker}."
        print(f" -> {pesan_sukses}")
        tulis_log(pesan_sukses, file_log)
    except Exception as e:
        pesan_error = f"[{nama_fungsi}] ERROR: {type(e).__name__} - {e}"
        print(f" -> {pesan_error}")
        tulis_log(pesan_error, file_log)

# ============================================================
# KODE UTAMA
# ============================================================

if __name__ == "__main__":
    NAMA_FILE_CSV    = "lokasi_semarang.csv"
    NAMA_FILE_PETA   = "peta_penugasan.html"
    NAMA_FILE_CONFIG = "config_peta.txt"
    NAMA_FILE_LOG    = "proses_peta.log"

    print("=" * 55)
    print("  PENUGASAN: Mini Project SIG")
    print("=" * 55)

    df_lokasi = baca_data_lokasi(NAMA_FILE_CSV)
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)

    print("\nDaftar semua objek lokasi:")
    for idx, lok in enumerate(list_semua_lokasi):
        print(f"  {idx+1}. {repr(lok)}")

    buat_peta_lokasi_folium(
        list_semua_lokasi,
        file_output=NAMA_FILE_PETA,
        file_config=NAMA_FILE_CONFIG,
        file_log=NAMA_FILE_LOG
    )

    print(f"\n  Buka '{NAMA_FILE_PETA}' di browser untuk melihat peta.")
    print(f"  Cek '{NAMA_FILE_LOG}' untuk log proses.")
    print("=" * 55)