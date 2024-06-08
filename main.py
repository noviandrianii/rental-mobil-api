from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Rental Mobil",
    description="API untuk mengelola data Rental Mobil",
    docs_url="/",  # Ubah docs_url menjadi "/"
)

@app.get("/")
async def read_root():
    return {"Data": "Successful"}

# Model untuk Data Mobil
class Mobil(BaseModel):
    id_mobil: str
    merek: str
    model: str
    tipe_mobil: str
    tahun_pembuatan: int
    warna: str
    nomor_polisi: str
    harga_sewa_per_hari: int
    status_ketersediaan: str

# Dummy data untuk mobil
data_mobil = [
    {"id_mobil": "1", "merek": "Toyota", "model": "Avanza", "tipe_mobil": "MPV", "tahun_pembuatan": 2020, "warna": "Hitam", "nomor_polisi": "B 1234 ABC", "harga_sewa_per_hari": 300000, "status_ketersediaan": "Tersedia"},
    {"id_mobil": "2", "merek": "Honda", "model": "Jazz", "tipe_mobil": "Hatchback", "tahun_pembuatan": 2019, "warna": "Putih", "nomor_polisi": "D 5678 DEF", "harga_sewa_per_hari": 350000, "status_ketersediaan": "Tersedia"},
    {"id_mobil": "3", "merek": "Suzuki", "model": "Ertiga", "tipe_mobil": "MPV", "tahun_pembuatan": 2021, "warna": "Silver", "nomor_polisi": "E 9012 GHI", "harga_sewa_per_hari": 320000, "status_ketersediaan": "Tersedia"},
    {"id_mobil": "4", "merek": "Mitsubishi", "model": "Xpander", "tipe_mobil": "MPV", "tahun_pembuatan": 2020, "warna": "Merah", "nomor_polisi": "F 3456 JKL", "harga_sewa_per_hari": 350000, "status_ketersediaan": "Tersedia"},
    {"id_mobil": "5", "merek": "Toyota", "model": "Innova", "tipe_mobil": "SUV", "tahun_pembuatan": 2022, "warna": "Abu-abu", "nomor_polisi": "G 7890 MNO", "harga_sewa_per_hari": 400000, "status_ketersediaan": "Tersedia"}
]

# Endpoint untuk menambahkan data mobil
@app.post("/mobil")
def tambah_mobil(mobil: Mobil):
    data_mobil.append(mobil.dict())
    return {"message": "Data mobil berhasil ditambahkan."}

# Endpoint untuk mendapatkan data mobil
@app.get("/mobil", response_model=List[Mobil])
def get_mobil():
    return data_mobil

def get_mobil_index(id_mobil: str):
    for index, mobil in enumerate(data_mobil):
        if mobil['id_mobil'] == id_mobil:
            return index
    return None

# Endpoint untuk detail get id
@app.get("/mobil/{id_mobil}", response_model=Optional[Mobil])
def get_mobil_by_id(id_mobil: str):
    for mobil in data_mobil:
        if mobil['id_mobil'] == id_mobil:
            return Mobil(**mobil)
    return None

# Endpoint untuk memperbarui data mobil dengan hanya memasukkan id_mobil
@app.put("/mobil/{id_mobil}")
def update_mobil_by_id(id_mobil: str, mobil_baru: Mobil):
    index = get_mobil_index(id_mobil)
    if index is not None:
        data_mobil[index] = mobil_baru.dict()
        return {"message": "Data mobil berhasil diperbarui."}
    else:
        raise HTTPException(status_code=404, detail="Data mobil tidak ditemukan.")

# Endpoint untuk menghapus data mobil
@app.delete("/mobil/{id_mobil}")
def delete_mobil(id_mobil: str):
    index = get_mobil_index(id_mobil)
    if index is not None:
        del data_mobil[index]
        return {"message": "Data mobil berhasil dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Data mobil tidak ditemukan.")


# Model untuk Data Penyewaan
class Penyewaan(BaseModel):
    id_penyewaan: str
    id_mobil: int
    nomor_pesanan: str
    tanggal_peminjaman: str
    tanggal_pengembalian: str
    durasi_sewa: int

