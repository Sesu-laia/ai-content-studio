# IMAGE GENERATOR - ABSTRACT BASE CLASS (Fitur 1 dan 5)
# Kelas induk untuk semua generator gambar (DALL-E dan Mock).
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

    # STATIC METHOD: fungsi bantu yang tidak butuh self maupun cls
    @staticmethod
    def prompt_valid(prompt):
        return isinstance(prompt, str) and prompt.strip() != ""

    # CLASS METHOD: memakai cls untuk membaca atribut milik kelas
    @classmethod
    def daftar_style(cls):
        return list(cls.STYLE_MODIFIER)

    # Fitur 5: menggabungkan prompt + style modifier
    def _build_full_prompt(self, prompt, style):
        if not self.prompt_valid(prompt):
            raise PipelineException("IMAGE_GEN", "Prompt tidak boleh kosong")
        if style not in self.STYLE_MODIFIER:
            daftar = ", ".join(self.daftar_style())
            raise PipelineException("IMAGE_GEN", f"Style '{style}' tidak dikenal. Pilihan: {daftar}")
        return f"{prompt.strip()}, {self.STYLE_MODIFIER[style]}"

    # Method abstrak: wajib dibuat ulang di setiap kelas turunan (polymorphism)
    @abstractmethod
    def generate(self, prompt, style="realistis"):
        """Mengembalikan objek GeneratedImage."""
        pass
