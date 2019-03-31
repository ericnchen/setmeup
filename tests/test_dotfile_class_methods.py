# -*- coding: utf-8 -*-
import setmeup.dotfiles


def test_dotfiles_are_importable():
    assert setmeup.dotfiles.bash_profile.name == ".bash_profile"
    assert setmeup.dotfiles.bashrc.name == ".bashrc"
    assert setmeup.dotfiles.condarc.name == ".condarc"
    assert setmeup.dotfiles.editorconfig.name == ".editorconfig"
    assert setmeup.dotfiles.gitconfig.name == ".gitconfig"
    assert setmeup.dotfiles.gitignore.name == ".gitignore"
    assert setmeup.dotfiles.vimrc.name == ".vimrc"
