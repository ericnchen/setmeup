# -*- coding: utf-8 -*-
"""
Usage:
    dtf install [--yes] [--[no-]backup] ((--all | --missing) | <filename>...)
    dtf list (--all | --installed [--full] | --missing)
    dtf update [--yes] ((--all | --installed | --missing) | <filename>...)
    dtf uninstall [--yes] [--[no-]restore] (--all | <filename>...)

Options:
    -h, --help      Show this menu and exit.
    -y, --yes       Answer yes to all confirmation prompts.
    -a, --all       Select all provided dotfiles.
    -m, --missing   Select only missing dotfiles.
    -i, --installed Select only installed dotfiles.
    -f, --full      Show full path output.
    --[no-]backup   Existing dotfiles are backed up by default, but can be disabled.
    --[no-]restore  Restore a dotfile to the original backed up dotfile, if it exists.
"""
from typing import Any, List, Sequence

import click
from click import Context


@click.group(name="dtf")
def main() -> None:
    pass


def validate_only_one(ctx: Context, params: List[str], **kwargs: Any) -> None:
    count = 0
    for k in params:
        count = count + 1 if kwargs.get(k) else count

    if count > 1:
        click.echo(f"Only one of {params} can be set.")
        ctx.exit(1)


def validate_require_one(ctx: Context, params: List[str], **kwargs: Any) -> None:
    count = 0
    for k in params:
        count = count + 1 if kwargs.get(k) else count

    if count == 0:
        click.echo(f"One of {params} is required.")
        ctx.exit(1)


def validate_incompatible(ctx: Context, params: List[str], **kwargs: Any) -> None:
    count = 0
    for k in params:
        count = count + 1 if kwargs.get(k) else count

    if len(params) == count:
        click.echo(f"The options {params} are not compatible.")
        ctx.exit(1)


@click.command("install")
@click.argument("fn", nargs=-1, metavar="<filename>...")
@click.option("-y", "--yes", is_flag=True, default=False)
@click.option("-a", "--all", is_flag=True, default=False)
@click.option("-m", "--missing", is_flag=True, default=False)
@click.option("--backup/--nobackup", is_flag=True, default=True)
@click.pass_context
def dtf_install(ctx: Context, fn: Sequence[str], **kwargs: Any) -> None:

    validate_only_one(ctx, ["all", "missing"], **kwargs)

    if (fn and kwargs.get("all")) or (fn and kwargs.get("missing")):
        click.echo("cannot give a filename and set --all/--missing at the same time")
        ctx.exit(1)


@click.command("list")
@click.option("-a", "--all", is_flag=True, default=False)
@click.option("-m", "--missing", is_flag=True, default=False)
@click.option("-i", "--installed", is_flag=True, default=False)
@click.option("-f", "--full", is_flag=True, default=False)
@click.pass_context
def dtf_list(ctx: Context, **kwargs: Any) -> None:

    validate_only_one(ctx, ["all", "missing", "installed"], **kwargs)
    validate_require_one(ctx, ["all", "missing", "installed"], **kwargs)
    validate_incompatible(ctx, ["all", "full"], **kwargs)
    validate_incompatible(ctx, ["missing", "full"], **kwargs)


main.add_command(dtf_install)
main.add_command(dtf_list)
