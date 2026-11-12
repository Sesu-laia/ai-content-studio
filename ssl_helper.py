# SSL HELPER
# Di macOS (Python dari python.org) sertifikat SSL kadang belum terpasang,
# sehingga muncul error CERTIFICATE_VERIFY_FAILED. Jika library certifi
# terpasang, sertifikat dari certifi dipakai. Verifikasi SSL TETAP aktif.
import ssl


def buat_ssl_context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()
