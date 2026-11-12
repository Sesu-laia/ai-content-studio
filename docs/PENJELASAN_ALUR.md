# Penjelasan Alur & Persiapan Tanya Jawab (UTS)

## 1. Gambaran Besar

```
main.py (CLI)
   │
   ▼
ContentPipeline ──memakai──► ImageGenerator (abstract)
   │                             ├── DALLEImageGenerator  (berbayar, butuh API key)
   │                             └── MockImageGenerator   (offline, untuk demo)
   ▼
ContentProject ──berisi──► GeneratedImage (gambar_list)
```

## 2. Alur Generate Gambar
Contoh: `pipeline.jalankan("kucing", "anime")`

| Langkah | Terjadi di | Hasil |
|---|---|---|
| 1 | `ContentPipeline.jalankan()` memanggil `self.image_generator.generate("kucing", "anime")` | |
| 2 | `generate()` memanggil `_build_full_prompt()` dari kelas induk | `"kucing, anime style, vibrant colors, clean line art"` |
| 3 | Mock membuat url `mock://image/001.png` (DALL-E memanggil API) | |
| 4 | Mengembalikan objek `GeneratedImage` | |
| 5 | Baru setelah generate berhasil, `jalankan()` membuat `ContentProject("kucing")` | project kosong |
| 6 | `project.tambah_gambar(gambar)` | `gambar_list` berisi 1 |
| 7 | Project disimpan ke `pipeline.projects` lalu dikembalikan | |
| 8 | `main.py` mencetak info gambar + estimasi biaya | tampilan CLI |

Generate dijalankan lebih dulu (`content_pipeline.py`, method `jalankan()`): kalau generate gagal,
exception langsung keluar dari method, sehingga project kosong tidak ikut tersimpan.

## 3. Alur DALL-E (hanya jika API key tersedia)
1. `_build_full_prompt()` → `"kucing, anime style, vibrant colors, clean line art"`
2. Cek `self.api_key`. Kalau kosong → `PipelineException("IMAGE_GEN", "OPENAI_API_KEY belum diatur")`
3. Data request (model, prompt, jumlah, ukuran) diubah ke JSON
4. Request POST ke `https://api.openai.com/v1/images/generations` dengan header `Authorization: Bearer <api key>`
5. Respons JSON dibaca, url gambar diambil dari `data["data"][0]["url"]`
6. HTTP error, koneksi gagal, atau format respons salah → diubah menjadi `PipelineException`
7. Mengembalikan `GeneratedImage` dengan `url` = alamat gambar dari OpenAI

## 4. Alur Exception
Error dibungkus `PipelineException(tahap, alasan)`, jadi pesan selalu menunjukkan **tahap** terjadinya masalah:

| Tahap | Penyebab | Dicek di |
|---|---|---|
| `IMAGE_GEN` | prompt kosong / style tidak dikenal | `_build_full_prompt()` |
| `IMAGE_GEN` | API key kosong, HTTP error, koneksi gagal, format respons salah | `DALLEImageGenerator.generate()` |
| `IMAGE_GEN` | mock disuruh gagal (`gagal=True`) | `MockImageGenerator.generate()` |
| `PROJECT` | prompt project kosong / belum ada project | `ContentProject` (setter `prompt`), `main.py` |
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

**Kenapa project dibuat setelah generate, bukan sebelumnya?**
Lihat `ContentPipeline.jalankan()`: baris `generate()` ada di atas baris `ContentProject(prompt)`. Kalau generate gagal, exception langsung keluar, jadi tidak ada project kosong yang tersimpan di `pipeline.projects`.

**Kenapa demo memakai Mock, bukan DALL-E?**
DALL-E berbayar dan butuh API key. Di lokal kami memakai data Mock; DALL-E baru dipakai saat API key tersedia.

**Dari mana program tahu harus pakai Mock atau DALL-E?**
Dari fungsi `generator_otomatis()` di `main.py`. Fungsi itu membaca `os.environ.get("OPENAI_API_KEY")`: kalau ada isinya, mengembalikan `DALLEImageGenerator()`; kalau tidak, `MockImageGenerator()`. Hasilnya diberikan ke `ContentPipeline(...)` di awal `menu()`. Karena keduanya turunan `ImageGenerator`, `ContentPipeline` tidak diubah sama sekali (polymorphism).

**Kalau DALL-E dipilih tapi API key tidak ada?**
`DALLEImageGenerator.generate()` mengecek `self.api_key` sebelum memanggil API. Kalau kosong, raise `PipelineException("IMAGE_GEN", "OPENAI_API_KEY belum diatur")`, ditangkap di `main.py`, dan program kembali ke menu.

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
