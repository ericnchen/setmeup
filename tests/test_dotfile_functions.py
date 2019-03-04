# -*- coding: utf-8 -*-
from setmeup.dotfiles import read_target_path, file_exists


def test_read_target_path_is_correct():
    assert read_target_path("setmeup/assets/dotfiles/.bashrc") == "~/.bashrc"


def test_file_exists_is_true_when_file_exists():
    assert file_exists("setmeup/assets/dotfiles/.bashrc") is True


def test_file_exists_is_true_when_file_doesnt_exist():
    assert file_exists("fake/file/doesnt/exist.ext") is False
