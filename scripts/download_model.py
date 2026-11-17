import urllib.request
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models" / "all-MiniLM-L6-v2"

MODEL_URL = (
    "https://huggingface.co/optimum/all-MiniLM-L6-v2/"
    "resolve/main/model.onnx"
)

TOKENIZER_URL = (
    "https://huggingface.co/optimum/all-MiniLM-L6-v2/"
    "resolve/main/tokenizer.json"
)

FILES = {
    "model.onnx": MODEL_URL,
    "tokenizer.json": TOKENIZER_URL,
}


def download_file(filename, url):

    destination = MODEL_DIR / filename

    if destination.exists() and destination.stat().st_size > 0:
        print(f"Already available: {filename}")
        return

    temporary_file = destination.with_suffix(
        destination.suffix + ".part"
    )

    print(f"Downloading: {filename}")

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AI-Resume-Analyzer/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            with open(temporary_file, "wb") as output:
                shutil.copyfileobj(response, output)

        if not temporary_file.exists() or temporary_file.stat().st_size == 0:
            raise RuntimeError(f"Downloaded file is empty: {filename}")

        temporary_file.replace(destination)

        print(f"Downloaded successfully: {filename}")

    except Exception:
        if temporary_file.exists():
            temporary_file.unlink()
        raise


def main():

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    for filename, url in FILES.items():
        download_file(filename, url)

    print("\nMiniLM model setup completed.")


if __name__ == "__main__":
    main()
