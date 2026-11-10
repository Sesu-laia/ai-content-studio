# EXCEPTION KHUSUS PROYEK (Fitur 4)
# Setiap error di pipeline dibungkus PipelineException supaya kita tahu
# di TAHAP mana error terjadi (misal IMAGE_GEN, VIDEO_GEN, PILIH_GAMBAR).


class PipelineException(Exception):
    def __init__(self, tahap, alasan):
        self.tahap = tahap
        self.alasan = alasan
        super().__init__(f"[{tahap}] {alasan}")
