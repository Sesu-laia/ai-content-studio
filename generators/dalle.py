# DALL-E IMAGE GENERATOR (Fitur 2)
# Memanggil OpenAI Images API. API key dibaca dari environment variable
# OPENAI_API_KEY supaya tidak tersimpan di kode / GitHub.
import json
import os
import urllib.error
import urllib.request

from config import HARGA_DALLE_PER_GAMBAR
from exceptions import PipelineException
from ssl_helper import buat_ssl_context
from generators.base import ImageGenerator
from models.generated_image import GeneratedImage


class DALLEImageGenerator(ImageGenerator):
    nama_provider = "dalle"
    biaya_per_gambar = HARGA_DALLE_PER_GAMBAR
    URL_API = "https://api.openai.com/v1/images/generations"

    def __init__(self, api_key=None, timeout=60):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.timeout = timeout

    def generate(self, prompt, style="realistis"):
        full_prompt = self._build_full_prompt(prompt, style)
        if not self.api_key:
            raise PipelineException("IMAGE_GEN", "OPENAI_API_KEY belum diatur")

        body = json.dumps({
            "model": "dall-e-3",
            "prompt": full_prompt,
            "n": 1,
            "size": "1024x1024",
        }).encode("utf-8")
        request = urllib.request.Request(
            self.URL_API,
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout, context=buat_ssl_context()) as response:
                data = json.loads(response.read().decode("utf-8"))
            url = data["data"][0]["url"]
        except urllib.error.HTTPError as e:
            raise PipelineException("IMAGE_GEN", f"DALL-E error HTTP {e.code}")
        except urllib.error.URLError as e:
            raise PipelineException("IMAGE_GEN", f"Tidak bisa terhubung ke DALL-E: {e.reason}")
        except (KeyError, IndexError, json.JSONDecodeError):
            raise PipelineException("IMAGE_GEN", "Format respons DALL-E tidak dikenali")

        return GeneratedImage(url, full_prompt, style, self.nama_provider, self.biaya_per_gambar)
