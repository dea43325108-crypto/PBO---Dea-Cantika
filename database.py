# database.py

import sqlite3
import pandas as pd
from konfigurasi import DB_PATH


def get_db_connection() -> sqlite3.Connection | None:

    try:

        conn = sqlite3.connect(
            DB_PATH,
            timeout=10,
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        conn.row_factory = sqlite3.Row

        return conn

    except sqlite3.Error as e:

        print(f"ERROR [database.py] Koneksi DB gagal: {e}")

        return None


# =========================
# EXECUTE QUERY
# =========================
def execute_query(query: str, params: tuple = None):

    conn = get_db_connection()

    if not conn:
        return None

    try:

        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        conn.commit()

        # jumlah row yang berubah
        return cursor.rowcount

    except sqlite3.Error as e:

        print(f"ERROR [database.py] Query gagal: {e}")

        conn.rollback()

        return None

    finally:

        if conn:
            conn.close()


# =========================
# FETCH QUERY
# =========================
def fetch_query(
    query: str,
    params: tuple = None,
    fetch_all: bool = True
):

    conn = get_db_connection()

    if not conn:
        return None

    try:

        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = (
            cursor.fetchall()
            if fetch_all
            else cursor.fetchone()
        )

        return result

    except sqlite3.Error as e:

        print(f"ERROR [database.py] Fetch gagal: {e}")

        return None

    finally:

        if conn:
            conn.close()


# =========================
# DATAFRAME
# =========================
def get_dataframe(
    query: str,
    params: tuple = None
) -> pd.DataFrame:

    conn = get_db_connection()

    if not conn:
        return pd.DataFrame()

    try:

        df = pd.read_sql_query(
            query,
            conn,
            params=params
        )

        return df

    except Exception as e:

        print(
            f"ERROR [database.py] "
            f"Gagal baca DataFrame: {e}"
        )

        return pd.DataFrame()

    finally:

        if conn:
            conn.close()


# =========================
# SETUP DATABASE
# =========================
def setup_database_initial():

    print(
        f"Memeriksa/membuat tabel database: {DB_PATH}"
    )

    conn = get_db_connection()

    if not conn:
        return False

    try:

        cursor = conn.cursor()

        sql_create_table = """
        CREATE TABLE IF NOT EXISTS transaksi (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            deskripsi TEXT NOT NULL,

            jumlah REAL NOT NULL
            CHECK(jumlah > 0),

            kategori TEXT,

            tanggal DATE NOT NULL

        );
        """

        cursor.execute(sql_create_table)

        conn.commit()

        print(" -> Tabel transaksi siap.")

        return True

    except sqlite3.Error as e:

        print(f"ERROR setup tabel: {e}")

        return False

    finally:

        if conn:
            conn.close()