# -*- coding: utf-8 -*-
from __future__ import annotations

import pathlib
from typing import Any

from pkg_resources import resource_filename


class PathDescriptor:
    """Source and target path descriptor."""

    __slots__ = "name"

    def __init__(self, name: str) -> None:
        self.name = name

    def __get__(self, obj: Dotfile, objtype: Any) -> pathlib.Path:
        if self.name not in ["source", "target"]:
            raise RuntimeError
        return self.source(obj) if self.name == "source" else self.target(obj)

    def __set__(self, obj: Any, val: Any) -> None:
        raise AttributeError

    @staticmethod
    def source(obj: Dotfile) -> pathlib.Path:
        """Return a Path object to the source file."""
        return pathlib.Path(resource_filename(__name__, obj.name))

    def target(self, obj: Dotfile) -> pathlib.Path:
        """Return a Path object to the target file."""
        with self.source(obj).open() as f:
            p = f.readline()
        return pathlib.Path(p.rstrip().split(" ")[-1]).expanduser()


class Dotfile:
    source = PathDescriptor("source")
    target = PathDescriptor("target")

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}')"


bash_profile = Dotfile(".bash_profile")
bashrc = Dotfile(".bashrc")
condarc = Dotfile(".condarc")
editorconfig = Dotfile(".editorconfig")
gitconfig = Dotfile(".gitconfig")
gitignore = Dotfile(".gitignore")
vimrc = Dotfile(".vimrc")

all_dotfiles = [v for v in dict(locals()).values() if isinstance(v, Dotfile)]
