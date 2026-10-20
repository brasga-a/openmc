"""Download and verify official Minecraft server JARs."""

import hashlib

import requests
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)

from openmc.modules import database
from openmc.modules.paths import data_dir

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"


def add_loader(v: str) -> None:
    manifest_response = requests.get(MANIFEST_URL, timeout=15)
    manifest_response.raise_for_status()

    version = next(
        (item for item in manifest_response.json()["versions"] if item["id"] == v),
        None,
    )
    if version is None:
        raise ValueError(f"Minecraft version {v!r} not found")

    metadata_response = requests.get(version["url"], timeout=15)
    metadata_response.raise_for_status()
    server = metadata_response.json().get("downloads", {}).get("server")
    if server is None:
        raise ValueError(f"Minecraft version {v!r} has no server JAR")

    expected_sha1 = server["sha1"].lower()
    expected_size = server.get("size")
    path = data_dir() / "loaders"
    path.mkdir(parents=True, exist_ok=True)
    jar = path / f"{v}.jar"
    partial = path / f"{v}.jar.part"

    try:
        with requests.get(server["url"], stream=True, timeout=30) as response:
            response.raise_for_status()
            total = expected_size or int(response.headers.get("content-length", 0)) or None
            digest = hashlib.sha1()
            bytes_written = 0

            with Progress(
                TextColumn("[cyan]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(f"Downloading {v}", total=total)
                with partial.open("wb") as file:
                    for chunk in response.iter_content(chunk_size=65536):
                        if chunk:
                            file.write(chunk)
                            digest.update(chunk)
                            bytes_written += len(chunk)
                            progress.update(task, advance=len(chunk))

        if expected_size is not None and bytes_written != expected_size:
            raise ValueError(f"Incomplete download: expected {expected_size} bytes, got {bytes_written}")
        if digest.hexdigest() != expected_sha1:
            raise ValueError(f"SHA-1 mismatch for Minecraft server {v!r}")

        partial.replace(jar)
    except Exception:
        partial.unlink(missing_ok=True)
        raise

    # Only register a JAR after successful download and hash verification.
    database.register_loader("vanilla", v, version["type"], expected_sha1, str(jar))
