# CONTENT PIPELINE (Fitur 9)
# Pengatur alur pembuatan konten. Di tahap UTS baru Tahap 1: teks -> gambar.
# Pipeline tidak peduli generatornya DALL-E atau Mock, cukup
# memanggil generate() (POLYMORPHISM).
from models.content_project import ContentProject


class ContentPipeline:
    def __init__(self, image_generator):
        self.image_generator = image_generator
        self._projects = []

    # PROPERTY read-only: daftar project tidak bisa ditimpa dari luar
    @property
    def projects(self):
        return list(self._projects)

    # Fitur 9: Tahap 1, generate gambar dari prompt
    def jalankan(self, prompt, style="realistis"):
        # Generate dulu: jika gagal, project tidak ikut dibuat/disimpan
        gambar = self.image_generator.generate(prompt, style)
        project = ContentProject(prompt)
        project.tambah_gambar(gambar)
        self._projects.append(project)
        return project

    # Menambah gambar baru (style lain) ke project yang sudah ada
    def tambah_gambar_ke(self, project, style):
        gambar = self.image_generator.generate(project.prompt, style)
        project.tambah_gambar(gambar)
        return gambar
