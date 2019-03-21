# -*- coding: utf-8 -*-
import click

from setmeup.dotfiles import dotfiles_main


@click.group()
def main():
    pass


main.add_command(dotfiles_main)
