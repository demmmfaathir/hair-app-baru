# Klasifikasi Jenis Rambut Berbasis CNN dengan Rekomendasi Perawatan Berbasis Aturan

Aplikasi web yang mengklasifikasikan foto rambut ke empat kelas (`straight`, `wavy`, `curly`, `kinky`) dengan CNN
(EfficientNetB0, transfer learning), lalu meneruskan hasilnya ke rule-based system untuk rekomendasi perawatan.
Sistem ini alat bantu, bukan pengganti diagnosis ahli.

- Backend: FastAPI + Uvicorn (Python 3.11), model `.keras`, validasi foto dengan CLIP, aturan perawatan di `rules.py`
- Frontend: Flutter Web
- Container: Docker (hanya backend)

## Struktur repository

```
hair-app-baru/
├── backend/
│   ├── main.py              # API FastAPI (/predict, /health)
│   ├── rules.py             # basis aturan rekomendasi perawatan
│   ├── requirements.txt     # dependency dengan versi dipin
│   ├── Dockerfile
│   ├── .dockerignore
│   └── model/
│       ├── hair_EfficientNetB0.keras
│       └── class_names.json
└── frontend/                # proyek Flutter
```

## Menjalankan backend dengan Docker

Prasyarat: Docker Desktop. Folder aktif: `backend/`.

```bash
docker build -t hair-backend .
docker run -d -p 8000:8000 --name hair-backend hair-backend
```

- Build pertama mengunduh model CLIP satu kali (disimpan di dalam image), jadi butuh internet dan waktu beberapa menit.
- Tunggu sampai log menampilkan `Application startup complete` (`docker logs hair-backend`).
- Dokumentasi API interaktif: http://localhost:8000/docs
- Kebutuhan memori: pada pengujian, penggunaan RAM saat idle sekitar 815 MiB. Dengan batas 512 MB tanpa swap,
  proses terhenti saat memuat model, jadi sediakan **minimal 1 GB, disarankan 2 GB atau lebih**.

Berhenti dan hapus container:

```bash
docker rm -f hair-backend
```

## Menjalankan frontend (Flutter Web)

Prasyarat: Flutter SDK. Folder aktif: `frontend/`.

Alamat backend dibaca dari variabel `API_URL` saat build atau run. Jika tidak diisi, nilai bawaannya
`http://127.0.0.1:8001`, jadi untuk backend Docker di atas isi `API_URL` dengan port 8000.

Mode pengembangan:

```bash
flutter pub get
flutter run -d chrome --dart-define=API_URL=http://127.0.0.1:8000
```

Build rilis (hasil di `build/web`):

```bash
flutter build web --release --dart-define=API_URL=http://127.0.0.1:8000
```

## API

### `GET /health`

Pemeriksaan status layanan.

### `POST /predict`

`multipart/form-data`

| Field | Tipe | Keterangan |
|---|---|---|
| `file` | berkas gambar (wajib) | foto rambut (JPEG/PNG) |
| `scalp` | string | kondisi kulit kepala (opsional) |
| `condition` | string | kondisi rambut (opsional) |
| `complaints` | string | keluhan (opsional) |

Contoh:

```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@kinky.jpg;type=image/jpeg" \
  -F "scalp=Normal" \
  -F "condition=Normal" \
  -F "complaints="
```

Respons JSON memuat antara lain `label`, `label_id`, `confidence`, `low_confidence`, `gate_score`,
`probs` (probabilitas keempat kelas), dan `inputs` (masukan pengguna), beserta rekomendasi perawatan.
Bila keyakinan prediksi di bawah 0,80, sistem menandai hasil sebagai kurang jelas dan tidak memberi rekomendasi.

## Batasan

- Data uji berjumlah 209 citra dan isi rekomendasi belum divalidasi oleh pakar (lihat bagian keterbatasan pada naskah).
- Backend memuat model CNN dan CLIP saat startup, sehingga permintaan pertama setelah container hidup bisa lebih lambat.
- Demo publik dijalankan dari mesin lokal melalui tunnel sementara, sehingga tautannya hanya aktif selama sesi demo.

## Pemecahan masalah

| Gejala | Penyebab umum | Solusi |
|---|---|---|
| Container berhenti atau status `Exited (137)` | RAM tidak cukup | naikkan batas memori (minimal 1 GB) |
| Frontend tidak menampilkan hasil | `API_URL` salah atau backend belum siap | cek `docker logs hair-backend` dan alamat `API_URL` |
| Error CORS di browser | backend tidak terjangkau dari alamat frontend | pastikan backend berjalan dan alamatnya benar |

## Tim
- Muhammad Abi Raffi
- Muhammad Faathir
- Nova Aiza Ilham
