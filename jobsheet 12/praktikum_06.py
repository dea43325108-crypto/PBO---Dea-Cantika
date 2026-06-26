from praktikum_04 import baca_data_lokasi, buat_objek_lokasi_dari_df
import folium

def buat_peta_lokasi_folium(daftar_lokasi, nama_file_peta, nama_file_log):

    pesan_awal = f"[buat_peta_lokasi_folium] Memulai pembuatan peta dari {len(daftar_lokasi)} lokasi..."

    print("\n" + pesan_awal)

    with open(nama_file_log, "a", encoding="utf-8") as log:
        log.write(pesan_awal + "\n")

    pusat = [
        daftar_lokasi[0].latitude,
        daftar_lokasi[0].longitude
    ]

    peta = folium.Map(
        location=pusat,
        zoom_start=13
    )

    jumlah_marker = 0

    for lokasi in daftar_lokasi:

        folium.Marker(
            location=[
                lokasi.latitude,
                lokasi.longitude
            ],
            popup=f"{lokasi.nama}<br>{lokasi.deskripsi}"
        ).add_to(peta)

        jumlah_marker += 1

    peta.save(nama_file_peta)

    pesan_sukses = (
        f"-> [buat_peta_lokasi_folium] "
        f"Peta '{nama_file_peta}' berhasil dibuat dengan "
        f"{jumlah_marker} marker."
    )

    print(pesan_sukses)

    with open(nama_file_log, "a", encoding="utf-8") as log:
        log.write(pesan_sukses + "\n")


# ==================================
# PROGRAM UTAMA
# ==================================

print("--- Memulai Praktikum 6: File Handling Tambahan (Log) ---\n")

nama_csv = "lokasi_semarang.csv"
nama_log = "proses_peta.log"

# kosongkan log setiap program dijalankan
with open(nama_log, "w", encoding="utf-8") as log:
    log.write("=== LOG PEMBUATAN PETA ===\n")

df = baca_data_lokasi(nama_csv)
daftar_lokasi = buat_objek_lokasi_dari_df(df)

# peta pertama
buat_peta_lokasi_folium(
    daftar_lokasi,
    "peta_interaktif_semarang.html",
    nama_log
)

print("\nMenjalankan pembuatan peta lagi untuk demo log append...\n")

# peta kedua
buat_peta_lokasi_folium(
    daftar_lokasi,
    "peta_kedua.html",
    nama_log
)

print(f"\nSilakan periksa isi file log '{nama_log}' untuk melihat catatan proses.")
print("\n--- Praktikum 6 Selesai ---")