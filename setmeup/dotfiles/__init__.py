# -*- coding: utf-8 -*-
import subprocess
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
            return

        click.echo(msg)
        self.target.write_text(self.source.read_text())


def list_dotfiles() -> List[str]:
    """Return a tuple of all provided dotfiles."""
    dfs = [fn for fn in resource_listdir(__name__, "") if fn not in IGNORED]
    return sorted(dfs)


def collect_dotfiles(dotfiles: List[Dotfile], **kwargs: Any) -> List[Dotfile]:
    if kwargs.get("confirm_yes"):
        return dotfiles

    collected = []
    for df in dotfiles:
        choice = True
        if df.is_installed():
            choice = click.confirm(f"Replace existing {df.filename}?")
        if choice is False:
            continue
        collected.append(df)
    return collected


@click.group(name="dotfiles")
def dotfiles_main():
    pass


def list_available() -> None:
    click.echo("The following dotfiles are available:")
    for fn in list_dotfiles():
        click.echo(f"\t{click.format_filename(fn)}")


def list_installed(show_path: bool = False) -> None:
    click.echo("The following dotfiles are installed:")
    for fn in list_dotfiles():
        df = Dotfile(fn)
        if df.target.exists():
            fp = str(df.target) if show_path else fn
            click.echo(f"\t{click.format_filename(fp)}")


def list_not_installed() -> None:
    click.echo("The following dotfiles are not installed:")
    for fn in list_dotfiles():
        df = Dotfile(fn)
        if df.target.exists():
            continue
        click.echo(f"\t{click.format_filename(fn)}")


@click.command(name="list")
@click.option("--show-path", is_flag=True)
@click.option("--installed", is_flag=True)
@click.option("--not-installed", is_flag=True)
@click.pass_context
def dotfiles_list(ctx: click.Context, **kwargs) -> None:
    """List available and/or installed dotfiles."""
    if kwargs["installed"]:
        list_installed(show_path=kwargs["show_path"])
    elif kwargs["not_installed"]:
        list_not_installed()
    else:
        list_available()
    ctx.exit()


help_all = "Install all dotfiles."
help_dry = "Execute the installation but without installing anything."
help_yes = "Automatically confirm all prompts with yes."

dotfile_choices = click.Choice(list_dotfiles())


@click.command(name="install")
@click.argument("fn", nargs=-1, type=dotfile_choices, metavar="<filename>...")
@click.option("-a", "--all", "install_all", help=help_all, is_flag=True)
@click.option("-y", "--yes", "confirm_yes", help=help_yes, is_flag=True)
@click.option("--dry-run", help=help_dry, is_flag=True)
@click.pass_context
def dotfiles_install(ctx, fn, **kwargs) -> None:
    """Install a dotfile or multiple dotfiles."""
    if kwargs.get("install_all"):
        fn = list_dotfiles()
    collected = collect_dotfiles([Dotfile(f) for f in fn], **kwargs)
    if len(collected) == 0:
        click.echo("Nothing to install.")
        ctx.exit()
    if kwargs.get("confirm_yes"):
        pass
    else:
        click.confirm(f"Installing {len(collected)} dotfiles. Proceed?", abort=True)
    [df.install(**kwargs) for df in collected]
    ctx.exit()


ctx_diff_kwds = {"ignore_unknown_options": True, "allow_extra_args": True}


@click.command(name="diff", context_settings=ctx_diff_kwds)
@click.argument("fn", type=dotfile_choices, metavar="<filename>")
@click.pass_context
def dotfiles_diff(ctx: click.Context, fn: str, **kwargs: Any) -> None:
    df = Dotfile(fn)
    subprocess.call(["diff", *ctx.args, str(df.source), str(df.target)])
    ctx.exit()


dotfiles_main.add_command(dotfiles_diff)
dotfiles_main.add_command(dotfiles_list)
dotfiles_main.add_command(dotfiles_install)
