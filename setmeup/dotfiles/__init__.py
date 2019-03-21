# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Any, List

import click
from pkg_resources import resource_filename, resource_listdir

IGNORED = "__init__.py", "__pycache__"


class Dotfile:
    def __init__(self, fn: str) -> None:
        self.filename = fn

    @property
    def source(self) -> Path:
        """Return a Path object to the source file."""
        return Path(resource_filename(__name__, self.filename))

    @property
    def target(self) -> Path:
        """Return a Path object to the target file."""
        with self.source.open() as f:
            p = f.readline()
        return Path(p.rstrip().split(" ")[-1]).expanduser()

    def is_installed(self) -> bool:
        """Check if the dotfile has been installed to the target path."""
        return self.target.exists()

    def install(self, **kwargs: Any) -> None:
        """Install this dotfile to the appropriate target path."""
        msg = f"Installing {self.filename} to {self.source.resolve()} ..."
        if kwargs.get("dry_run"):
            click.echo(f"[DRY RUN] {msg}")
        else:
            click.echo(msg)
            self.target.write_text(self.source.read_text())


def list_dotfiles() -> List[str]:
    """Return a tuple of all provided dotfiles."""
    dfs = [fn for fn in resource_listdir(__name__, "") if fn not in IGNORED]
    return sorted(dfs)


def collect_dotfiles(dotfiles: List[Dotfile], **kwargs: Any) -> List[Dotfile]:
    collected = []
    for df in dotfiles:
        if df.is_installed():
            if kwargs.get("confirm_yes"):
                choice = "yes"
            else:
                choice = click.prompt(
                    f"Replace existing {df.filename}?",
                    default="no",
                    type=click.Choice(["yes", "no"]),
                )
            if choice == "no":
                continue
        collected.append(df)
    return collected


@click.group(name="dotfiles")
def dotfiles_main():
    pass


@click.command(name="list")
def dotfiles_list() -> int:
    """List available and/or installed dotfiles."""
    click.echo("The following dotfiles are provided:")
    for fn in list_dotfiles():
        click.echo(f"\t{click.format_filename(fn)}")
    return 0


@click.command(name="install")
@click.argument(
    "fn", nargs=-1, type=click.Choice(list_dotfiles()), metavar="<filename>..."
)
@click.option("-a", "--all", "install_all", help="Install all dotfiles.", is_flag=True)
@click.option(
    "-y",
    "--yes",
    "confirm_yes",
    help="Automatically confirm all prompts with yes.",
    is_flag=True,
)
@click.option(
    "--dry-run",
    help="Execute the installation but without installing anything.",
    is_flag=True,
)
def dotfiles_install(fn, **kwargs) -> int:
    """Install a dotfile or multiple dotfiles."""
    if kwargs.get("install_all"):
        fn = list_dotfiles()

    collected = collect_dotfiles([Dotfile(f) for f in fn], **kwargs)
    if len(collected) == 0:
        click.echo("Nothing to install.")
        return 0

    if kwargs.get("confirm_yes"):
        proceed = "yes"
    else:
        proceed = click.prompt(
            f"Installing {len(collected)} dotfiles. Proceed?",
            type=click.Choice(["yes", "no"]),
            default="no",
        )
    if proceed == "no":
        click.echo("Install canceled.")
        return 0

    [df.install(**kwargs) for df in collected]

    return 0


dotfiles_main.add_command(dotfiles_list)
dotfiles_main.add_command(dotfiles_install)
