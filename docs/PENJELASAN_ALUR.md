# Penjelasan Alur & Persiapan Tanya Jawab (UTS)

## 1. Gambaran Besar

```
main.py (CLI)
   │
   ▼
ContentPipeline ──memakai──► ImageGenerator (abstract)
   │                             ├── DALLEImageGenerator        (berbayar)
   │                             ├── PollinationsImageGenerator (gratis, gambar asli)
   │                             └── MockImageGenerator         (offline)
   ▼
ContentProject ──berisi──► GeneratedImage (gambar_list)
```

## 2. Alur Generate Gambar
Contoh: `pipeline.jalankan("kucing", "anime")`

| Langkah | Terjadi di | Hasil |
|---|---|---|
| 1 | `ContentPipeline.jalankan()` membuat `ContentProject("kucing")` | project kosong |
| 2 | Memanggil `self.image_generator.generate("kucing", "anime")` | |
| 3 | `generate()` memanggil `_build_full_prompt()` dari kelas induk | `"kucing, anime style, vibrant colors, clean line art"` |
| 4 | Mock membuat url `mock://image/001.png` (DALL-E memanggil API) | |
| 5 | Mengembalikan objek `GeneratedImage` | |
| 6 | `project.tambah_gambar(gambar)` | `gambar_list` berisi 1 |
| 7 | Project disimpan ke `pipeline.projects` lalu dikembalikan | |
| 8 | `main.py` mencetak info gambar + estimasi biaya | tampilan CLI |

## 3. Alur Pollinations (gambar sungguhan)
1. `_build_full_prompt()` → `"kucing, anime style, vibrant colors, clean line art"`
2. `_tunggu_jeda()` → kalau request sebelumnya belum lewat 15 detik, program menunggu dulu
3. Prompt di-encode ke URL (`urllib.parse.quote`), karena spasi dan koma tidak boleh langsung masuk URL
4. Request GET ke `https://image.pollinations.ai/prompt/...`
5. Cek `Content-Type` harus `image/...` (bukan halaman error)
6. Isi gambar ditulis ke `output/pollinations_<tanggal>_<jam>.jpg`
7. Mengembalikan `GeneratedImage` dengan `url` = path file tersebut

## 4. Alur Exception
Error dibungkus `PipelineException(tahap, alasan)`, jadi pesan selalu menunjukkan **tahap** terjadinya masalah:

| Tahap | Penyebab | Dicek di |
|---|---|---|
| `IMAGE_GEN` | prompt kosong / style tidak dikenal | `_build_full_prompt()` |
| `IMAGE_GEN` | API key kosong, HTTP error, koneksi gagal | `DALLEImageGenerator.generate()` |
| `IMAGE_GEN` | koneksi gagal, timeout, HTTP 429 (terlalu banyak request), respons bukan gambar | `PollinationsImageGenerator.generate()` |
| `BUKA_GAMBAR` | mencoba membuka gambar hasil mock (bukan file asli) | `main.py` menu 6 |
| `PILIH_GAMBAR` | project kosong / indeks di luar jangkauan | `pilih_untuk_video()` |
| `PROVIDER` | nama provider tidak ada | `main.py` menu 1 |

Di `main.py` setiap menu dibungkus `try ... except PipelineException`, sehingga program **tidak berhenti** walaupun ada error.

---

## 5. Pertanyaan yang Mungkin Ditanya Dosen / Asdos

**Kenapa `ImageGenerator` dibuat abstract?**
Supaya setiap provider WAJIB punya method `generate()`. `ImageGenerator` sendiri tidak bisa dibuat objeknya (muncul `TypeError`).

**Di mana inheritance-nya?**
`DALLEImageGenerator` dan `MockImageGenerator` mewarisi `ImageGenerator`, sehingga keduanya otomatis punya `_build_full_prompt()` dan `STYLE_MODIFIER` tanpa menulis ulang.

**Di mana polymorphism-nya?**
Di `ContentPipeline.jalankan()`: kodenya hanya `self.image_generator.generate(...)`. Kalau generatornya Mock, hasilnya url mock. Kalau DALL-E, memanggil API. Nama method sama, perilakunya berbeda. Ini juga terlihat di demo bagian [4].

**`_build_full_prompt` kenapa pakai garis bawah?**
Tanda method internal (protected): dipakai oleh kelas turunan, bukan dipanggil langsung dari luar kelas.

**Kenapa membuat exception sendiri (`PipelineException`)?**
Supaya pesan error menyebutkan tahap terjadinya masalah (`IMAGE_GEN`, `PILIH_GAMBAR`, ...). Ini memudahkan mencari sumber error, terutama nanti saat pipeline punya 2 tahap (gambar dan video).

**Kenapa memakai Pollinations?**
Karena DALL-E berbayar. Pollinations gratis dan tanpa API key, jadi kami tetap bisa menghasilkan gambar AI sungguhan. Karena ia turunan `ImageGenerator`, `ContentPipeline` tidak perlu diubah sama sekali.

**Kenapa harus menunggu 15 detik?**
Itu batas layanan gratis Pollinations. `_waktu_terakhir` disimpan sebagai atribut kelas (bukan atribut objek), jadi berlaku untuk semua objek Pollinations. Kalau tetap kena batas, server membalas HTTP 429 dan kami ubah menjadi `PipelineException`.

**Kenapa cek `Content-Type`?**
Kadang server membalas halaman error (HTML) dengan status sukses. Kalau tidak dicek, file `.jpg` yang tersimpan sebenarnya rusak.

**Kenapa prompt harus di-`quote()`?**
Prompt dimasukkan ke URL. Spasi dan simbol seperti koma harus diubah ke format URL (`%20`, `%2C`), kalau tidak URL-nya tidak valid.

**Kenapa ada Mock?**
Supaya program bisa didemokan tanpa API key dan tanpa biaya. Mock juga bisa disuruh gagal (`gagal=True`) untuk menunjukkan exception handling.

**Biaya di mode Mock dari mana?**
Biaya simulasi dari `config.py` (setara harga DALL-E), supaya fitur estimasi biaya tetap bisa ditunjukkan.

**Kenapa API key tidak ditulis di kode?**
Karena kode di-push ke GitHub. API key yang bocor bisa dipakai orang lain dan saldo kita yang tertagih. Jadi dibaca dari environment variable `OPENAI_API_KEY`.

**`video_list` kenapa kosong?**
Disiapkan untuk Tahap 2 (UAS): gambar yang dipilih lewat `pilih_untuk_video()` nantinya diubah menjadi video.

**Kalau mau menambah provider baru?**
Buat kelas baru turunan `ImageGenerator` dengan method `generate()`, lalu tambahkan ke dictionary `PROVIDER_GAMBAR` di `main.py`. `ContentPipeline` tidak perlu diubah.
