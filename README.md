# AI Content Creator Studio – Tahap UTS

Proyek PPBO 2026 – Topik **[I3] AI Content Creator Studio (Teks → Gambar → Video)**.
Tahap UTS mengerjakan **fitur 1–10**: alur **teks (prompt) → gambar**.

Ada 3 provider gambar:
- **pollinations** → menghasilkan **gambar AI sungguhan secara GRATIS** (tanpa API key, butuh internet)
- **dalle** → gambar AI dari OpenAI (berbayar, butuh API key)
- **mock** → mode offline untuk demo cepat, tanpa file gambar

---

## Cara Menjalankan

```bash
python main.py --demo    # demo otomatis
python main.py           # menu interaktif
```

Tidak perlu install library tambahan (hanya Python standar).

### Menghasilkan gambar sungguhan (gratis)
1. Jalankan `python main.py`
2. Menu **1** → ketik `pollinations`
3. Menu **2** → isi prompt dan style
4. File gambar tersimpan di folder `output/`, buka lewat menu **6**

**Jika muncul error `CERTIFICATE_VERIFY_FAILED` (macOS):** jalankan sekali
`open "/Applications/Python 3.13/Install Certificates.command"` (sesuaikan versi Python),
atau `python3 -m pip install --upgrade certifi`. Program otomatis memakai certifi jika terpasang.

Batasan layanan gratis Pollinations: 1 request per 15 detik (program menunggu otomatis),
gambar bisa memakan waktu 10–60 detik, dan kadang ada watermark.

### Memakai DALL-E asli (opsional)
```bash
export OPENAI_API_KEY="..."
```
Lalu pilih provider `dalle` di menu 1. Tanpa API key, DALL-E akan melempar
`PipelineException` dengan pesan yang jelas. **Jangan menulis API key di kode.**

---

## Struktur Folder

```
ai-content-studio-uts/
├── main.py                  # CLI (menu interaktif + demo)
├── config.py                # harga & kurs
├── exceptions.py            # PipelineException
├── content_pipeline.py      # ContentPipeline (Tahap 1)
├── ssl_helper.py            # sertifikat SSL (fix error macOS)
├── generators/
│   ├── base.py              # ImageGenerator (Abstract Base Class)
│   ├── dalle.py             # DALLEImageGenerator
│   ├── pollinations.py      # PollinationsImageGenerator (gratis)
│   └── mock.py              # MockImageGenerator
├── output/                  # file gambar hasil generate
├── models/
│   ├── generated_image.py   # GeneratedImage
│   └── content_project.py   # ContentProject
└── docs/
    ├── class_diagram.png    # Class diagram UML
    └── PENJELASAN_ALUR.md   # alur program & persiapan tanya jawab
```

---

## Fitur UTS (1–10)

| No | Fitur | Lokasi |
|---|---|---|
| 1 | `ImageGenerator` sebagai Abstract Base Class | `generators/base.py` |
| 2 | `DALLEImageGenerator` extends `ImageGenerator`, implement `generate()` (+ tambahan: `PollinationsImageGenerator` gratis) | `generators/dalle.py`, `generators/pollinations.py` |
| 3 | `MockImageGenerator`: mode offline tanpa API key | `generators/mock.py` |
| 4 | Raise `PipelineException('IMAGE_GEN', alasan)` jika gagal | `exceptions.py` |
| 5 | `_build_full_prompt()`: gabungkan prompt + style modifier | `generators/base.py` |
| 6 | `GeneratedImage`: simpan url, prompt, style, provider, biaya | `models/generated_image.py` |
| 7 | `ContentProject`: tampung `gambar_list` & `video_list` | `models/content_project.py` |
| 8 | `project.pilih_untuk_video(idx)` | `models/content_project.py` |
| 9 | `ContentPipeline.jalankan()`: Tahap 1 generate gambar | `content_pipeline.py` |
| 10 | Tampilkan info gambar hasil & estimasi biaya (CLI) | `main.py` |

## Konsep OOP Wajib UTS

| Konsep | Penerapan |
|---|---|
| **Inheritance / ABC** | `ImageGenerator` (abstract) → `DALLEImageGenerator`, `PollinationsImageGenerator`, `MockImageGenerator` · `PipelineException` → turunan `Exception` |
| **Polymorphism** | `ContentPipeline.jalankan()` cukup memanggil `generate()`; hasilnya berbeda tergantung generator yang dipakai (Mock / DALL-E / Pollinations) |
| **Exception Handling** | `PipelineException(tahap, alasan)` untuk prompt kosong, style salah, API key kosong, HTTP error, koneksi gagal, timeout, batas request (HTTP 429), respons bukan gambar, indeks gambar salah, provider tidak ada. Semua ditangkap di CLI sehingga program tidak berhenti |

---

## Catatan
- Pollinations.ai adalah layanan gratis pihak ketiga; aturannya bisa berubah sewaktu-waktu. Jika gagal, ganti ke provider `mock`.
- Harga di `config.py` adalah **estimasi**; cek harga terbaru di situs resmi OpenAI.
- Mode Mock memakai **biaya simulasi** (setara DALL-E) supaya estimasi biaya bisa didemokan. Tidak ada tagihan sungguhan.
- `video_list` di `ContentProject` sudah disiapkan, dan akan diisi pada Tahap 2 (UAS).
