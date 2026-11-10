# IMAGE GENERATOR - ABSTRACT BASE CLASS (Fitur 1 dan 5)
# Kelas induk untuk semua generator gambar (DALL-E, Stable Diffusion, Mock).
# Setiap kelas turunan WAJIB membuat method generate().
from abc import ABC, abstractmethod

from exceptions import PipelineException


class ImageGenerator(ABC):
    nama_provider = "base"
    biaya_per_gambar = 0.0

    # Kata tambahan yang digabungkan ke prompt sesuai style
    STYLE_MODIFIER = {
        "realistis": "photorealistic, highly detailed, natural lighting",
        "anime": "anime style, vibrant colors, clean line art",
        "kartun": "cartoon style, flat colors, playful",
        "cinematic": "cinematic shot, dramatic lighting, film grain",
    }

    # Fitur 5: menggabungkan prompt + style modifier
    def _build_full_prompt(self, prompt, style):
        if not isinstance(prompt, str) or not prompt.strip():
            raise PipelineException("IMAGE_GEN", "Prompt tidak boleh kosong")
        if style not in self.STYLE_MODIFIER:
            daftar = ", ".join(self.STYLE_MODIFIER)
            raise PipelineException("IMAGE_GEN", f"Style '{style}' tidak dikenal. Pilihan: {daftar}")
        return f"{prompt.strip()}, {self.STYLE_MODIFIER[style]}"

    # Method abstrak: wajib dibuat ulang di setiap kelas turunan (polymorphism)
    @abstractmethod
    def generate(self, prompt, style="realistis"):
        """Mengembalikan objek GeneratedImage."""
        pass
