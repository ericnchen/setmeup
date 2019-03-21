# -*- coding: utf-8 -*-
from pathlib import Path

from setmeup.dotfiles import Dotfile, list_dotfiles


def test_list_dotfiles_returns_only_dotfiles():
    dotfiles = [
        ".bash_profile",
        ".bashrc",
        ".condarc",
        ".editorconfig",
        ".gitconfig",
        ".gitignore",
        ".vimrc",
    ]
    assert sorted(list_dotfiles()) == sorted(dotfiles)


def test_dotfile_class_source_path():
    assert Dotfile(".bashrc").source.exists()


def test_dotfile_class_target_path():
    assert Dotfile(".bashrc").target == Path().home() / ".bashrc"
