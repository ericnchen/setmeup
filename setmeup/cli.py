# -*- coding: utf-8 -*-
import click
from pkg_resources import resource_listdir
from setmeup.dotfiles import Dotfile


@click.group()
def cli():
    pass


@click.group()
def dotfiles():
    pass


@click.command("install")
@click.argument("fn")
@click.option("-y", "--yes", "confirm_yes", flag_value=True, default=False)
@click.option("--dry-run", flag_value=True, default=False)
def dotfiles_install(fn, **kwargs):
    if fn not in resource_listdir("setmeup", "assets/dotfiles"):
        click.echo(f"{fn} not a valid dotfile")

    dotfile = Dotfile(fn)
    click.echo(dotfile.is_installed())


cli.add_command(dotfiles)
dotfiles.add_command(dotfiles_install)
