# -*- coding: utf-8 -*-
from click.testing import CliRunner

from setmeup.cli import cli


def test_dotfiles_commands_exist():
    runner = CliRunner()
    assert runner.invoke(cli, ["dotfiles"]).exit_code == 0
