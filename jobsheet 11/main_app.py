# main_app.py

import streamlit as st
import datetime
import pandas as pd
import locale
import time

try:

    locale.setlocale(
        locale.LC_ALL,
        'id_ID.UTF-8'
    )

except locale.Error:

    try:

        locale.setlocale(
            locale.LC_ALL,
            'Indonesian_Indonesia.1252'
        )

    except:

        print("Locale Indonesia tidak tersedia.")


def format_rp(angka):

    try:

        return locale.currency(
            angka or 0,
            grouping=True,
            symbol='Rp '
        )[:-3]

    except:

        return (
            f"Rp {angka or 0:,.0f}"
            .replace(",", ".")
        )


try:

    from model import Transaksi
    from manajer_anggaran import AnggaranHarian
    from konfigurasi import KATEGORI_PENGELUARAN

except ImportError as e:

    st.error(f"Gagal import modul: {e}")

    st.stop()


st.set_page_config(
    page_title="Catatan Pengeluaran",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# CACHE MANAGER
# =========================
@st.cache_resource
def get_anggaran_manager():

    print(">>> INIT AnggaranHarian")

    return AnggaranHarian()


anggaran = get_anggaran_manager()


# =========================
# HALAMAN INPUT
# =========================
def halaman_input(anggaran: AnggaranHarian):

    st.header("📝 Tambah Pengeluaran Baru")

    with st.form(
        "form_transaksi_baru",
        clear_on_submit=True
    ):

        col1, col2 = st.columns([3, 1])

        with col1:

            deskripsi = st.text_input(
                "Deskripsi",
                placeholder="Contoh: Makan siang"
            )

        with col2:

            kategori = st.selectbox(
                "Kategori:",
                KATEGORI_PENGELUARAN,
                index=0
            )

        col3, col4 = st.columns([1, 1])

        with col3:

            jumlah = st.number_input(
                "Jumlah (Rp):",
                min_value=0.01,
                step=1000.0,
                format="%.0f",
                value=None,
                placeholder="25000"
            )

        with col4:

            tanggal = st.date_input(
                "Tanggal:",
                value=datetime.date.today()
            )

        submitted = st.form_submit_button(
            "💾 Simpan Transaksi"
        )

        if submitted:

            if not deskripsi:

                st.warning(
                    "Deskripsi wajib diisi!"
                )

            elif jumlah is None or jumlah <= 0:

                st.warning(
                    "Jumlah harus lebih dari 0!"
                )

            else:

                tx = Transaksi(
                    deskripsi,
                    float(jumlah),
                    kategori,
                    tanggal
                )

                if anggaran.tambah_transaksi(tx):

                    st.success(
                        "Transaksi berhasil disimpan!"
                    )

                    time.sleep(1)

                    st.cache_data.clear()

                    st.rerun()

                else:

                    st.error(
                        "Gagal menyimpan transaksi."
                    )


# =========================
# HALAMAN RIWAYAT
# =========================
def halaman_riwayat(anggaran: AnggaranHarian):

    st.subheader("📋 Detail Semua Transaksi")

    # =========================
    # HAPUS TRANSAKSI
    # =========================
    st.markdown("### 🗑️ Hapus Transaksi")

    id_hapus = st.number_input(
        "Masukkan ID transaksi:",
        min_value=1,
        step=1
    )

    if st.button("Hapus Transaksi"):

        st.warning(
            f"Yakin ingin menghapus ID {id_hapus} ?"
        )

        if st.button("Konfirmasi Hapus"):

            berhasil = anggaran.hapus_transaksi(
                id_hapus
            )

            if berhasil:

                st.success(
                    "Transaksi berhasil dihapus."
                )

                st.cache_data.clear()

                st.rerun()

            else:

                st.error(
                    "Gagal menghapus transaksi."
                )

    st.divider()

    # =========================
    # REFRESH
    # =========================
    if st.button("🔄 Refresh Riwayat"):

        st.cache_data.clear()

        st.rerun()

    # =========================
    # TAMPILKAN DATA
    # =========================
    with st.spinner("Memuat data transaksi..."):

        df_transaksi = (
            anggaran.get_dataframe_transaksi()
        )

        if df_transaksi is None:

            st.error(
                "Gagal mengambil data."
            )

        elif df_transaksi.empty:

            st.info(
                "Belum ada transaksi."
            )

        else:

            st.dataframe(
                df_transaksi,
                use_container_width=True,
                hide_index=True
            )


# =========================
# HALAMAN RINGKASAN
# =========================
def halaman_ringkasan(anggaran: AnggaranHarian):

    st.subheader("📊 Ringkasan Pengeluaran")

    total = (
        anggaran.hitung_total_pengeluaran()
    )

    st.metric(
        "Total Pengeluaran",
        format_rp(total)
    )

    st.divider()

    dict_kategori = (
        anggaran.get_pengeluaran_per_kategori()
    )

    if not dict_kategori:

        st.info("Belum ada data.")

    else:

        data = []

        for kat, jml in dict_kategori.items():

            data.append({
                "Kategori": kat,
                "Total": jml
            })

        df = pd.DataFrame(data)

        df['Total (Rp)'] = (
            df['Total']
            .apply(format_rp)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.dataframe(
                df[['Kategori', 'Total (Rp)']],
                hide_index=True,
                use_container_width=True
            )

        with col2:

            st.bar_chart(
                df.set_index('Kategori')['Total'],
                use_container_width=True
            )


# =========================
# MAIN
# =========================
def main():

    st.sidebar.title(
        "🧮 Catatan Pengeluaran"
    )

    menu = st.sidebar.radio(
        "Pilih Menu:",
        [
            "Tambah",
            "Riwayat",
            "Ringkasan"
        ]
    )

    st.sidebar.markdown("---")

    st.sidebar.info(
        "Aplikasi Pengeluaran Harian"
    )

    manajer = get_anggaran_manager()

    if menu == "Tambah":

        halaman_input(manajer)

    elif menu == "Riwayat":

        halaman_riwayat(manajer)

    elif menu == "Ringkasan":

        halaman_ringkasan(manajer)

    st.markdown("---")

    st.caption(
        "Pengembangan Aplikasi OOP + SQLite"
    )


if __name__ == "__main__":

    main()