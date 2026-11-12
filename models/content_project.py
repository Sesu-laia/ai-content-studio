# CONTENT PROJECT (Fitur 7 dan 8)
# Satu project = satu prompt, berisi daftar gambar dan daftar video.
# video_list masih kosong di tahap UTS, diisi di Tahap 2 (UAS).
from exceptions import PipelineException


class ContentProject:
    def __init__(self, prompt):
        self.prompt = prompt          # lewat setter -> divalidasi
        self._gambar_list = []        # private, dibaca lewat property
        self._video_list = []

    # PROPERTY dengan getter + setter (setter memvalidasi isi prompt)
    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, nilai):
        if not isinstance(nilai, str) or not nilai.strip():
            raise PipelineException("PROJECT", "Prompt project tidak boleh kosong")
        self._prompt = nilai.strip()

    # PROPERTY read-only: list hanya bisa diubah lewat method tambah_gambar()
    @property
    def gambar_list(self):
        return list(self._gambar_list)

    @property
    def video_list(self):
        return list(self._video_list)

    def tambah_gambar(self, gambar):
        self._gambar_list.append(gambar)

    # Fitur 8: memilih gambar yang nanti akan dijadikan video
    def pilih_untuk_video(self, idx):
        if not self._gambar_list:
            raise PipelineException("PILIH_GAMBAR", "Project belum punya gambar")
        if not isinstance(idx, int) or idx < 0 or idx >= len(self._gambar_list):
            raise PipelineException(
                "PILIH_GAMBAR",
                f"Indeks {idx} tidak valid, pilih 0 sampai {len(self._gambar_list) - 1}",
            )
        return self._gambar_list[idx]
