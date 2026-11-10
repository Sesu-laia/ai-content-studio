# KONFIGURASI UMUM
# Harga dalam USD per gambar. Ini ESTIMASI, cek harga terbaru di situs resmi.
HARGA_DALLE_PER_GAMBAR = 0.04          # DALL-E 3, 1024x1024, standard

# Kurs untuk menampilkan perkiraan biaya dalam Rupiah
KURS_USD_KE_IDR = 16000


def format_biaya(usd):
    """Mengubah biaya USD menjadi teks USD + perkiraan Rupiah."""
    rupiah = usd * KURS_USD_KE_IDR
    return f"${usd:.2f} (~Rp{rupiah:,.0f})".replace(",", ".")


# Pollinations.ai: gratis, tanpa API key (batas 1 request per 15 detik)
HARGA_POLLINATIONS_PER_GAMBAR = 0.0
JEDA_POLLINATIONS = 15

# Folder tempat menyimpan file gambar hasil generate
FOLDER_OUTPUT = "output"
