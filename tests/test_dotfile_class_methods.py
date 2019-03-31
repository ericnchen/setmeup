# -*- coding: utf-8 -*-
import dtf.dotfiles


def test_dotfiles_are_importable():
    assert dtf.dotfiles.bash_profile.name == ".bash_profile"
    assert dtf.dotfiles.bashrc.name == ".bashrc"
    assert dtf.dotfiles.condarc.name == ".condarc"
    assert dtf.dotfiles.editorconfig.name == ".editorconfig"
    assert dtf.dotfiles.gitconfig.name == ".gitconfig"
    assert dtf.dotfiles.gitignore.name == ".gitignore"
    assert dtf.dotfiles.vimrc.name == ".vimrc"
