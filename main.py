# AI CONTENT CREATOR STUDIO - TAHAP UTS - ANTARMUKA CLI (Fitur 10)
# Jalankan:  python main.py          -> menu interaktif
#            python main.py --demo   -> demo otomatis (mode Mock, tanpa API key)
import os
import sys

from config import format_biaya
from content_pipeline import ContentPipeline
from exceptions import PipelineException
from generators.base import ImageGenerator
from generators.dalle import DALLEImageGenerator
from generators.mock import MockImageGenerator

# Daftar provider gambar yang bisa dipilih user
PROVIDER_GAMBAR = {
    "mock": MockImageGenerator,
    "dalle": DALLEImageGenerator,
}


# Arahan dosen: di lokal pakai data Mock, DALL-E baru dipakai saat API key tersedia.
# Karena keduanya turunan ImageGenerator, pipeline tidak perlu tahu mana yang dipilih.
def generator_otomatis():
    if os.environ.get("OPENAI_API_KEY"):
        return DALLEImageGenerator()
    return MockImageGenerator()


# Fitur 10: menampilkan info gambar hasil + estimasi biaya
def tampilkan_project(project, nomor=None):
    judul = f"PROJECT {nomor}" if nomor else "PROJECT"
    print(f"\n----- {judul}: \"{project.prompt}\" -----")
    for i, g in enumerate(project.gambar_list):
        print(f"  Gambar [{i}] {g.url}")
        print(f"      style    : {g.style}")
        print(f"      provider : {g.provider}")
        print(f"      prompt   : {g.prompt}")
        print(f"      biaya    : {format_biaya(g.biaya)}")
    total = sum(g.biaya for g in project.gambar_list)
    print(f"  Estimasi biaya project: {format_biaya(total)}")


def project_terakhir(pipeline):
    if not pipeline.projects:
        raise PipelineException("PROJECT", "Belum ada project, generate gambar dulu")
    return pipeline.projects[-1]


def demo():
    print("=" * 60)
    print("  AI CONTENT CREATOR STUDIO - DEMO UTS (MODE MOCK)")
    print("=" * 60)

    pipeline = ContentPipeline(MockImageGenerator())

    print("\n[1] Tahap 1: teks -> gambar")
    tampilkan_project(pipeline.jalankan("kucing astronot di bulan", "anime"))

    print("\n[2] Tambah gambar style lain ke project yang sama")
    project = pipeline.jalankan("robot membaca buku", "realistis")
    pipeline.tambah_gambar_ke(project, "kartun")
    tampilkan_project(project)

    print("\n[3] Pilih gambar untuk dijadikan video (Tahap 2 di UAS)")
    terpilih = project.pilih_untuk_video(1)
    print(f"  Gambar terpilih: {terpilih.url} (style {terpilih.style})")

    print("\n[4] Polymorphism: generator berbeda, pemanggilan sama")
    print("    (dalle hanya berhasil jika OPENAI_API_KEY sudah diatur)")
    for nama, kelas in PROVIDER_GAMBAR.items():
        try:
            gambar = kelas().generate("gunung bersalju", "cinematic")
            print(f"  {nama:<12} -> berhasil: {gambar.url}")
        except PipelineException as e:
            print(f"  {nama:<12} -> {e}")

    print("\n[5] Exception handling")
    percobaan = [
        ("Prompt kosong", lambda: pipeline.jalankan("   ", "anime")),
        ("Style tidak dikenal", lambda: pipeline.jalankan("naga", "pixel art")),
        ("Pilih gambar indeks 5", lambda: project.pilih_untuk_video(5)),
        ("Mock disuruh gagal", lambda: MockImageGenerator(gagal=True).generate("naga", "anime")),
    ]
    for judul, aksi in percobaan:
        try:
            aksi()
        except PipelineException as e:
            print(f"  {judul:<23} -> {e}")

    print("\n[6] Semua project")
    for nomor, p in enumerate(pipeline.projects, start=1):
        tampilkan_project(p, nomor)


def menu():
    pipeline = ContentPipeline(generator_otomatis())
    if pipeline.image_generator.nama_provider == "mock":
        print("OPENAI_API_KEY tidak ditemukan -> memakai data Mock (lokal).")
    else:
        print("OPENAI_API_KEY ditemukan -> generate memakai DALL-E.")
    while True:
        print("\n" + "=" * 50)
        print("  AI CONTENT CREATOR STUDIO (UTS)")
        print(f"  Provider gambar: {pipeline.image_generator.nama_provider}")
        print("=" * 50)
        print("1. Pilih provider gambar")
        print("2. Generate gambar (Tahap 1)")
        print("3. Tambah gambar style lain ke project terakhir")
        print("4. Pilih gambar untuk dijadikan video")
        print("5. Lihat semua project")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        try:
            if pilihan == "1":
                nama = input(f"Provider ({'/'.join(PROVIDER_GAMBAR)}): ").strip()
                if nama not in PROVIDER_GAMBAR:
                    raise PipelineException("PROVIDER", f"Provider '{nama}' tidak tersedia")
                pipeline.image_generator = PROVIDER_GAMBAR[nama]()
                print(f"Provider diganti ke {nama}")
            elif pilihan == "2":
                prompt = input("Prompt: ")
                style = input(f"Style ({'/'.join(ImageGenerator.daftar_style())}): ").strip()
                tampilkan_project(pipeline.jalankan(prompt, style))
            elif pilihan == "3":
                project = project_terakhir(pipeline)
                style = input(f"Style ({'/'.join(ImageGenerator.daftar_style())}): ").strip()
                pipeline.tambah_gambar_ke(project, style)
                tampilkan_project(project)
            elif pilihan == "4":
                project = project_terakhir(pipeline)
                tampilkan_project(project)
                idx = int(input("Indeks gambar: "))
                gambar = project.pilih_untuk_video(idx)
                print(f"Gambar terpilih: {gambar.url} (siap dijadikan video di Tahap 2)")
            elif pilihan == "5":
                if not pipeline.projects:
                    print("Belum ada project.")
                for nomor, p in enumerate(pipeline.projects, start=1):
                    tampilkan_project(p, nomor)
            elif pilihan == "0":
                print("Sampai jumpa!")
                break
            else:
                print("Menu tidak dikenal.")
        except PipelineException as e:
            print(f"[ERROR] {e}")
        except ValueError:
            print("[ERROR] Input harus berupa angka")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        menu()
