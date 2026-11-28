#!/usr/bin/env python3
"""Bind Windows build inputs to an independently verified Cygwin index."""

import argparse
import hashlib
import lzma
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory

from verify_source_sdk import sha256, write_json


CYGWIN_FINGERPRINT = "56405CF6FCC81574682A5D561A698DE9E2E56300"
PACKAGE_ARCHES = {"x86_64", "noarch"}


def verify_index(index, signature, public_key, gpg):
    with TemporaryDirectory(prefix="cygwin-gpg-") as home:
        command = [str(gpg), "--homedir", home, "--batch", "--no-auto-key-retrieve"]
        subprocess.run([*command, "--import", str(public_key)], check=True, timeout=30)
        result = subprocess.run([*command, "--status-fd", "1", "--verify", str(signature), str(index)],
                                check=True, timeout=30, capture_output=True, text=True)
    signatures = [line.split() for line in result.stdout.splitlines() if line.startswith("[GNUPG:] VALIDSIG ")]
    if len(signatures) != 1 or signatures[0][2] != CYGWIN_FINGERPRINT or signatures[0][-1] != CYGWIN_FINGERPRINT:
        raise ValueError("The Cygwin index does not have the expected release signature")


def index_packages(index):
    packages = {}
    architecture = None
    with lzma.open(index, "rt", encoding="utf-8", errors="replace") as source:
        for line in source:
            if line.startswith("arch:"):
                architecture = line.split(":", 1)[1].strip()
            if not line.startswith("install: "):
                continue
            _, path, size, checksum = line.split()
            if re.fullmatch(r"[0-9a-f]{128}", checksum):
                material = (int(size), checksum)
                if packages.setdefault(path, material) != material:
                    raise ValueError(f"Ambiguous signed Cygwin index entry: {path}")
    if architecture != "x86_64" or not packages:
        raise ValueError("The signed Cygwin index does not contain the x64 package catalog")
    return packages


def cache_receipt(cache, index, signature):
    packages = index_packages(index)
    actual = {}
    for archive in sorted(cache.rglob("*.tar.*")):
        path_parts = archive.relative_to(cache).parts
        arch = next((position for position, part in enumerate(path_parts) if part in PACKAGE_ARCHES), None)
        if arch is None or not archive.is_file() or archive.is_symlink():
            raise ValueError(f"Unexpected Cygwin cache entry: {archive.name}")
        path = "/".join(path_parts[arch:])
        with archive.open("rb") as content:
            material = (archive.stat().st_size, hashlib.file_digest(content, "sha512").hexdigest())
        if path in actual or packages.get(path) != material:
            raise ValueError(f"Cygwin cache bytes differ from the signed index: {path}")
        actual[path] = {"bytes": material[0], "sha512": material[1]}
    if not actual:
        raise ValueError("The hosted Cygwin package cache is empty")
    return {"signing_fingerprint": CYGWIN_FINGERPRINT, "index_sha256": sha256(index),
            "signature_sha256": sha256(signature), "package_count": len(actual), "packages": actual}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("cache", "index", "signature", "public-key", "gpg", "output"):
        parser.add_argument(f"--{option}", type=Path, required=True)
    args = parser.parse_args()
    verify_index(args.index, args.signature, args.public_key, args.gpg)
    write_json(args.output, cache_receipt(args.cache, args.index, args.signature))
