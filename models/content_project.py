# CONTENT PROJECT (Fitur 7 dan 8)
# Satu project = satu prompt, berisi daftar gambar dan daftar video.
# video_list masih kosong di tahap UTS, diisi di Tahap 2 (UAS).
from exceptions import PipelineException


class ContentProject:
    def __init__(self, prompt):
        self.prompt = prompt
        self.gambar_list = []
        self.video_list = []

    def tambah_gambar(self, gambar):
        self.gambar_list.append(gambar)

    # Fitur 8: memilih gambar yang nanti akan dijadikan video
    def pilih_untuk_video(self, idx):
        if not self.gambar_list:
            raise PipelineException("PILIH_GAMBAR", "Project belum punya gambar")
        if not isinstance(idx, int) or idx < 0 or idx >= len(self.gambar_list):
            raise PipelineException(
                "PILIH_GAMBAR",
                f"Indeks {idx} tidak valid, pilih 0 sampai {len(self.gambar_list) - 1}",
            )
        return self.gambar_list[idx]
