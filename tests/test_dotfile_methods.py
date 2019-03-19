# -*- coding: utf-8 -*-
from pathlib import Path
from setmeup.dotfiles import Dotfile
from setmeup.cli import dotfiles_install
from click.testing import CliRunner


def test_foo():
    bashrc = Dotfile(".bashrc")
    source_file = Path().cwd() / "setmeup" / "assets" / "dotfiles" / ".bashrc"
    assert bashrc.source_path == source_file
    assert bashrc.target_path == Path().home() / ".bashrc"
    assert bashrc.is_installed() is True


def test_install_one_file():
    runner = CliRunner()
    result = runner.invoke(dotfiles_install, ["--dry-run", ".bashrc"])
    assert result.exit_code == 0
