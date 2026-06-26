import folium
from praktikum_04 import baca_data_lokasi, buat_objek_lokasi_dari_df

print("--- Memulai Praktikum 5: Visualisasi Peta dengan Folium ---\n")

nama_file = "lokasi_semarang.csv"

print(f"Mencoba membaca file CSV: {nama_file}\n")

df = baca_data_lokasi(nama_file)

if df is not None:

    daftar_lokasi = buat_objek_lokasi_dari_df(df)

    print(f"\nMemulai pembuatan peta Folium dari {len(daftar_lokasi)} lokasi...")

    pusat_peta = [
        daftar_lokasi[0].latitude,
        daftar_lokasi[0].longitude
    ]

    peta = folium.Map(
        location=pusat_peta,
        zoom_start=13
    )

    print(
        f" -> Objek peta dibuat, berpusat di ({pusat_peta[0]:.4f}, {pusat_peta[1]:.4f})"
    )

    jumlah_marker = 0

    for lokasi in daftar_lokasi:

        popup_text = f"""
        <b>{lokasi.nama}</b><br>
        {lokasi.deskripsi}
        """

        folium.Marker(
            location=[lokasi.latitude, lokasi.longitude],
            popup=popup_text
        ).add_to(peta)

        jumlah_marker += 1

    nama_output = "peta_interaktif_semarang.html"

    peta.save(nama_output)

    print(
        f"\n -> Peta berhasil dibuat dan disimpan sebagai '{nama_output}'."
    )

    print(
        f"    Total marker ditambahkan: {jumlah_marker}"
    )

    print(
        f"\nSilakan buka file '{nama_output}' di browser Anda untuk melihat hasilnya."
    )

else:
    print("Gagal membaca data CSV.")

print("\n--- Praktikum 5 Selesai ---")