# Dummy data untuk penyewaan
data_penyewaan = [
    {"id_penyewaan": "001", "id_mobil": 1, "nomor_pesanan": "ORD001", "tanggal_peminjaman": "2024-03-20", "tanggal_pengembalian": "2024-03-25", "durasi_sewa": 5},
    {"id_penyewaan": "002", "id_mobil": 2, "nomor_pesanan": "ORD002", "tanggal_peminjaman": "2024-04-10", "tanggal_pengembalian": "2024-04-12", "durasi_sewa": 2},
    {"id_penyewaan": "003", "id_mobil": 3, "nomor_pesanan": "ORD003", "tanggal_peminjaman": "2024-05-01", "tanggal_pengembalian": "2024-05-05", "durasi_sewa": 4},
    {"id_penyewaan": "004", "id_mobil": 4, "nomor_pesanan": "ORD004", "tanggal_peminjaman": "2024-06-15", "tanggal_pengembalian": "2024-06-18", "durasi_sewa": 3},
    {"id_penyewaan": "005", "id_mobil": 5, "nomor_pesanan": "ORD005", "tanggal_peminjaman": "2024-07-20", "tanggal_pengembalian": "2024-07-25", "durasi_sewa": 5}
]

@app.post("/penyewaan")
def tambah_penyewaan(penyewaan: Penyewaan):
    data_penyewaan.append(penyewaan.dict())
    return {"message": "Data penyewaan berhasil ditambahkan."}

@app.get("/penyewaan", response_model=List[Penyewaan])
def get_penyewaan():
    return data_penyewaan

# Model untuk Data Pembayaran
class Pembayaran(BaseModel):
    id_pembayaran: str
    id_penyewaan: str
    metode_pembayaran: str
    tanggal_pembayaran: str
    jumlah_pembayaran: int

# Dummy data untuk pembayaran
data_pembayaran = [
    {"id_pembayaran": "C01", "id_penyewaan": "001", "metode_pembayaran": "Tunai", "tanggal_pembayaran": "2024-03-25", "jumlah_pembayaran": 1500000},
    {"id_pembayaran": "B01", "id_penyewaan": "002", "metode_pembayaran": "Transfer Bank", "tanggal_pembayaran": "2024-04-12", "jumlah_pembayaran": 640000},
    {"id_pembayaran": "K01", "id_penyewaan": "003", "metode_pembayaran": "Kartu Kredit", "tanggal_pembayaran": "2024-05-04", "jumlah_pembayaran": 500000},
    {"id_pembayaran": "C02", "id_penyewaan": "004", "metode_pembayaran": "Tunai", "tanggal_pembayaran": "2024-06-18", "jumlah_pembayaran": 1050000},
    {"id_pembayaran": "B02", "id_penyewaan": "005", "metode_pembayaran": "Transfer Bank", "tanggal_pembayaran": "2024-07-25", "jumlah_pembayaran": 2000000}
]

@app.post("/pembayaran")
def tambah_pembayaran(pembayaran: Pembayaran):
    data_pembayaran.append(pembayaran.dict())
    return {"message": "Data pembayaran berhasil ditambahkan."}

@app.get("/pembayaran", response_model=List[Pembayaran])
def get_pembayaran():
    return data_pembayaran

class Pengembalian(BaseModel):
    id_pengembalian: str
    id_penyewaan: str
    id_pembayaran: str
    kerusakan: str
    total_denda: int

# Dummy data untuk data pengembalian
data_pengembalian = [
    {"id_pengembalian": "201", "id_penyewaan": "001", "id_pembayaran": "C01", "kerusakan": "Ban bocor", "total_denda": 250000},
    {"id_pengembalian": "202", "id_penyewaan": "002", "id_pembayaran": "B01", "kerusakan": "-", "total_denda": 0},
    {"id_pengembalian": "203", "id_penyewaan": "003", "id_pembayaran": "K01", "kerusakan": "-", "total_denda": 0},
    {"id_pengembalian": "204", "id_penyewaan": "004", "id_pembayaran": "C02", "kerusakan": "Aki tidak berfungsi dengan baik", "total_denda": 200000},
    {"id_pengembalian": "205", "id_penyewaan": "005", "id_pembayaran": "B02", "kerusakan": "Pintu mobil bagian kanan terdapat baret", "total_denda": 150000}
]

# Endpoint untuk menambahkan data pengembalian
@app.post("/pengembalian")
def tambah_pengembalian(pengembalian: Pengembalian):
    data_pengembalian.append(pengembalian.dict())
    return {"message": "Data pengembalian berhasil ditambahkan."}

# Endpoint untuk mendapatkan data pengembalian
@app.get("/pengembalian", response_model=List[Pengembalian])
def get_pengembalian():
    return data_pengembalian

def get_pengembalian_index(id_pengembalian):
    for index, pengembalian in enumerate(data_pengembalian):
        if pengembalian['id_pengembalian'] == id_pengembalian:
            return index
    return None

