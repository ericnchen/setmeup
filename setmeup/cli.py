# -*- coding: utf-8 -*-
"""
Usage:
    dtf install [-yam] [--[no-]dry-run] [--[no-]debug] <filename>...

Options:
    -h, --help      Show this menu and exit.
    -y, --yes       Answer yes to all confirmation prompts.
    -a, --all       Select all provided dotfiles.
    -m, --missing   Select only missing dotfiles.
    --[no-]dry-run  Enable or disable dry run mode.
    --[no-]debug    Enable or disable debug mode.
"""
from __future__ import annotations

import os
import pathlib
from typing import Any, List, Sequence

import click

from . import dotfiles

Filenames = Sequence[str]
Dotfiles = List[dotfiles.Dotfile]

XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", "~/.config")
INSTALL_PATH = pathlib.Path(XDG_CONFIG_HOME).expanduser() / "dtf"


@click.group(name="dtf")
def main() -> None:
    return


@click.command("install")
@click.argument("filenames", nargs=-1, metavar="<filename>...")
@click.option("-y", "--yes", is_flag=True, default=False)
@click.option("-a", "--all", is_flag=True, default=False)
@click.option("-m", "--missing", is_flag=True, default=False)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--debug/--no-debug", is_flag=True, default=False)
def dtf_install(filenames: Filenames, **kwargs: Any) -> None:
    check_flag("yes")
    check_flag("dry_run")

    if not INSTALL_PATH.exists():
        mkdir(INSTALL_PATH)

    collected_dotfiles = collect(filenames)

    message("The following dotfiles will be installed:")
    [message(f"\t{df.name}") for df in collected_dotfiles]

    if not confirm("Continue with install?"):
        return message("Nothing to do.")

    symlinked_dotfiles = symlink(install(collected_dotfiles))

    message("The following dotfiles have been installed:")
    [message(f"\t{df.name}") for df in symlinked_dotfiles]


def message(msg: str, debug_only: bool = False) -> None:
    """Output a message, automatically prepending it with [DEBUG] if needed."""
    debug_mode = click.get_current_context().params["debug"]
    if debug_only and not debug_mode:
        return
    click.echo(f"[DEBUG] {msg}" if debug_mode else msg)


def confirm(msg: str, default: bool = False) -> bool:
    params = click.get_current_context().params
    if params["yes"]:
        return True
    return click.confirm(f"[DEBUG] {msg}" if params["debug"] else msg, default=default)


def check_flag(flag_name: str) -> None:
    """Check if a flag is enabled, and output a message if appropriate."""
    if not click.get_current_context().params[flag_name]:
        return
    message(f"Enable {flag_name.upper()}", debug_only=True)


def mkdir(fp: pathlib.Path) -> None:
    if click.get_current_context().params["dry_run"]:
        return
    fp.mkdir(parents=True, exist_ok=True)


def collect(filenames: Filenames) -> Dotfiles:
    params = click.get_current_context().params

    if params["all"]:
        return dotfiles.all_dotfiles

    from_files = []
    for fn in filenames:
        fn_ = fn[1:] if fn.startswith(".") else fn
        if fn_ in dir(dotfiles):
            from_files.append(getattr(dotfiles, fn_))

    from_missing = []
    if params["missing"]:
        from_missing = [df for df in dotfiles.all_dotfiles if not df.target.exists()]

    return list(set(from_files + from_missing))


def install(collected: Dotfiles) -> Dotfiles:
    params = click.get_current_context().params

    installed = []
    for df in collected:
        if params["yes"]:
            installed.append(df)
        else:
            if confirm(f"Overwrite {INSTALL_PATH / df.name}?", default=True):
                installed.append(df)

    if not params["dry_run"]:
        [(INSTALL_PATH / df.name).write_text(df.source.read_text()) for df in installed]

    return installed


def symlink(installed: Dotfiles) -> Dotfiles:
    params = click.get_current_context().params

    symlinks = []
    actual_files = []
    installables = []
    for df in installed:
        if df.target.is_symlink():
            symlinks.append(df)
        elif df.target.is_file():
            actual_files.append(df)
        else:
            installables.append(df)

    if actual_files:
        mkdir(INSTALL_PATH / "originals")

    symlinked = [_ for _ in installables]
    if not params["dry_run"]:
        for df in symlinks:
            df.target.unlink()
            symlinked.append(df)

        for df in actual_files:
            df.target.rename(INSTALL_PATH / "originals" / df.name)
            symlinked.append(df)

        for df in symlinked:
            df.target.symlink_to(INSTALL_PATH / df.name)

    return symlinked


main.add_command(dtf_install)
