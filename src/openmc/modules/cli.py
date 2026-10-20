"""OpenMC command-line interface."""

import argparse
import sqlite3

import requests
from rich.console import Console
from rich.table import Table

from openmc.modules import request, database


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="openmc",
        description="A Minecraft server manager for Linux",
    )

    commands = parser.add_subparsers(dest="command", required=True)

    list_cmd = commands.add_parser("list", help="List servers")
    list_cmd.add_argument(
        "--loaders", action="store_true", help="List installed loaders"
    )

    add_cmd = commands.add_parser("add", help="Download a vanilla server JAR")
    add_cmd.add_argument("version")

    args = parser.parse_args()

    try:
        database.init_db()
        match args.command:
            case "add":
                request.add_loader(args.version)
                print(f"Installed vanilla loader for Minecraft {args.version}")
            case "list":
                if args.loaders:
                    print_loaders(database.get_loaders())
                else:
                    print("Server listing is not implemented yet.")
    except (requests.RequestException, sqlite3.Error, OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"openmc: error: {exc}\n")


def print_loaders(loaders: list[tuple]) -> None:
    console = Console()
    table = Table(title="Installed Loaders")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Version")
    table.add_column("Type", style="yellow")

    for loader in loaders:
        table.add_row(*(str(value) for value in loader[:4]))

    console.print(table)
