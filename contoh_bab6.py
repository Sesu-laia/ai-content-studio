# =============================================================
# contoh_bab6.py  -  Versi LENGKAP potongan kode BAB VI laporan
# Jalankan dari folder project:  python contoh_bab6.py
# (potongan di laporan tidak bisa jalan sendiri karena tidak
#  ada baris import; file ini sudah lengkap dengan import-nya)
# =============================================================

# --- import: "mengambil" class dari file lain di project ---
from content_pipeline import ContentPipeline           # file content_pipeline.py
from generators.base import ImageGenerator             # file generators/base.py
from generators.mock import MockImageGenerator         # file generators/mock.py
from generators.dalle import DALLEImageGenerator       # file generators/dalle.py
from models.content_project import ContentProject      # file models/content_project.py
from exceptions import PipelineException               # file exceptions.py


print("===== 6.1 & 6.2  CLASS dan OBJECT =====")
pipeline = ContentPipeline(MockImageGenerator())       # buat objek pipeline, provider = Mock (offline)
project1 = pipeline.jalankan("kucing astronot", "anime")     # objek ContentProject ke-1
project2 = pipeline.jalankan("pantai sore", "cinematic")     # objek ContentProject ke-2
print(project1.prompt, "|", project1.gambar_list[0].style)  # state objek 1
print(project2.prompt, "|", project2.gambar_list[0].style)  # state objek 2 (beda)
print("Jumlah project:", len(pipeline.projects))            # 2 objek tersimpan di pipeline


print("\n===== 6.3  PROPERTY (getter, setter, validasi) =====")
print("Prompt lama :", project1.prompt)            # getter -> membaca _prompt
project1.prompt = "kucing astronot di bulan"       # setter -> lolos validasi
print("Prompt baru :", project1.prompt)
try:
    project1.prompt = "   "                        # setter -> prompt kosong ditolak
except PipelineException as e:
    print("Ditolak     :", e)
gambar = project1.gambar_list[0]
print("Biaya USD   :", gambar.biaya)
print("Biaya Rupiah:", gambar.biaya_rupiah)        # property yang dihitung otomatis


print("\n===== 6.4  METHOD (instance, class, static) =====")
print("Static method :", ImageGenerator.prompt_valid("kota futuristik"))  # True
print("Static method :", ImageGenerator.prompt_valid(""))                 # False
print("Class method  :", ImageGenerator.daftar_style())                  # daftar style


print("\n===== 6.5  INHERITANCE =====")
mock = MockImageGenerator()
print("Mock turunan ImageGenerator? ", isinstance(mock, ImageGenerator))  # True
print("Method warisan _build_full_prompt():")
print("  ", mock._build_full_prompt("gunung bersalju", "realistis"))


print("\n===== 6.6  POLYMORPHISM =====")
# method yang sama (generate) dipanggil, hasilnya beda tergantung objeknya
for generator in [MockImageGenerator(), DALLEImageGenerator()]:
    try:
        hasil = generator.generate("gunung bersalju", "realistis")
        print(generator.nama_provider, "->", hasil.url)
    except PipelineException as e:
        print(generator.nama_provider, "->", e)
# (Pollinations tidak dimasukkan di sini supaya tidak perlu internet & menunggu 15 detik;
#  coba lewat menu 2 di main.py)
