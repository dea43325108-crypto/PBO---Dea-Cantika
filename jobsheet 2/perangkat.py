class Handphone:
    def __init__(self, merk, model, harga):
        self.merk = merk
        self.model = model
        self.harga = harga
        self.stok = 10  # Default stok awal

    def info_hp(self):
        print(f"[{self.merk}] {self.model} - Harga: Rp {self.harga:,} (Stok: {self.stok})")

    def hitung_diskon(self, persen):
        # Mengembalikan nilai (Return Value) harga setelah diskon
        potongan = self.harga * (persen / 100)
        return self.harga - potongan

    def jual(self, jumlah):
        if jumlah <= self.stok:
            self.stok -= jumlah
            total = self.harga * jumlah
            print(f"Berhasil menjual {jumlah} unit {self.model}. Total: Rp {total:,}")
        else:
            print(f"Maaf, stok {self.model} tidak mencukupi!")