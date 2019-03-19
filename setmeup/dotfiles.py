# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

import click
from pkg_resources import resource_filename, resource_string

ASSETDIR = "assets/dotfiles"
DOTFILES = json.loads(resource_string("setmeup", "assets/assets.json"))


def main(fn, **kwargs):
    dotfile = Dotfile(fn)

    click.echo(dotfile.source_path)
    click.echo(dotfile.target_path)
    click.echo(dotfile.is_installed())

    click.echo(str(kwargs))

    dotfile.install()

    exit()
    dotfiles = get_dotfiles_to_install()

    print("\nThe following dotfiles will be installed:\n")
    for src, tar in dotfiles:
        print("\t{:13}\tto\t{}".format(src.split(os.sep)[-1], tar))

    if input("\nContinue? ").lower() not in ("yes", "y"):
        return

    for src, tar in dotfiles:
        print("\nInstalling {} to {} ...".format(src, tar))
        # shutil.copy2(src, tar)
        print("Installing {} to {} ... done.".format(src, tar))


class Dotfile:
    def __init__(self, fn):
        self.filename = fn
        self.source_path = Path(resource_filename("setmeup", f"assets/dotfiles/{fn}"))
        self.target_path = Path(read_target_path(self.source_path)).expanduser()

    def is_installed(self):
        return self.target_path.exists()

    def install(self):
        choice = click.prompt(
            f"Install {self.filename} to {self.target_path}",
            default="yes",
            type=click.Choice(["yes", "no"]),
        )
        if choice == "no":
            click.echo(f"Skipping install for {self.filename}.")
            return 0

        if self.is_installed():
            choice = click.prompt(
                f"Dotfile {self.filename} exists. Replace it?",
                default="no",
                type=click.Choice(["yes", " no"]),
            )
            if choice == "no":
                click.echo(f"Skipping install for {self.filename}.")
                return 0
            if self.target_path.is_file():
                os.remove(self.target_path)
            elif self.target_path.is_symlink():
                self.target_path.unlink()

        self.target_path.symlink_to(self.source_path)

        click.echo(f"you chose {choice}")


def read_target_path(filepath):
    """Read the first line of a dotfile to see where it should be placed."""
    with open(filepath, "r") as f:
        first_line = f.readline()  # e.g.: # ~/.bashrc
    return first_line.split(" ")[1].rstrip()  # remove comment marker and trailing \n


def file_exists(filepath):
    return os.path.exists(filepath)


def get_dotfiles_to_install():
    """Gather up a list of which dotfiles need to be installed.

    Dotfiles that don't already exist in the target path will be automatically
    added to the list. Dotfiles that do exist need to be manually confirmed.
    """
    dotfiles_to_install = []
    for fn in DOTFILES:
        fn_source = resource_filename("setmeup", os.sep.join([ASSETDIR, fn]))
        fn_target = os.path.expanduser(read_target_path(os.sep.join([ASSETDIR, fn])))
        if file_exists(fn_target):
            answer = input("{} already exists. Overwrite it? ".format(fn_target))
            if answer.lower() not in ("yes", "y"):
                continue
        dotfiles_to_install.append((fn_source, fn_target))
    return dotfiles_to_install


if __name__ == "__main__":
    main()
