# OpenMC

An open-source CLI tool for managing Minecraft servers on Linux.

> **Early development:** OpenMC currently downloads and registers **vanilla Minecraft server JARs**. Creating, starting, stopping, and listing server instances are not implemented yet.

## Features

- Download official Mojang vanilla server JARs with Rich progress bars.
- Verify SHA-1 checksums and download sizes before installation.
- Store installed loader metadata in SQLite. Reinstalling a version updates its record instead of duplicating it.
- Respect `XDG_DATA_HOME` (default: `~/.local/share`).

## Requirements

- Linux
- Python 3.10 or newer (with `venv`/`pip`)
- Git, for the installation script

## Installation

Inspect [`install.sh`](install.sh) before running it. The script clones the `main` branch, creates an isolated Python environment, and adds a command under `~/.local/bin`.

~~~sh
curl -fsSL https://raw.githubusercontent.com/brasga-a/openmc/main/install.sh -o install.sh
bash install.sh
~~~

For a development checkout with [`uv`](https://docs.astral.sh/uv/):

~~~sh
git clone https://github.com/brasga-a/openmc.git
cd openmc
uv sync
uv run openmc --help
~~~

For fish, if `~/.local/bin` is not already on `PATH`:

~~~fish
fish_add_path ~/.local/bin
~~~

## Usage

~~~sh
openmc add 1.21.4
openmc list --loaders
openmc --help
~~~

`openmc list` is reserved for listing actual server instances and is not implemented yet.

## Data storage

Default location: `~/.local/share/openmc/` (or `$XDG_DATA_HOME/openmc/` when set to an absolute path).

- `chest.db` — SQLite metadata database.
- `loaders/<version>.jar` — Verified Minecraft vanilla server JARs.
- `env/` — The isolated environment created by `install.sh`.

## Tests

From the project root:

~~~sh
uv run python -m unittest discover -s tests -v
~~~

## License

See [LICENSE](LICENSE).
