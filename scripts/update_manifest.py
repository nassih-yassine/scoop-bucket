#!/usr/bin/env python3
"""Rewrite bucket/dep-vet.json from the latest dep-vet GitHub release.

Idempotent: running it twice for the same release changes nothing.
"""

import json
import pathlib
import urllib.request

REPO = "nassih-yassine/Dep-Vet"
ASSET = "dep-vet-x86_64-pc-windows-msvc.zip"
MANIFEST = pathlib.Path("bucket/dep-vet.json")


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "dep-vet-scoop-bucket",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def main() -> int:
    release = json.loads(fetch(f"https://api.github.com/repos/{REPO}/releases/latest"))
    if release.get("draft") or release.get("prerelease"):
        print("latest release is a draft or prerelease; nothing to do")
        return 0

    tag = release["tag_name"]
    if not tag.startswith("v"):
        raise SystemExit(f"unexpected tag {tag!r}")
    version = tag[1:]

    assets = {asset["name"]: asset["browser_download_url"] for asset in release["assets"]}
    if ASSET not in assets:
        raise SystemExit(f"release {tag} has no {ASSET}")
    checksum = fetch(assets[ASSET + ".sha256"]).decode("utf-8", "replace").split()[0].lower()
    if len(checksum) != 64 or any(c not in "0123456789abcdef" for c in checksum):
        raise SystemExit(f"unreadable checksum for {ASSET}")

    manifest = json.loads(MANIFEST.read_text())
    manifest["version"] = version
    manifest["architecture"]["64bit"]["url"] = assets[ASSET]
    manifest["architecture"]["64bit"]["hash"] = checksum
    manifest["autoupdate"]["architecture"]["64bit"]["url"] = (
        f"https://github.com/{REPO}/releases/download/v$version/{ASSET}"
    )
    rendered = json.dumps(manifest, indent=2) + "\n"
    if MANIFEST.read_text() == rendered:
        print(f"{MANIFEST} is already at {tag}")
        return 0
    MANIFEST.write_text(rendered)
    print(f"updated {MANIFEST} to {tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
