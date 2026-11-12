# AI Content Creator Studio – Tahap UTS

Proyek PPBO 2026 – Topik **[I3] AI Content Creator Studio (Teks → Gambar → Video)**.
Tahap UTS mengerjakan **fitur 1–10**: alur **teks (prompt) → gambar**.

Ada 2 provider gambar:
- **mock** → mode offline tanpa API key, dipakai untuk demo di lokal
- **dalle** → gambar AI dari OpenAI (berbayar), hanya dipakai jika API key tersedia

---

## Cara Menjalankan

```bash
python main.py --demo    # demo otomatis
python main.py           # menu interaktif
```

Tidak perlu install library tambahan (hanya Python standar).

### Pemilihan provider otomatis
Saat `python main.py` dijalankan, program mengecek environment variable `OPENAI_API_KEY`
(fungsi `generator_otomatis()` di `main.py`):
- **tidak ada API key** → memakai data **Mock** (lokal)
- **ada API key** → generate memakai **DALL-E**

```bash
export OPENAI_API_KEY="..."   # hanya jika punya API key
python main.py
```
Provider tetap bisa diganti manual lewat menu 1. Jika `dalle` dipilih tanpa API key, program
melempar `PipelineException` dengan pesan yang jelas. **Jangan menulis API key di kode.**
`python main.py --demo` selalu memakai Mock.

**Jika muncul error `CERTIFICATE_VERIFY_FAILED` (macOS):** jalankan sekali
`open "/Applications/Python 3.13/Install Certificates.command"` (sesuaikan versi Python),
atau `python3 -m pip install --upgrade certifi`. Program otomatis memakai certifi jika terpasang.

---

## Struktur Folder

```
ai-content-studio/
├── main.py                  # CLI (menu interaktif + demo)
├── contoh_bab6.py           # contoh kode BAB VI laporan (bisa dijalankan)
├── config.py                # harga & kurs
├── exceptions.py            # PipelineException
├── content_pipeline.py      # ContentPipeline (Tahap 1)
├── ssl_helper.py            # sertifikat SSL (fix error macOS)
├── generators/
│   ├── base.py              # ImageGenerator (Abstract Base Class)
│   ├── dalle.py             # DALLEImageGenerator
│   └── mock.py              # MockImageGenerator
├── models/
│   ├── generated_image.py   # GeneratedImage
│   └── content_project.py   # ContentProject
└── docs/
    ├── class_diagram.png    # Class diagram UML
    ├── diagrams/            # use case & activity diagram
    └── PENJELASAN_ALUR.md   # alur program & persiapan tanya jawab
```

---

## Fitur UTS (1–10)

| No | Fitur | Lokasi |
|---|---|---|
| 1 | `ImageGenerator` sebagai Abstract Base Class | `generators/base.py` |
| 2 | `DALLEImageGenerator` extends `ImageGenerator`, implement `generate()` | `generators/dalle.py` |
| 3 | `MockImageGenerator`: mode offline tanpa API key | `generators/mock.py` |
| 4 | Raise `PipelineException('IMAGE_GEN', alasan)` jika gagal | `exceptions.py`, `generators/` |
| 5 | `_build_full_prompt()`: gabungkan prompt + style modifier | `generators/base.py` |
| 6 | `GeneratedImage`: simpan url, prompt, style, provider, biaya | `models/generated_image.py` |
| 7 | `ContentProject`: tampung `gambar_list` & `video_list` | `models/content_project.py` |
| 8 | `project.pilih_untuk_video(idx)` | `models/content_project.py` |
| 9 | `ContentPipeline.jalankan()`: Tahap 1 generate gambar | `content_pipeline.py` |
| 10 | Tampilkan info gambar hasil & estimasi biaya (CLI) | `main.py` |

## Konsep OOP Wajib UTS

| Konsep | Penerapan |
|---|---|
| **Inheritance / ABC** | `ImageGenerator` (abstract) → `DALLEImageGenerator`, `MockImageGenerator` · `PipelineException` → turunan `Exception` |
| **Polymorphism** | `ContentPipeline.jalankan()` cukup memanggil `generate()`; hasilnya berbeda tergantung generator yang dipakai (Mock / DALL-E) |
| **Exception Handling** | `PipelineException(tahap, alasan)` untuk prompt kosong, style salah, API key kosong, HTTP error, koneksi gagal, format respons salah, indeks gambar salah, provider tidak ada. Semua ditangkap di CLI sehingga program tidak berhenti |

---

## Catatan
- Harga di `config.py` adalah **estimasi**; cek harga terbaru di situs resmi OpenAI.
- Mode Mock memakai **biaya simulasi** (setara DALL-E) supaya estimasi biaya bisa didemokan. Tidak ada tagihan sungguhan.
- `video_list` di `ContentProject` sudah disiapkan, dan akan diisi pada Tahap 2 (UAS).
