# OpenMC

An open-source CLI tool for managing Minecraft servers on Linux.

## Features

- **Mojang Loader Downloads**: Fetch and download official Minecraft server `.jar` versions directly from Mojang's version manifest with real-time progress bars.
- **Local Registry**: Automatically tracks installed server loaders and metadata (version, release type, SHA-1, file path) in a local SQLite database (`~/.local/share/openmc/chest.db`).
- **Rich Terminal UI**: Clean, formatted tables and download progress indicators powered by [Rich](https://github.com/Textualize/rich).

## Requirements

- **OS**: Linux
- **Python**: `>= 3.10` (`python3` and `python3-venv`)
- **Git**: `git`

## Installation

Install directly using `curl`:

```bash
curl -fsSL https://raw.githubusercontent.com/brasga-a/openmc/master/install.sh | bash
```

### Manual Installation

```bash
git clone https://github.com/brasga-a/openmc.git
cd openmc
./install.sh
```

## Usage

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
- **CLI Environment**: `~/.local/share/openmc/env/`

## Project Structure

```text
openmc/
├── install.sh
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
