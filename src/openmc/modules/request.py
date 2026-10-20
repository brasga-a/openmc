import requests
from pathlib import Path
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


def add_loader(v: str) -> None:
    url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()

    path = Path.home() / ".local/share/openmc/loaders"
    path.mkdir(parents=True, exist_ok=True)

    for version in data["versions"]:
        if version["id"] != v:
            continue

        jar = path / f"{v}.jar"

        metadata = requests.get(version["url"], timeout=15)
        metadata.raise_for_status()

        server = metadata.json()["downloads"]["server"]
        server_url = server["url"]

        with requests.get(server_url, stream=True, timeout=30) as response:
            response.raise_for_status()

            total = int(response.headers.get("content-length", 0)) or None

            with Progress(
                TextColumn("[cyan]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
            ) as progress:

                task = progress.add_task(
                    f"Downloading {v}",
                    total=total
                )

                with open(jar, "wb") as file:
                    for chunk in response.iter_content(chunk_size=65536):
                        if chunk:
                            file.write(chunk)
                            progress.update(task, advance=len(chunk))

        database.register_loader(
            version["id"],
            version["id"],
            version["type"],
            server["sha1"],
            str(jar)
        )
        return

    print(f"Version {v} not found")
