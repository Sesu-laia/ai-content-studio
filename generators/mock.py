# MOCK IMAGE GENERATOR (Fitur 3)
# Mode offline tanpa API key, dipakai untuk demo.
from config import HARGA_DALLE_PER_GAMBAR
from exceptions import PipelineException
from generators.base import ImageGenerator
from models.generated_image import GeneratedImage


class MockImageGenerator(ImageGenerator):
    nama_provider = "mock"
    # Biaya SIMULASI (setara DALL-E) supaya estimasi biaya bisa didemokan.
    # Mode mock tidak memanggil API, jadi tidak ada tagihan sungguhan.
    biaya_per_gambar = HARGA_DALLE_PER_GAMBAR

    def __init__(self, gagal=False):
        # gagal=True dipakai untuk mensimulasikan API error (demo exception)
        self.gagal = gagal
        self._counter = 0

    def generate(self, prompt, style="realistis"):
        full_prompt = self._build_full_prompt(prompt, style)
        if self.gagal:
            raise PipelineException("IMAGE_GEN", "Simulasi gagal: server mock sedang error")
        self._counter += 1
        return GeneratedImage(
            url=f"mock://image/{self._counter:03d}.png",
            prompt=full_prompt,
            style=style,
            provider=self.nama_provider,
            biaya=self.biaya_per_gambar,
        )
