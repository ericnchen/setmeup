# -*- coding: utf-8 -*-
import os
import shutil


ASSETDIR = "assets/dotfiles"
DOTFILES = (
    ".bash_profile",
    ".bashrc",
    ".condarc",
    ".editorconfig",
    ".gitconfig",
    ".gitignore",
    ".vimrc",
)


def main():
    dotfiles = get_dotfiles_to_install()

    print("\nThe following dotfiles will be installed:\n")
    for src, tar in dotfiles:
        print("\t {} to {}".format(src, tar))

    if input("\nContinue? ").lower() not in ("yes", "y"):
        return

    for src, tar in dotfiles:
        print("\nInstalling {} to {} ...".format(src, tar))
        shutil.copy2(os.path.abspath(os.sep.join([ASSETDIR, src])), tar)
        print("Installing {} to {} ... done.".format(src, tar))


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
        fn_target = os.path.expanduser(read_target_path(os.sep.join([ASSETDIR, fn])))
        if file_exists(fn_target):
            answer = input("{} already exists. Overwrite it? ".format(fn_target))
            if answer.lower() not in ("yes", "y"):
                continue
        dotfiles_to_install.append((fn, fn_target))
    return dotfiles_to_install


if __name__ == "__main__":
    main()
