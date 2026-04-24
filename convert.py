import json
from collections import OrderedDict
from datetime import date
from pathlib import Path
from typing import Dict, List

import typer


class DomainBlocklistConverter:

    INPUT_FILE = "amazon.txt"
    PIHOLE_FILE = "parsedamazon"
    UNBOUND_FILE = "amazon-unbound.conf"
    ADGUARD_FILE = "amazon-adguard.txt"
    CATEGORIES_PATH = "categories"

    BLOCKLIST_ABOUT = "This blocklist helps to restrict access to Amazon and its domains. Contribute at https://github.com/nickspaargaren/no-amazon"

    def __init__(self) -> None:
        self.data: Dict[str, List[str]] = OrderedDict()
        self.timestamp: str = date.today().strftime("%Y-%m-%d")

    def read(self) -> None:
        """
        Read input file into `self.data`, a dictionary mapping category names to lists of member items.
        """
        with open(self.INPUT_FILE, "r") as f:
            category = None
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    category = line.lstrip("# ")
                    self.data.setdefault(category, [])
                else:
                    if category is None:
                        raise ValueError("Unable to store item without category")
                    self.data[category].append(line)

    def dump(self) -> None:
        """
        Output data in JSON format on STDOUT.
        """
        print(json.dumps(self.data, indent=4))

    def pihole(self) -> None:
        """
        Produce blocklist for the Pi-hole.
        """
        with open(self.PIHOLE_FILE, "w") as f:
            f.write(f"# {self.BLOCKLIST_ABOUT}\n")
            f.write(f"# Last updated: {self.timestamp}\n")
            for category, entries in self.data.items():
                f.write(f"# {category}\n")
                for entry in entries:
                    f.write(f"0.0.0.0 {entry}\n")

    def unbound(self) -> None:
        """
        Produce blocklist for the Unbound DNS server.
        """
        with open(self.UNBOUND_FILE, "w") as f:
            f.write(f"# {self.BLOCKLIST_ABOUT}\n")
            f.write(f"# Last updated: {self.timestamp}\n")
            for category, entries in self.data.items():
                f.write(f"\n# Category: {category}\n")
                for entry in entries:
                    f.write(f'local-zone: "{entry}" always_refuse\n')

    def adguard(self) -> None:
        """
        Produce blocklist for AdGuard.
        """
        with open(self.ADGUARD_FILE, "w") as f:
            f.write(f"! {self.BLOCKLIST_ABOUT}\n")
            f.write(f"! Last updated: {self.timestamp}\n")
            for category, entries in self.data.items():
                f.write(f"! {category}\n")
                for entry in entries:
                    f.write(f"||{entry}^\n")

    def categories(self) -> None:
        """
        Produce individual per-category blocklist files.
        """

        def write_file(path: Path, category: str, entries: List[str], line_prefix: str = "") -> None:
            """
            Generic function to write per-category file in both flavours.
            """
            with open(path, "w") as f:
                f.write(f"# {self.BLOCKLIST_ABOUT}\n")
                f.write(f"# Last updated: {self.timestamp}\n")
                f.write(f"# {category}\n")
                f.write(f"\n")
                for entry in entries:
                    f.write(f"{line_prefix}{entry}\n")

        for category, entries in self.data.items():

            # Compute file names.
            filename = category.replace(" ", "").lower()
            filepath = Path(self.CATEGORIES_PATH).joinpath(filename)
            text_file = filepath.with_suffix(".txt")
            parsed_file = Path(str(filepath) + "parsed")

            # Write two flavours of per-category file.
            write_file(text_file, category, entries, line_prefix="0.0.0.0 ")
            write_file(parsed_file, category, entries)

app = typer.Typer(help="Amazon domain blocklist converter")


@app.callback()
def setup(ctx: typer.Context) -> None:
    """
    Initialize converter and read input file.
    """
    converter = DomainBlocklistConverter()
    converter.read()
    ctx.obj = converter


@app.command()
def pihole(ctx: typer.Context) -> None:
    """
    Produce blocklist for Pi-hole.
    """
    print("Invoking subcommand 'pihole'")
    ctx.obj.pihole()


@app.command()
def unbound(ctx: typer.Context) -> None:
    """
    Produce blocklist for Unbound DNS server.
    """
    print("Invoking subcommand 'unbound'")
    ctx.obj.unbound()


@app.command()
def adguard(ctx: typer.Context) -> None:
    """
    Produce blocklist for AdGuard.
    """
    print("Invoking subcommand 'adguard'")
    ctx.obj.adguard()


@app.command()
def categories(ctx: typer.Context) -> None:
    """
    Produce individual per-category blocklist files.
    """
    print("Invoking subcommand 'categories'")
    ctx.obj.categories()


@app.command()
def all(ctx: typer.Context) -> None:
    """
    Generate all blocklist formats.
    """
    print("Invoking subcommand 'pihole'")
    ctx.obj.pihole()
    print("Invoking subcommand 'unbound'")
    ctx.obj.unbound()
    print("Invoking subcommand 'adguard'")
    ctx.obj.adguard()
    print("Invoking subcommand 'categories'")
    ctx.obj.categories()


@app.command(name="json")
def json_output(ctx: typer.Context) -> None:
    """
    Output data in JSON format for debugging.
    """
    ctx.obj.dump()


if __name__ == "__main__":
    app()