# Endpoint untuk detail get id
@app.get("/pengembalian/{id_pengembalian}", response_model=Optional[Pengembalian])
def get_pengembalian_by_id(id_pengembalian: str):
    for pengembalian in data_pengembalian:
        if pengembalian['id_pengembalian'] == id_pengembalian:
            return Pengembalian(**pengembalian)
    return None

# Endpoint untuk memperbarui data pengembalian dengan hanya memasukkan id_pengembalian
@app.put("/pengembalian/{id_pengembalian}")
def update_pengembalian_by_id(id_pengembalian: str, pengembalian_baru: Pengembalian):
    index = get_pengembalian_index(id_pengembalian)
    if index is not None:
        data_pengembalian[index] = pengembalian_baru.dict()
        return {"message": "Data pengembalian berhasil diperbarui."}
    else:
        raise HTTPException(status_code=404, detail="Data pengembalian tidak ditemukan.")

# Endpoint untuk menghapus data pengembalian
@app.delete("/pengembalian/{id_pengembalian}")
def delete_pengembalian(id_pengembalian: str):
    index = get_pengembalian_index(id_pengembalian)
    if index is not None:
        del data_pengembalian[index]
        return {"message": "Data pengembalian berhasil dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Data pengembalian tidak ditemukan.")

class Pelanggan(BaseModel):
    nomor_telepon: str
    email: str

# Dummy data untuk pelanggan
data_pelanggan = [
    {"nomor_telepon": "555-123-4567", "email": "ale@example.com"},
    {"nomor_telepon": "555-456-7891", "email": "leoo@example.com"},
    {"nomor_telepon": "555-789-1232", "email": "leaaa@example.com"},
    {"nomor_telepon": "555-678-1233", "email": "satoru@example.com"},
    {"nomor_telepon": "555-123-9874", "email": "suguru@example.com"},
]

# Endpoint untuk menambahkan data pelanggan
@app.post("/pelanggan", response_model=Pelanggan)
def tambah_pelanggan(pelanggan: Pelanggan):
    data_pelanggan.append(pelanggan.dict())
    return pelanggan

# Endpoint untuk mendapatkan data pelanggan
@app.get("/pelanggan", response_model=List[Pelanggan])
def get_pelanggan():
    return data_pelanggan

def get_pelanggan_index(nomor_telepon: str):
    for index, pelanggan in enumerate(data_pelanggan):
        if pelanggan['nomor_telepon'] == nomor_telepon:
            return index
    return None

# Endpoint untuk detail pelanggan berdasarkan nomor telepon
@app.get("/pelanggan/{nomor_telepon}", response_model=Pelanggan)
def get_pelanggan_by_telepon(nomor_telepon: str):
    for pelanggan in data_pelanggan:
        if 'nomor_telepon' in pelanggan and pelanggan['nomor_telepon'] == nomor_telepon:
            return Pelanggan(**pelanggan)
        elif 'email' in pelanggan and pelanggan['email'] == nomor_telepon:
            return Pelanggan(**pelanggan)
    raise HTTPException(status_code=404, detail="Data pelanggan tidak ditemukan.")

# Endpoint untuk memperbarui data pelanggan dengan hanya memasukkan nomor telepon
@app.put("/pelanggan/{nomor_telepon}", response_model=Pelanggan)
def update_pelanggan_by_telepon(nomor_telepon: str, pelanggan_baru: Pelanggan):
    index = get_pelanggan_index(nomor_telepon)
    if index is not None:
        data_pelanggan[index] = pelanggan_baru.dict()
        return pelanggan_baru
    else:
        raise HTTPException(status_code=404, detail="Data pelanggan tidak ditemukan.")

# Endpoint untuk menghapus data pelanggan
@app.delete("/pelanggan/{nomor_telepon}")
def delete_pelanggan(nomor_telepon: str):
    index = get_pelanggan_index(nomor_telepon)
    if index is not None:
        del data_pelanggan[index]
        return {"message": "Data pelanggan berhasil dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Data pelanggan tidak ditemukan.")






# Endpoint untuk mendapatkan data penduduk
def get_data_penduduk_from_web():
    url = "https://api-government.onrender.com/penduduk"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data TOUR GUIDE dari web hosting.")

# Model untuk Data Tour Guide
class Penduduk(BaseModel):
    nik: int

# Endpoint untuk mendapatkan data Tour Guide
@app.get("/penduduk", response_model=List[Penduduk])
def get_penduduk():
    data_penduduk = get_data_penduduk_from_web()
    return data_penduduk
