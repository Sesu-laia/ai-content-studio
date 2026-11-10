# POLLINATIONS IMAGE GENERATOR (provider GRATIS, tanpa API key)
# Menghasilkan gambar AI sungguhan lewat Pollinations.ai, lalu menyimpannya
# sebagai file .jpg di folder output.
# Batasan layanan gratis: 1 request per 15 detik, gambar bisa ada watermark.
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from config import FOLDER_OUTPUT, HARGA_POLLINATIONS_PER_GAMBAR, JEDA_POLLINATIONS
from exceptions import PipelineException
from generators.base import ImageGenerator
from models.generated_image import GeneratedImage


class PollinationsImageGenerator(ImageGenerator):
    nama_provider = "pollinations"
    biaya_per_gambar = HARGA_POLLINATIONS_PER_GAMBAR
    URL_API = "https://image.pollinations.ai/prompt/"

    # Waktu request terakhir, dipakai bersama oleh semua objek kelas ini
    _waktu_terakhir = 0.0

    def __init__(self, lebar=768, tinggi=768, timeout=120):
        self.lebar = lebar
        self.tinggi = tinggi
        self.timeout = timeout

    def _tunggu_jeda(self):
        """Menunggu jika request sebelumnya belum lewat 15 detik (batas layanan gratis)."""
        selisih = time.time() - PollinationsImageGenerator._waktu_terakhir
        if selisih < JEDA_POLLINATIONS:
            sisa = JEDA_POLLINATIONS - selisih
            print(f"  (menunggu {sisa:.0f} detik, batas layanan gratis Pollinations)")
            time.sleep(sisa)

    def generate(self, prompt, style="realistis"):
        full_prompt = self._build_full_prompt(prompt, style)
        self._tunggu_jeda()

        # Prompt dimasukkan ke URL, jadi spasi dan simbol harus di-encode
        parameter = urllib.parse.urlencode({
            "width": self.lebar,
            "height": self.tinggi,
            "nologo": "true",
        })
        url = self.URL_API + urllib.parse.quote(full_prompt) + "?" + parameter
        request = urllib.request.Request(url, headers={"User-Agent": "AIContentStudio/1.0"})

        try:
            PollinationsImageGenerator._waktu_terakhir = time.time()
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                jenis = response.headers.get("Content-Type", "")
                isi_gambar = response.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                raise PipelineException("IMAGE_GEN", "Terlalu banyak request, tunggu 15 detik lalu coba lagi")
            raise PipelineException("IMAGE_GEN", f"Pollinations error HTTP {e.code}")
        except urllib.error.URLError as e:
            raise PipelineException("IMAGE_GEN", f"Tidak bisa terhubung ke Pollinations: {e.reason}")
        except TimeoutError:
            raise PipelineException("IMAGE_GEN", f"Timeout: gambar belum selesai setelah {self.timeout} detik")

        # Pastikan yang diterima benar-benar gambar, bukan halaman error
        if not jenis.startswith("image/") or not isi_gambar:
            raise PipelineException("IMAGE_GEN", f"Respons bukan gambar (Content-Type: {jenis or '-'})")

        os.makedirs(FOLDER_OUTPUT, exist_ok=True)
        nama_file = f"pollinations_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
        path = os.path.join(FOLDER_OUTPUT, nama_file)
        with open(path, "wb") as f:
            f.write(isi_gambar)

        return GeneratedImage(path, full_prompt, style, self.nama_provider, self.biaya_per_gambar)
