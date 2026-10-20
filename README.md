# OpenMC

An open-source CLI tool for managing Minecraft servers on Linux.

## Features

- **Mojang Loader Downloads**: Fetch and download official Minecraft server `.jar` versions directly from Mojang's version manifest with real-time progress bars.
- **Local Registry**: Automatically tracks installed server loaders and metadata (version, release type, SHA-1, file path) in a local SQLite database (`~/.local/share/openmc/chest.db`).
- **Rich Terminal UI**: Clean, formatted tables and download progress indicators powered by [Rich](https://github.com/Textualize/rich).

## Requirements

- **OS**: Linux
- **Python**: `>= 3.14`
- **Package Manager**: [uv](https://docs.astral.sh/uv/) (recommended)

## Installation

Clone the repository and install the project using `uv`:

```bash
git clone <repository-url>
cd openmc
uv sync
```

You can also install `openmc` globally as a CLI tool:

```bash
uv tool install .
```

## Usage

If running inside the project environment with `uv`, prefix commands with `uv run`:

### Download a Server Loader

Download a specific Minecraft version (release or snapshot) to `~/.local/share/openmc/loaders/`:

```bash
openmc add <version>
```

**Example:**

```bash
openmc add 1.21.4
```

### List Installed Loaders

View all downloaded and registered server loaders in a formatted table:

```bash
openmc list --loaders
```

### List Servers

```bash
openmc list
```

## Data Storage

OpenMC stores its data in your user's local share directory following the XDG specification:

- **Database**: `~/.local/share/openmc/chest.db`
- **Server JARs**: `~/.local/share/openmc/loaders/<version>.jar`

## Project Structure

```text
openmc/
├── pyproject.toml
├── README.md
└── src/
    └── openmc/
        ├── __init__.py
        └── modules/
            ├── cli.py       # CLI argument parsing and Rich table output
            ├── database.py  # SQLite database initialization and queries
            └── request.py   # Mojang API requests and JAR downloader
```

## License

Open-source project. See license details in the repository.
