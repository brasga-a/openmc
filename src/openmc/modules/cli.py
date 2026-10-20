import argparse
from openmc.modules import request, database
from rich.console import Console
from rich.table import Table

def main() -> None:
    database.init_db()

    parser = argparse.ArgumentParser(
        prog='openmc',
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True
    )

    list_cmd = commands.add_parser(
        "list",
        help="List servers"
    )

    list_cmd.add_argument(
        "--loaders",
        action="store_true",
        help="List installed loaders"
    )

    add_cmd = commands.add_parser(
        "add",
        help="Download a loader"
    )
    add_cmd.add_argument("version")

    args = parser.parse_args()

    match args.command:
        case "add":
            request.add_loader(args.version)
        case "list":
            if args.loaders:
                loaders = database.get_loaders()
                print_loaders(loaders)
            else:
                print("Listing servers...")




def print_loaders(loaders: list[tuple]) -> None:
    console = Console()

    table = Table(title="Installed Loaders")

    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Version")
    table.add_column("Type", style="yellow")

    for loader in loaders:
        table.add_row(
            str(loader[0]),
            str(loader[1]),
            str(loader[2]),
            str(loader[3])
        )

    console.print(table)
