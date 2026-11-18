#!/usr/bin/env python3
"""Download the frozen raw data snapshot from Box into data/raw/.

This works from the project root or from inside the scripts/ folder:
    python scripts/download_data.py
"""

import hashlib
import sys
from pathlib import Path

import requests

# Find the project root from this script's own location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Direct Box links and expected SHA-256 hashes for the 2026-11-16 snapshot.
FILES = {
    "crashes_2023_2024.csv": {
        "url": "https://uofi.box.com/shared/static/8lhwlz4dxjsyhmxsr63kyuldtecr1y2l.csv",
        "sha256": "0e5fa1cce0fd16a169df39e81a09556db08a00ca0f22417b0d9390d830023490",
    },
    "people_2023_2024.csv": {
        "url": "https://uofi.box.com/shared/static/ojz1aww9109q5tfstoyoadmwqjedrfgk.csv",
        "sha256": "85157f9c76e86721cf4684293ac9cd29abd8a795803704fd6dea6b7886a39fdf",
    },
    "noaa_usw00094846.csv": {
        "url": "https://uofi.box.com/shared/static/1ka0x135afas8z6odobnn7n7pny7kc7v.csv",
        "sha256": "b271731e860445557fe66acd33400aea0e5755b955fd5118f0368d0d31c3adcf",
    },
}

CHUNK_SIZE = 1024 * 1024  # 1 MB at a time


def sha256_of_file(path):
    """Return the SHA-256 hash of a file, reading it in chunks."""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def download_file(url, dest):
    """Stream a file from url and save it to dest."""
    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    all_ok = True

    for filename, info in FILES.items():
        dest = RAW_DIR / filename
        expected = info["sha256"]

        # Skip the download if the file is already there and the hash matches.
        if dest.exists():
            actual = sha256_of_file(dest)
            if actual == expected:
                print(f"OK (already present): {filename}")
                continue
            print(f"Existing file has a different hash, re-downloading: {filename}")

        print(f"Downloading {filename} ...")
        try:
            download_file(info["url"], dest)
        except requests.RequestException as e:
            print(f"ERROR: failed to download {filename}: {e}")
            all_ok = False
            continue

        actual = sha256_of_file(dest)
        if actual == expected:
            print(f"OK: {filename}")
        else:
            print(f"ERROR: SHA-256 mismatch for {filename}")
            print(f"  expected: {expected}")
            print(f"  actual:   {actual}")
            all_ok = False

    if not all_ok:
        print("Download or checksum check failed. Stopping.")
        sys.exit(1)

    print("All files are present and checksums match.")


if __name__ == "__main__":
    main()
