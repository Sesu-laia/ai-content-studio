# GENERATED IMAGE (Fitur 6)
# Menyimpan data satu gambar hasil generate.
from dataclasses import dataclass, field
from datetime import datetime

from config import KURS_USD_KE_IDR


@dataclass
class GeneratedImage:
    url: str
    prompt: str
    style: str
    provider: str
    biaya: float
    dibuat_pada: datetime = field(default_factory=datetime.now)

    # PROPERTY (read-only): biaya dalam Rupiah dihitung dari biaya USD
    @property
    def biaya_rupiah(self):
        return self.biaya * KURS_USD_KE_IDR

    def to_dict(self):
        """Mengubah objek menjadi dictionary (dipakai saat ekspor ke JSON)."""
        return {
            "url": self.url,
            "prompt": self.prompt,
            "style": self.style,
            "provider": self.provider,
            "biaya": self.biaya,
            "dibuat_pada": self.dibuat_pada.isoformat(timespec="seconds"),
        }
