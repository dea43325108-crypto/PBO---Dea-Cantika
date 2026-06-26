import os
import pandas as pd

# ==========================================
# 1. DEFINISI KELAS (DARI PRAKTIKUM 03)
# ==========================================
class Lokasi:
    def __init__(self, nama, latitude, longitude, deskripsi=""):
        self.nama = nama
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.deskripsi = deskripsi

class TempatWisata(Lokasi):
    def __init__(self, nama, latitude, longitude, tipe, deskripsi):
        super().__init__(nama, latitude, longitude, deskripsi)
        self.tipe = tipe

    def __repr__(self):
        return f"<TempatWisata: '{self.nama}' ({self.tipe}) | Koordinat: {self.latitude}, {self.longitude}>"

class Kuliner(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi):
        super().__init__(nama, latitude, longitude, deskripsi)

    def __repr__(self):
        return f"<Kuliner: '{self.nama}' | Koordinat: {self.latitude}, {self.longitude}>"

class TempatIbadah(Lokasi):
    def __init__(self, nama, latitude, longitude, agama, deskripsi):
        super().__init__(nama, latitude, longitude, deskripsi)
        self.agama = agama

    def __repr__(self):
        return f"<TempatIbadah: '{self.nama}' ({self.agama}) | Koordinat: {self.latitude}, {self.longitude}>"


# ==========================================
# 2. FUNGSI MEMBACA DATA (DARI PRAKTIKUM 02)
# ==========================================
def baca_data_lokasi(nama_file: str) -> pd.DataFrame:
    """Membaca file CSV dan membersihkan spasi pada nama kolom"""
    try:
        df = pd.read_csv(nama_file)
        # SOLUSI KUNCI: Menghilangkan spasi di awal/akhir nama kolom CSV
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"[ERROR] Gagal membaca file {nama_file}: {e}")
        return None


# ==========================================
# 3. FUNGSI PEMBUATAN OBJEK (PRAKTIKUM 04)
# ==========================================
def buat_objek_lokasi_dari_df(dataframe: pd.DataFrame) -> list:
    list_objek_lokasi = []
    if dataframe is None or dataframe.empty:
        print("DataFrame kosong atau None, tidak ada objek dibuat.")
        return list_objek_lokasi
    
    print("\nMembuat objek dari DataFrame...")
    for index, row in dataframe.iterrows():
        # Mengambil data menggunakan key yang sudah bersih dari spasi
        nama = row.get('Nama', None)
        lat = row.get('Latitude', None)
        lon = row.get('Longitude', None)
        tipe = row.get('Tipe', 'Lainnya')
        deskripsi = row.get('Deskripsi', '')
        
        if nama is None or pd.isna(lat) or pd.isna(lon):
            continue
            
        objek = None
        try:
            # Pengecekan kategori tipe objek
            if 'Wisata' in tipe or tipe == 'Landmark':
                objek = TempatWisata(nama, lat, lon, tipe, deskripsi)
            elif tipe == 'Kuliner':
                objek = Kuliner(nama, lat, lon, deskripsi)
            elif 'Ibadah' in tipe:
                agama_info = "Umum"
                # Pengecekan berbasis string Nama atau Tipe agar lebih akurat
                if "Islam" in tipe or "Masjid" in nama: 
                    agama_info = "Islam"
                elif "Kristen" in tipe or "Gereja" in nama: 
                    agama_info = "Kristen"
                elif "Klenteng" in tipe or "Sam Poo Kong" in nama: 
                    agama_info = "Tridharma"
                
                objek = TempatIbadah(nama, lat, lon, agama_info, deskripsi)
            
            if objek:
                list_objek_lokasi.append(objek)
        except Exception as e:
            print(f" -> GAGAL membuat objek untuk '{nama}' di baris {index}: {e}")
            
    print(f"Total {len(list_objek_lokasi)} objek lokasi berhasil dibuat dari {len(dataframe)} baris data.")
    return list_objek_lokasi


# ==========================================
# 4. RUNNER PROGRAM UTAMA
# ==========================================
if __name__ == "__main__":
    nama_file_csv = "lokasi_semarang.csv"

    # Membuat file CSV otomatis jika belum ada di folder (untuk uji coba langsung)
    if not os.path.exists(nama_file_csv):
        data_mentah = """Nama, Latitude, Longitude, Tipe, Deskripsi
Lawang Sewu,-6.9840,110.4105,Wisata Sejarah,Bangunan bersejarah peninggalan Belanda dengan banyak pintu.
Simpang Lima,-6.9929,110.4200,Landmark,"Alun-alun pusat kota Semarang, tempat berkumpul populer."
Masjid Agung Jawa Tengah,-6.9892,110.4452,Tempat Ibadah,Masjid besar dengan arsitektur megah dan menara pandang Asmaul Husna.
Klenteng Sam Poo Kong,-6.9980,110.4030,Tempat Ibadah,Klenteng bersejarah peninggalan Laksamana Cheng Ho.
Brown Canyon,-7.0375,110.4875,Wisata Alam,"Tebing bekas penambangan galian C yang unik menyerupai Grand Canyon."
Lumpia Gang Lombok,-6.9718,110.4255,Kuliner,Salah satu tempat makan lumpia legendaris dan otentik di Semarang.
Kota Lama,-6.9690,110.4250,Wisata Sejarah,"Kawasan cagar budaya dengan bangunan-bangunan kuno bergaya Eropa."
Pantai Marina,-6.9585,110.3875,Wisata Alam,Kawasan pantai rekreasi di bagian utara kota.
Kampoeng Kopi Banaran,-7.2780,110.4010,Wisata Alam,"Agrowisata kebun kopi dengan pemandangan dan restoran."
Toko Oen,-6.9715,110.4235,Kuliner,Restoran dan toko es krim legendaris sejak zaman kolonial."""
        
        with open(nama_file_csv, "w", encoding="utf-8") as f:
            f.write(data_mentah)

    print("--- Memulai Praktikum 4: Membuat Objek dari Data Pandas ---")
    df_lokasi = baca_data_lokasi(nama_file_csv)
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)
    
    print("\n--- Daftar Objek Lokasi yang Berhasil Dibuat (Hasil __repr__) ---")
    if list_semua_lokasi:
        for idx, lok in enumerate(list_semua_lokasi):
            print(f" {idx+1}. {repr(lok)}")
    else:
        print("Tidak ada objek lokasi yang dibuat.")
    print("\n--- Praktikum 4 Selesai ---")